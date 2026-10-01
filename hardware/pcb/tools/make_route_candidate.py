#!/usr/bin/env python3
"""Temporary DRC candidate: D27_RELAY3 MCU1 -> U1 input 3."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 22)" in ln for ln in s.splitlines() if "(segment " in ln or "(via " in ln)
parts=[
'  (segment (start 124.52 48.82) (end 126.0 51.36) (width 0.3) (layer "B.Cu") (net 22))',
'  (segment (start 126.0 51.36) (end 126.0 54.5) (width 0.3) (layer "B.Cu") (net 22))',
'  (segment (start 126.0 54.5) (end 129.5 54.5) (width 0.3) (layer "B.Cu") (net 22))',
'  (via (at 129.5 54.5) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 22))',
'  (segment (start 129.5 54.5) (end 133.0 58.5) (width 0.3) (layer "F.Cu") (net 22))',
'  (segment (start 133.0 58.5) (end 133.0 67.08) (width 0.3) (layer "F.Cu") (net 22))',
'  (segment (start 133.0 67.08) (end 135.0 67.08) (width 0.3) (layer "F.Cu") (net 22))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+chr(10).join(parts)+chr(10)+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added D27_RELAY3 candidate")
