#!/usr/bin/env python3
"""Temporary DRC candidate: D28 below-header fanout."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 23)" in ln for ln in s.splitlines() if "(segment " in ln or "(via " in ln)
parts=[
'  (segment (start 121.98 51.36) (end 120.0 52.63) (width 0.3) (layer "F.Cu") (net 23))',
'  (via (at 120.0 52.63) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 23))',
'  (segment (start 120.0 52.63) (end 120.0 69.0) (width 0.3) (layer "B.Cu") (net 23))',
'  (segment (start 120.0 69.0) (end 129.5 69.0) (width 0.3) (layer "B.Cu") (net 23))',
'  (via (at 129.5 69.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 23))',
'  (segment (start 129.5 69.0) (end 130.5 69.62) (width 0.3) (layer "F.Cu") (net 23))',
'  (segment (start 130.5 69.62) (end 135.0 69.62) (width 0.3) (layer "F.Cu") (net 23))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+chr(10).join(parts)+chr(10)+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added D28 below-header candidate")
