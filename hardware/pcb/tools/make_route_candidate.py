#!/usr/bin/env python3
"""Candidate: local D27 escape repack + D29 outer-right route."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
old22=[
'  (segment (start 124.52 48.82) (end 127.0 51.5) (width 0.3) (layer "F.Cu") (net 22))',
'  (via (at 127.0 51.5) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 22))',
'  (segment (start 127.0 51.5) (end 126.0 52.5) (width 0.3) (layer "B.Cu") (net 22))',
]
for x in old22:
    assert s.count(x)==1, x
    s=s.replace(x,"",1)
assert not any("(net 24)" in ln for ln in s.splitlines() if "(segment " in ln or "(via " in ln)
parts=[
'  (segment (start 124.52 48.82) (end 127.0 53.0) (width 0.3) (layer "F.Cu") (net 22))',
'  (via (at 127.0 53.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 22))',
'  (segment (start 127.0 53.0) (end 126.0 54.0) (width 0.3) (layer "B.Cu") (net 22))',
'  (segment (start 126.0 54.0) (end 126.0 61.5) (width 0.3) (layer "B.Cu") (net 22))',
'  (segment (start 124.52 51.36) (end 129.5 51.36) (width 0.3) (layer "B.Cu") (net 24))',
'  (via (at 129.5 51.36) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 24))',
'  (segment (start 129.5 51.36) (end 143.0 53.0) (width 0.3) (layer "F.Cu") (net 24))',
'  (segment (start 143.0 53.0) (end 143.0 72.16) (width 0.3) (layer "F.Cu") (net 24))',
'  (via (at 143.0 72.16) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 24))',
'  (segment (start 143.0 72.16) (end 135.0 72.16) (width 0.3) (layer "B.Cu") (net 24))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+chr(10).join(parts)+chr(10)+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added coordinated D27/D29 candidate")
