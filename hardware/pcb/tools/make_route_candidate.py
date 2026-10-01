#!/usr/bin/env python3
"""Temporary DRC candidate: D29_RELAY5 right escape + staggered wall crossing."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 24)" in ln for ln in s.splitlines() if "(segment " in ln or "(via " in ln)
parts=[
'  (segment (start 124.52 51.36) (end 127.5 54.0) (width 0.3) (layer "F.Cu") (net 24))',
'  (segment (start 127.5 54.0) (end 127.5 90.0) (width 0.3) (layer "F.Cu") (net 24))',
'  (segment (start 127.5 90.0) (end 127.0 94.0) (width 0.3) (layer "F.Cu") (net 24))',
'  (via (at 127.0 94.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 24))',
'  (segment (start 127.0 94.0) (end 129.5 94.0) (width 0.3) (layer "B.Cu") (net 24))',
'  (via (at 129.5 94.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 24))',
'  (segment (start 129.5 94.0) (end 132.0 96.0) (width 0.3) (layer "F.Cu") (net 24))',
'  (segment (start 132.0 96.0) (end 142.0 96.0) (width 0.3) (layer "F.Cu") (net 24))',
'  (segment (start 142.0 96.0) (end 142.0 75.0) (width 0.3) (layer "F.Cu") (net 24))',
'  (segment (start 142.0 75.0) (end 135.0 72.16) (width 0.3) (layer "F.Cu") (net 24))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+chr(10).join(parts)+chr(10)+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added D29 right-escape candidate")
