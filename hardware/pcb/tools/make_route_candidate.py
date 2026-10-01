#!/usr/bin/env python3
"""Temporary DRC candidate: D27_RELAY3 right-side fanout."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 22)" in ln for ln in s.splitlines() if "(segment " in ln or "(via " in ln)
parts=[
'  (segment (start 124.52 48.82) (end 126.0 51.36) (width 0.3) (layer "B.Cu") (net 22))',
'  (segment (start 126.0 51.36) (end 132.5 51.36) (width 0.3) (layer "B.Cu") (net 22))',
'  (via (at 132.5 51.36) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 22))',
'  (segment (start 132.5 51.36) (end 134.5 53.5) (width 0.3) (layer "F.Cu") (net 22))',
'  (segment (start 134.5 53.5) (end 134.5 67.08) (width 0.3) (layer "F.Cu") (net 22))',
'  (segment (start 134.5 67.08) (end 135.0 67.08) (width 0.3) (layer "F.Cu") (net 22))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+chr(10).join(parts)+chr(10)+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added D27 right-side candidate")
