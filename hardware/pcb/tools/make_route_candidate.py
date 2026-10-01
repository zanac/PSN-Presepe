#!/usr/bin/env python3
"""Temporary DRC candidate: K15/net50 coil-low route."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 50)" in ln for ln in s.splitlines() if "(segment " in ln)
parts=[
# U2.12 -> K15.5, B.Cu fanout then lower backbone below K14.
'  (segment (start 145.16 107.24) (end 141.5 109.0) (width 0.3) (layer "B.Cu") (net 50))',
'  (segment (start 141.5 109.0) (end 141.5 154.0) (width 0.3) (layer "B.Cu") (net 50))',
'  (segment (start 141.5 154.0) (end 265.62 154.0) (width 0.3) (layer "B.Cu") (net 50))',
'  (segment (start 265.62 154.0) (end 265.62 115.0) (width 0.3) (layer "B.Cu") (net 50))',
]
edge=s.find("  (gr_rect "); assert edge>0; s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added K15/net50 candidate")
