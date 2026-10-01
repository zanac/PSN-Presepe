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
  # Ordered trunks (START/NEXT/TEST left-to-right) avoid bottom fanout crossings.
  # D22 uses midpoint x=128.5 around C1 and jogs to x=130.5 around C2/C3.
  16:("F.Cu",[(121.98,43.74),(117,43.74),(117,38),(128.5,38),
               (128.5,52),(130.5,54),(130.5,58),(128.5,60),
               (128.5,82),(130.5,84),(130.5,88),(128.5,90),
               (128.5,174),(65,174),(65,184)]),
  # D23 uses x=130.5 except around shifted C1 where x=128.5 is the midpoint.
  17:("B.Cu",[(124.52,43.74),(130.5,43.74),(130.5,114),
               (128.5,116),(128.5,124),(130.5,126),
               (130.5,177),(78,177),(78,184)]),
  # D24 escapes through the gap left of the dense Mega D22..D53 columns,
  # crosses to the reviewed ULN/relay gap above the analog-header row.
  18:("F.Cu",[(121.98,46.28),(117,46.28),(117,84),(139,84),
               (139,180),(91,180),(91,184)]),
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
