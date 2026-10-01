#!/usr/bin/env python3
"""Candidate: coordinated D26 repack + D27 route."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
old21=[
'  (segment (start 121.98 48.82) (end 123.2 50.09) (width 0.3) (layer "B.Cu") (net 21))',
'  (segment (start 123.2 50.09) (end 129.5 50.09) (width 0.3) (layer "B.Cu") (net 21))',
'  (via (at 129.5 50.09) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 21))',
'  (segment (start 129.5 50.09) (end 131.5 52.0) (width 0.3) (layer "F.Cu") (net 21))',
'  (segment (start 131.5 52.0) (end 131.5 64.54) (width 0.3) (layer "F.Cu") (net 21))',
'  (segment (start 131.5 64.54) (end 135.0 64.54) (width 0.3) (layer "F.Cu") (net 21))',
]
for x in old21:
    assert s.count(x)==1, x
    s=s.replace(x,"",1)
assert not any("(net 22)" in ln for ln in s.splitlines() if "(segment " in ln or "(via " in ln)
parts=[
'  (segment (start 121.98 48.82) (end 123.2 50.09) (width 0.3) (layer "B.Cu") (net 21))',
'  (segment (start 123.2 50.09) (end 129.5 50.09) (width 0.3) (layer "B.Cu") (net 21))',
'  (via (at 129.5 50.09) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 21))',
'  (segment (start 129.5 50.09) (end 138.5 52.0) (width 0.3) (layer "F.Cu") (net 21))',
'  (segment (start 138.5 52.0) (end 138.5 61.5) (width 0.3) (layer "F.Cu") (net 21))',
'  (segment (start 138.5 61.5) (end 135.0 64.54) (width 0.3) (layer "F.Cu") (net 21))',
'  (segment (start 124.52 48.82) (end 126.0 51.36) (width 0.3) (layer "B.Cu") (net 22))',
'  (segment (start 126.0 51.36) (end 129.5 53.5) (width 0.3) (layer "B.Cu") (net 22))',
'  (via (at 129.5 53.5) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 22))',
'  (segment (start 129.5 53.5) (end 131.5 56.0) (width 0.3) (layer "F.Cu") (net 22))',
'  (segment (start 131.5 56.0) (end 131.5 67.08) (width 0.3) (layer "F.Cu") (net 22))',
'  (segment (start 131.5 67.08) (end 135.0 67.08) (width 0.3) (layer "F.Cu") (net 22))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+chr(10).join(parts)+chr(10)+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added coordinated D26/D27 candidate")
