#!/usr/bin/env python3
"""Temporary DRC candidate: replace K11/net46 and add K14/net49."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 49)" in ln for ln in s.splitlines() if "(segment " in ln)
lines=s.splitlines(); lines=[ln for ln in lines if not (("(segment " in ln or "(via " in ln) and "(net 46)" in ln)]; s="\n".join(lines)+"\n"
parts=[
# K11 replacement: escape left, descend outside U2, backbone below all existing relay routes
'  (segment (start 145.16 97.08) (end 139.0 99.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 139.0 99.0) (end 139.0 146.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 139.0 146.0) (end 193.62 146.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 193.62 146.0) (end 193.62 115.0) (width 0.3) (layer "F.Cu") (net 46))',
# K14 uses the old K11 B.Cu lane and its own lower backbone
'  (segment (start 145.16 104.70) (end 143.5 106.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 143.5 106.0) (end 143.5 142.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 143.5 142.0) (end 247.62 142.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 247.62 142.0) (end 247.62 115.0) (width 0.3) (layer "B.Cu") (net 49))',
]
edge=s.find("  (gr_rect "); assert edge>0; s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Replaced K11 below existing routes and added K14")
