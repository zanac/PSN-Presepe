#!/usr/bin/env python3
"""Create a temporary low-risk routing candidate for KiCad DRC.

Never overwrites the source PCB. This first experiment routes only D22/D23/D24
on B.Cu so the fabrication source remains intentionally unrouted.
"""
from pathlib import Path
import sys

src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") == 0

# Absolute endpoints:
# MCU1 D22=(121.98,43.74), D23=(124.52,43.74), D24=(121.98,46.28)
# J_START=(65,184), J_NEXT=(78,184), J_TEST=(91,184)
routes={
  16:[(121.98,43.74),(126,47),(126,176),(118,184),(65,184)],
  17:[(124.52,43.74),(128,47),(128,178),(122,184),(78,184)],
  18:[(121.98,46.28),(130,50),(130,180),(126,184),(91,184)],
}
parts=[]
for net,pts in routes.items():
    for a,b in zip(pts,pts[1:]):
        parts.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.3) (layer "B.Cu") (net {net}))')
insert="\n".join(parts)+"\n"
edge=s.find("  (gr_rect ")
assert edge>0
s=s[:edge]+insert+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s,encoding="utf-8")
print(f"Wrote {dst} with {len(parts)} B.Cu segments")
