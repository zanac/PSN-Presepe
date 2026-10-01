#!/usr/bin/env python3
"""Temporary DRC candidate: keep K11/K13, replace only K12 and add K14."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 49)" in ln for ln in s.splitlines() if "(segment " in ln)
lines=s.splitlines(); lines=[ln for ln in lines if not (("(segment " in ln or "(via " in ln) and "(net 47)" in ln)]; s="\n".join(lines)+"\n"
parts=[
# K12 replacement: escape on F.Cu to outer-left, then B.Cu low corridor to K12.5
'  (segment (start 145.16 99.62) (end 141.0 101.0) (width 0.3) (layer "F.Cu") (net 47))',
'  (segment (start 141.0 101.0) (end 141.0 132.0) (width 0.3) (layer "F.Cu") (net 47))',
'  (via (at 141.0 132.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 47))',
'  (segment (start 141.0 132.0) (end 141.0 144.0) (width 0.3) (layer "B.Cu") (net 47))',
'  (segment (start 141.0 144.0) (end 211.62 144.0) (width 0.3) (layer "B.Cu") (net 47))',
'  (segment (start 211.62 144.0) (end 211.62 115.0) (width 0.3) (layer "B.Cu") (net 47))',
# K14 takes former K12 right-side lane, then F.Cu lower corridor
'  (segment (start 145.16 104.70) (end 147.0 106.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 147.0 106.0) (end 147.0 138.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (via (at 147.0 138.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 49))',
'  (segment (start 147.0 138.0) (end 147.0 142.0) (width 0.3) (layer "F.Cu") (net 49))',
'  (segment (start 147.0 142.0) (end 247.62 142.0) (width 0.3) (layer "F.Cu") (net 49))',
'  (segment (start 247.62 142.0) (end 247.62 115.0) (width 0.3) (layer "F.Cu") (net 49))',
]
edge=s.find("  (gr_rect "); assert edge>0; s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Replaced K12 and added K14; K11/K13 unchanged")
