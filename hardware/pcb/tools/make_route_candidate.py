#!/usr/bin/env python3
"""Temporary DRC candidate: best K11+K14 topology with two local K11 layer hops."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 49)" in ln for ln in s.splitlines() if "(segment " in ln)
lines=s.splitlines(); lines=[ln for ln in lines if not (("(segment " in ln or "(via " in ln) and "(net 46)" in ln)]; s="\n".join(lines)+"\n"
parts=[
# K11: original left replacement, but hop to B.Cu across K10 x=142.
'  (segment (start 145.16 97.08) (end 143.0 97.9) (width 0.3) (layer "F.Cu") (net 46))',
'  (via (at 143.0 97.9) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 46))',
'  (segment (start 143.0 97.9) (end 140.0 99.0) (width 0.3) (layer "B.Cu") (net 46))',
'  (via (at 140.0 99.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 46))',
'  (segment (start 140.0 99.0) (end 140.0 134.5) (width 0.3) (layer "F.Cu") (net 46))',
# hop to B.Cu while crossing K12 F.Cu y=136, return after it
'  (via (at 140.0 134.5) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 46))',
'  (segment (start 140.0 134.5) (end 140.0 137.5) (width 0.3) (layer "B.Cu") (net 46))',
'  (via (at 140.0 137.5) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 46))',
'  (segment (start 140.0 137.5) (end 140.0 146.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 140.0 146.0) (end 193.62 146.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 193.62 146.0) (end 193.62 115.0) (width 0.3) (layer "F.Cu") (net 46))',
# K14 topology already shown clean in best artifact
'  (segment (start 145.16 104.70) (end 143.5 106.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 143.5 106.0) (end 143.5 142.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 143.5 142.0) (end 247.62 142.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 247.62 142.0) (end 247.62 115.0) (width 0.3) (layer "B.Cu") (net 49))',
]
edge=s.find("  (gr_rect "); assert edge>0; s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("K11 local layer hops + clean K14 candidate")
