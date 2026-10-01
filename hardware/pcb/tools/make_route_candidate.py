#!/usr/bin/env python3
"""Temporary DRC candidate: K15 route right of K14, local bridge across K14 backbone."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); s=src.read_text(encoding="utf-8")
# Candidate-only local K12 bridge around K15 crossing near y=108.
s=s.replace('  (segment (start 147.0 101.5) (end 147.0 132.0) (width 0.3) (layer "B.Cu") (net 47))', '\\n'.join([
'  (segment (start 147.0 101.5) (end 147.0 106.0) (width 0.3) (layer "B.Cu") (net 47))',
'  (via (at 147.0 106.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 47))',
'  (segment (start 147.0 106.0) (end 147.0 111.0) (width 0.3) (layer "F.Cu") (net 47))',
'  (via (at 147.0 111.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 47))',
'  (segment (start 147.0 111.0) (end 147.0 132.0) (width 0.3) (layer "B.Cu") (net 47))']))
assert not any("(net 50)" in ln for ln in s.splitlines() if "(segment " in ln)
parts=[
'  (segment (start 145.16 107.24) (end 148.0 109.0) (width 0.3) (layer "B.Cu") (net 50))',
'  (segment (start 148.0 109.0) (end 148.0 140.0) (width 0.3) (layer "B.Cu") (net 50))',
'  (via (at 148.0 140.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 50))',
'  (segment (start 148.0 140.0) (end 148.0 144.0) (width 0.3) (layer "F.Cu") (net 50))',
'  (via (at 148.0 144.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 50))',
'  (segment (start 148.0 144.0) (end 148.0 154.0) (width 0.3) (layer "B.Cu") (net 50))',
'  (segment (start 148.0 154.0) (end 265.62 154.0) (width 0.3) (layer "B.Cu") (net 50))',
'  (segment (start 265.62 154.0) (end 265.62 115.0) (width 0.3) (layer "B.Cu") (net 50))',
]
edge=s.find("  (gr_rect "); assert edge>0; s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added K15 right-side local-bridge candidate")
