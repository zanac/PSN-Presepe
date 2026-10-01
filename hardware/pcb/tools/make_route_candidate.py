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
  # Escape the dense Mega header before running vertically.
  # x=130.5 passes between the capacitor pads and stays left of the ULN rows.
  # x=139 is the reviewed gap between ULN and relay footprints.
  16:("F.Cu",[(121.98,43.74),(121.98,40),(139,40),(139,174),(65,174),(65,184)]),
  17:("B.Cu",[(124.52,43.74),(130.5,43.74),(130.5,177),(78,177),(78,184)]),
  18:("F.Cu",[(121.98,46.28),(119,49),(119,52),(130.5,52),(130.5,180),(91,180),(91,184)]),
}
parts=[]
for net,(layer,pts) in routes.items():
    for a,b in zip(pts,pts[1:]):
        parts.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.3) (layer "{layer}") (net {net}))')
insert="\n".join(parts)+"\n"
edge=s.find("  (gr_rect ")
assert edge>0
s=s[:edge]+insert+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s,encoding="utf-8")
print(f"Wrote {dst} with {len(parts)} B.Cu segments")
