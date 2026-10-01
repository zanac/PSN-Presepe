#!/usr/bin/env python3
"""Candidate: repack D22_START away from MCU->ULN fanout corridor."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
old=[ln for ln in s.splitlines() if "(net 16)" in ln and "(segment " in ln]
assert old
s="\n".join(ln for ln in s.splitlines() if not ("(net 16)" in ln and ("(segment " in ln or "(via " in ln)))+"\n"
parts=[
'  (segment (start 121.98 43.74) (end 113.0 43.74) (width 0.3) (layer "F.Cu") (net 16))',
'  (segment (start 113.0 43.74) (end 108.0 48.0) (width 0.3) (layer "F.Cu") (net 16))',
'  (segment (start 108.0 48.0) (end 108.0 174.0) (width 0.3) (layer "F.Cu") (net 16))',
'  (segment (start 108.0 174.0) (end 65.0 174.0) (width 0.3) (layer "F.Cu") (net 16))',
'  (segment (start 65.0 174.0) (end 65.0 184.0) (width 0.3) (layer "F.Cu") (net 16))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+chr(10).join(parts)+chr(10)+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Repacked D22_START candidate")
