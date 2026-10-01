#!/usr/bin/env python3
"""Temporary DRC candidate: K16 coil-low route."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 51)" in ln for ln in s.splitlines() if "(segment " in ln)
# Free the K16 escape by bridging K14 onto F.Cu; move K13's nearby F.Cu vertical to x=140.
old48=[
'  (segment (start 145.16 102.16) (end 143.0 103.5) (width 0.3) (layer "F.Cu") (net 48))',
'  (segment (start 143.0 103.5) (end 143.0 117.0) (width 0.3) (layer "F.Cu") (net 48))',
'  (segment (start 143.0 117.0) (end 170.0 117.0) (width 0.3) (layer "F.Cu") (net 48))',
]
for x in old48:
    assert s.count(x)==1
    s=s.replace(x,'')
new48=[
'  (segment (start 145.16 102.16) (end 140.0 103.5) (width 0.3) (layer "F.Cu") (net 48))',
'  (segment (start 140.0 103.5) (end 140.0 117.0) (width 0.3) (layer "F.Cu") (net 48))',
'  (segment (start 140.0 117.0) (end 170.0 117.0) (width 0.3) (layer "F.Cu") (net 48))',
]
old49='  (segment (start 143.5 106.0) (end 143.5 142.0) (width 0.3) (layer "B.Cu") (net 49))'
assert s.count(old49)==1
s=s.replace(old49,chr(10).join([
'  (segment (start 143.5 106.0) (end 143.5 108.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (via (at 143.5 108.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 49))',
'  (segment (start 143.5 108.0) (end 143.5 114.0) (width 0.3) (layer "F.Cu") (net 49))',
'  (via (at 143.5 114.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 49))',
'  (segment (start 143.5 114.0) (end 143.5 142.0) (width 0.3) (layer "B.Cu") (net 49))',
]))
edge0=s.find("  (gr_rect "); assert edge0>0
s=s[:edge0]+chr(10).join(new48)+chr(10)+s[edge0:]
parts=[
'  (segment (start 145.16 109.78) (end 141.0 112.0) (width 0.3) (layer "B.Cu") (net 51))',
'  (segment (start 141.0 112.0) (end 141.0 158.0) (width 0.3) (layer "B.Cu") (net 51))',
'  (segment (start 141.0 158.0) (end 283.62 158.0) (width 0.3) (layer "B.Cu") (net 51))',
'  (segment (start 283.62 158.0) (end 283.62 115.0) (width 0.3) (layer "B.Cu") (net 51))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+chr(10).join(parts)+chr(10)+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added K16 lower-backbone candidate")
