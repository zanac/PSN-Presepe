#!/usr/bin/env python3
"""Temporary DRC candidate: D30 low-left template on clean D29 baseline."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 25)" in ln for ln in s.splitlines() if "(segment " in ln or "(via " in ln)
parts=[
'  (segment (start 121.98 53.9) (end 116.0 56.0) (width 0.3) (layer "B.Cu") (net 25))',
'  (segment (start 116.0 56.0) (end 108.0 58.0) (width 0.3) (layer "B.Cu") (net 25))',
'  (segment (start 108.0 58.0) (end 108.0 83.0) (width 0.3) (layer "B.Cu") (net 25))',
'  (segment (start 108.0 83.0) (end 126.0 83.0) (width 0.3) (layer "B.Cu") (net 25))',
'  (via (at 126.0 83.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 25))',
'  (segment (start 126.0 83.0) (end 129.5 83.0) (width 0.3) (layer "F.Cu") (net 25))',
'  (via (at 129.5 83.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 25))',
'  (segment (start 129.5 83.0) (end 133.0 83.0) (width 0.3) (layer "B.Cu") (net 25))',
'  (segment (start 133.0 83.0) (end 133.0 74.7) (width 0.3) (layer "B.Cu") (net 25))',
'  (segment (start 133.0 74.7) (end 135.0 74.7) (width 0.3) (layer "B.Cu") (net 25))',
]
# KiCad accepts top-level segment/via objects anywhere inside the board
# S-expression. Insert immediately before the board's final closing paren so
# candidate generation is independent of the Edge.Cuts representation.
edge=s.rfind(")")
assert edge>0, "Malformed board: final closing parenthesis not found"
s=s[:edge]+chr(10)+chr(10).join(parts)+chr(10)+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added D30 low-left candidate")
