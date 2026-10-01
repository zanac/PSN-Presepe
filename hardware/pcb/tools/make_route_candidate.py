#!/usr/bin/env python3
"""Create temporary WS2811 data routing candidate from promoted low-risk routes."""
from pathlib import Path
import sys

src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") >= 47, "Expected promoted buttons + OLED + A0 baseline"

# WS2811 data only; no +12/GND routing in this experiment.
# Mega D5=(73.72,43.74) -> STELLE DATA pad3=(185.08,184)
# Mega D8=(78.8,43.74) -> CASETTE DATA pad3=(203.08,184)
# Escape above digital header, then use separate layers/corridors.
routes={
  6:("F.Cu",[(73.72,43.74),(73.72,27),(138,27),(138,172),(185.08,172),(185.08,184)]),
  7:("B.Cu",[(78.8,43.74),(78.8,24),(141,24),(141,175),(203.08,175),(203.08,184)]),
}
parts=[]
for net,(layer,pts) in routes.items():
    for a,b in zip(pts,pts[1:]):
        parts.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.3) (layer "{layer}") (net {net}))')
edge=s.find("  (gr_rect ")
assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s,encoding="utf-8")
print(f"Wrote {dst} with {len(parts)} additional WS2811 data segments")
