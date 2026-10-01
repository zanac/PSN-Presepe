#!/usr/bin/env python3
"""Temporary DRC candidate: D29 inter-pad escape + y80 wall crossing."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 24)" in ln for ln in s.splitlines() if "(segment " in ln or "(via " in ln)
parts=[
'  (segment (start 124.52 51.36) (end 123.25 52.63) (width 0.3) (layer "B.Cu") (net 24))',
'  (segment (start 123.25 52.63) (end 118.5 52.63) (width 0.3) (layer "B.Cu") (net 24))',
'  (via (at 118.5 52.63) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 24))',
'  (segment (start 118.5 52.63) (end 113.09 54.5) (width 0.3) (layer "F.Cu") (net 24))',
'  (segment (start 113.09 54.5) (end 113.09 80.0) (width 0.3) (layer "F.Cu") (net 24))',
'  (via (at 113.09 80.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 24))',
'  (segment (start 113.09 80.0) (end 129.5 80.0) (width 0.3) (layer "B.Cu") (net 24))',
'  (via (at 129.5 80.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 24))',
'  (segment (start 129.5 80.0) (end 132.0 80.0) (width 0.3) (layer "F.Cu") (net 24))',
'  (segment (start 132.0 80.0) (end 132.0 72.16) (width 0.3) (layer "F.Cu") (net 24))',
'  (segment (start 132.0 72.16) (end 135.0 72.16) (width 0.3) (layer "F.Cu") (net 24))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+chr(10).join(parts)+chr(10)+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added D29 inter-pad y80 candidate")
