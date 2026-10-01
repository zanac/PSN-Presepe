#!/usr/bin/env python3
"""Temporary DRC candidate: K16 coil-low route."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 51)" in ln for ln in s.splitlines() if "(segment " in ln)
old46='  (segment (start 140.0 99.0) (end 140.0 134.5) (width 0.3) (layer "F.Cu") (net 46))'
assert s.count(old46)==1
s=s.replace(old46,chr(10).join([
'  (segment (start 140.0 99.0) (end 140.0 118.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 140.0 118.0) (end 137.0 120.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 137.0 120.0) (end 137.0 130.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 137.0 130.0) (end 140.0 132.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 140.0 132.0) (end 140.0 134.5) (width 0.3) (layer "F.Cu") (net 46))',
]))
old49start='  (segment (start 145.16 104.70) (end 143.5 106.0) (width 0.3) (layer "B.Cu") (net 49))'
assert s.count(old49start)==1
s=s.replace(old49start,'  (segment (start 145.16 104.70) (end 139.5 104.0) (width 0.3) (layer "B.Cu") (net 49))' )
old='  (segment (start 143.5 106.0) (end 143.5 142.0) (width 0.3) (layer "B.Cu") (net 49))'
assert s.count(old)==1
s=s.replace(old,chr(10).join([
'  (segment (start 139.5 104.0) (end 139.5 124.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (via (at 139.5 124.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 49))',
'  (segment (start 139.5 124.0) (end 143.5 124.0) (width 0.3) (layer "F.Cu") (net 49))',
'  (via (at 143.5 124.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 49))',
'  (segment (start 143.5 124.0) (end 143.5 142.0) (width 0.3) (layer "B.Cu") (net 49))',
]))
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
