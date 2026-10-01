#!/usr/bin/env python3
"""Temporary DRC candidate: D40_RELAY16 MCU1 -> U2 input 8."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 35)" in ln for ln in s.splitlines() if "(segment " in ln or "(via " in ln)
parts=[
'  (segment (start 121.98 66.60) (end 126.0 70.0) (width 0.3) (layer "F.Cu") (net 35))',
'  (segment (start 126.0 70.0) (end 126.0 109.78) (width 0.3) (layer "F.Cu") (net 35))',
'  (segment (start 126.0 109.78) (end 135.0 109.78) (width 0.3) (layer "F.Cu") (net 35))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+chr(10).join(parts)+chr(10)+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added D40_RELAY16 candidate")
