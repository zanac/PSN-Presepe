#!/usr/bin/env python3
"""Temporary DRC candidate: K14 only, short right escape with early layer transition."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
assert not any("(net 49)" in ln for ln in s.splitlines() if "(segment " in ln)
parts=[
'  (segment (start 145.16 104.70) (end 150.5 104.70) (width 0.3) (layer "F.Cu") (net 49))',
'  (via (at 150.5 104.70) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 49))',
'  (segment (start 150.5 104.70) (end 150.5 123.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 150.5 123.0) (end 184.0 123.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (via (at 184.0 123.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 49))',
'  (segment (start 184.0 123.0) (end 184.0 142.0) (width 0.3) (layer "F.Cu") (net 49))',
'  (segment (start 184.0 142.0) (end 247.62 142.0) (width 0.3) (layer "F.Cu") (net 49))',
'  (segment (start 247.62 142.0) (end 247.62 115.0) (width 0.3) (layer "F.Cu") (net 49))',
]
edge=s.find("  (gr_rect "); assert edge>0; s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added K14 short-right early-transition candidate")
