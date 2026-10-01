#!/usr/bin/env python3
"""Temporary DRC candidate: locally repack K11/K13 and add K14."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert not any("(net 49)" in ln for ln in s.splitlines() if "(segment " in ln)
# Remove only K11/net46 and K13/net48 in the temporary candidate.
lines=s.splitlines()
lines=[ln for ln in lines if not (("(segment " in ln or "(via " in ln) and ("(net 46)" in ln or "(net 48)" in ln))]
s="\n".join(lines)+"\n"
parts=[
# K11/net46: far-left F.Cu then lower backbone
'  (segment (start 145.16 97.08) (end 140.0 99.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 140.0 99.0) (end 140.0 144.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 140.0 144.0) (end 193.62 144.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 193.62 144.0) (end 193.62 115.0) (width 0.3) (layer "F.Cu") (net 46))',
# K13/net48: immediate B.Cu right escape, then y=140
'  (segment (start 145.16 102.16) (end 149.5 103.5) (width 0.3) (layer "B.Cu") (net 48))',
'  (segment (start 149.5 103.5) (end 149.5 140.0) (width 0.3) (layer "B.Cu") (net 48))',
'  (segment (start 149.5 140.0) (end 229.62 140.0) (width 0.3) (layer "B.Cu") (net 48))',
'  (segment (start 229.62 140.0) (end 229.62 115.0) (width 0.3) (layer "B.Cu") (net 48))',
# K14/net49: freed central F.Cu lane, switch below relay region
'  (segment (start 145.16 104.70) (end 143.5 106.0) (width 0.3) (layer "F.Cu") (net 49))',
'  (segment (start 143.5 106.0) (end 143.5 130.0) (width 0.3) (layer "F.Cu") (net 49))',
'  (via (at 143.5 130.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 49))',
'  (segment (start 143.5 130.0) (end 143.5 142.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 143.5 142.0) (end 247.62 142.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 247.62 142.0) (end 247.62 115.0) (width 0.3) (layer "B.Cu") (net 49))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Repacked K11/K13 and added K14 candidate")
