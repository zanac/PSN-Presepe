#!/usr/bin/env python3
"""Temporary DRC candidate: D25_RELAY1 MCU1 -> U1 input 1."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 20)" in ln for ln in s.splitlines() if "(segment " in ln or "(via " in ln)
parts=[
'  (segment (start 124.52 46.28) (end 128.0 50.0) (width 0.3) (layer "B.Cu") (net 20))',
'  (segment (start 128.0 50.0) (end 128.0 58.0) (width 0.3) (layer "B.Cu") (net 20))',
'  (segment (start 128.0 58.0) (end 135.0 62.0) (width 0.3) (layer "B.Cu") (net 20))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+chr(10).join(parts)+chr(10)+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added D25_RELAY1 candidate")
