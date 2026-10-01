#!/usr/bin/env python3
"""Temporary DRC candidate: add four local Mega -> U1 relay-control routes.

Never overwrites the production PCB.
"""
from pathlib import Path
import sys

src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") == 74, "Expected promoted 74-segment baseline"

# MCU absolute endpoints:
# D25 124.52,46.28 -> U1.1 135,62
# D26 121.98,48.82 -> U1.2 135,64.54
# D27 124.52,48.82 -> U1.3 135,67.08
# D28 121.98,51.36 -> U1.4 135,69.62
# Escape the dense Mega header horizontally to the right on F.Cu, then
# use B.Cu for the long approach to U1. Via positions are deliberately
# staggered and outside the Mega header field.
routes={
  20:((124.52,46.28),(130.0,46.28),[(130.0,46.28),(132.0,48.0),(132.0,60.0),(134.0,62.0),(135.0,62.0)]),
  21:((121.98,48.82),(130.0,48.82),[(130.0,48.82),(131.0,51.0),(131.0,62.0),(133.54,64.54),(135.0,64.54)]),
  22:((124.52,48.82),(133.0,48.82),[(133.0,48.82),(133.0,64.0),(135.0,67.08)]),
  23:((121.98,51.36),(128.0,51.36),[(128.0,51.36),(128.0,65.0),(132.62,69.62),(135.0,69.62)]),
}
parts=[]
vias=[]
for net,(start,via,pts) in routes.items():
    parts.append(f'  (segment (start {start[0]} {start[1]}) (end {via[0]} {via[1]}) (width 0.3) (layer "F.Cu") (net {net}))')
    vias.append(f'  (via (at {via[0]} {via[1]}) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net {net}))')
    for a,b in zip(pts,pts[1:]):
        parts.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.3) (layer "B.Cu") (net {net}))')
insert="\n".join(parts+vias)+"\n"
edge=s.find("  (gr_rect ")
assert edge>0
s=s[:edge]+insert+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s,encoding="utf-8")
print(f"Added {len(parts)} candidate segments + {len(vias)} vias for D25..D28")
