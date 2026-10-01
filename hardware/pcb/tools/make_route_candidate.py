#!/usr/bin/env python3
"""Temporary DRC candidate: K16 coil-low route."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 51)" in ln for ln in s.splitlines() if "(segment " in ln)
parts=[
'  (segment (start 145.16 109.78) (end 141.0 112.0) (width 0.3) (layer "F.Cu") (net 51))',
'  (segment (start 141.0 112.0) (end 141.0 120.0) (width 0.3) (layer "F.Cu") (net 51))',
'  (via (at 141.0 120.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 51))',
'  (segment (start 141.0 120.0) (end 141.0 158.0) (width 0.3) (layer "B.Cu") (net 51))',
'  (segment (start 141.0 158.0) (end 283.62 158.0) (width 0.3) (layer "B.Cu") (net 51))',
'  (segment (start 283.62 158.0) (end 283.62 115.0) (width 0.3) (layer "B.Cu") (net 51))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+chr(10).join(parts)+chr(10)+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added K16 lower-backbone candidate")
