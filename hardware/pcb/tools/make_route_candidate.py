#!/usr/bin/env python3
"""Temporary DRC candidate: close D22_START from existing track end to J_START."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 16)" in ln and "(start 65 174)" in ln and "(end 65 194)" in ln for ln in s.splitlines() if "(segment " in ln)
parts=[
'  (segment (start 65.0 174.0) (end 65.0 194.0) (width 0.3) (layer "F.Cu") (net 16))',
]
# KiCad accepts top-level segment/via objects anywhere inside the board
# S-expression. Insert immediately before the board's final closing paren so
# candidate generation is independent of the Edge.Cuts representation.
edge=s.rfind(")")
assert edge>0, "Malformed board: final closing parenthesis not found"
s=s[:edge]+chr(10)+chr(10).join(parts)+chr(10)+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added D22_START candidate: (65,174) -> J_START (65,194)")
