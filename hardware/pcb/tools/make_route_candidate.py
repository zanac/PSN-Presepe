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
# Fan the four signals to distinct x corridors on B.Cu.
routes={
  20:[(124.52,46.28),(128.0,49.0),(128.0,59.0),(131.0,62.0),(135.0,62.0)],
  21:[(121.98,48.82),(126.5,52.0),(126.5,61.0),(130.0,64.54),(135.0,64.54)],
  22:[(124.52,48.82),(129.5,53.0),(129.5,63.0),(133.0,66.5),(135.0,67.08)],
  23:[(121.98,51.36),(125.0,54.0),(125.0,65.0),(129.62,69.62),(135.0,69.62)],
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
print(f"Added {len(parts)} candidate segments for D25..D28")
