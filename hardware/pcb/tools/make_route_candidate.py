#!/usr/bin/env python3
"""Temporary DRC candidate: keep K11-K13, repack K10 and add K14."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 49)" in ln for ln in s.splitlines() if "(segment " in ln)
lines=s.splitlines(); lines=[ln for ln in lines if not (("(segment " in ln or "(via " in ln) and "(net 45)" in ln)]; s="\n".join(lines)+"\n"
parts=[
# K10 replacement: direct B.Cu escape from THT U2.17, low outer corridor
'  (segment (start 145.16 94.54) (end 149.0 96.0) (width 0.3) (layer "B.Cu") (net 45))',
'  (segment (start 149.0 96.0) (end 149.0 150.0) (width 0.3) (layer "B.Cu") (net 45))',
'  (segment (start 149.0 150.0) (end 175.62 150.0) (width 0.3) (layer "B.Cu") (net 45))',
'  (segment (start 175.62 150.0) (end 175.62 115.0) (width 0.3) (layer "B.Cu") (net 45))',
# K14 use freed F.Cu x=142-ish corridor then low F.Cu backbone
'  (segment (start 145.16 104.70) (end 142.0 106.0) (width 0.3) (layer "F.Cu") (net 49))',
'  (segment (start 142.0 106.0) (end 142.0 150.0) (width 0.3) (layer "F.Cu") (net 49))',
'  (segment (start 142.0 150.0) (end 247.62 150.0) (width 0.3) (layer "F.Cu") (net 49))',
'  (segment (start 247.62 150.0) (end 247.62 115.0) (width 0.3) (layer "F.Cu") (net 49))',
]
edge=s.find("  (gr_rect "); assert edge>0; s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Repacked K10 and added K14; K11-K13 unchanged")
