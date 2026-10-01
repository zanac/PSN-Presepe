#!/usr/bin/env python3
"""Temporary DRC candidate: D26_RELAY2 MCU1 -> U1 input 2."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 21)" in ln for ln in s.splitlines() if "(segment " in ln or "(via " in ln)
parts=[
'  (segment (start 121.98 48.82) (end 127.0 48.82) (width 0.3) (layer "B.Cu") (net 21))',
'  (segment (start 127.0 48.82) (end 127.0 52.5) (width 0.3) (layer "B.Cu") (net 21))',
'  (segment (start 127.0 52.5) (end 129.5 52.5) (width 0.3) (layer "B.Cu") (net 21))',
'  (via (at 129.5 52.5) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 21))',
'  (segment (start 129.5 52.5) (end 138.0 56.0) (width 0.3) (layer "F.Cu") (net 21))',
'  (segment (start 138.0 56.0) (end 138.0 61.0) (width 0.3) (layer "F.Cu") (net 21))',
'  (segment (start 138.0 61.0) (end 135.0 64.54) (width 0.3) (layer "F.Cu") (net 21))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+chr(10).join(parts)+chr(10)+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added D26_RELAY2 candidate")
