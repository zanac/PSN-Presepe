#!/usr/bin/env python3
"""Create temporary A0 + buzzer routing candidate from promoted button/OLED board."""
from pathlib import Path
import sys

src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") == 42, "Expected clean promoted button + OLED baseline"

# Escape perpendicular to Mega header rows before turning into left corridors.
# A0=(78.8,89.46) -> below analog header, then left/down to RV1 wiper=(50.5,145)
# D6=(76.26,41.2) -> above digital header on F.Cu, then left/down to BZ1 pad1=(48,156)
routes={
  19:("F.Cu",[(78.8,89.46),(78.8,96),(64,96),(64,139),(50.5,139),(50.5,145)]),
}
# D6: escape the Mega on F.Cu, cross below the I2C trunks, then change to
# B.Cu for the final local approach to the buzzer.
d6_parts=[
  ("F.Cu",[(76.26,41.2),(76.26,30),(118,30),(118,105),(32,105),(32,148)]),
  ("B.Cu",[(32,148),(42,148),(48,156)]),
]
via=(32,148,62)
parts=[]
for net,(layer,pts) in routes.items():
    for a,b in zip(pts,pts[1:]):
        parts.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.3) (layer "{layer}") (net {net}))')
for layer,pts in d6_parts:
    for a,b in zip(pts,pts[1:]):
        parts.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.3) (layer "{layer}") (net 62))')
parts.append(f'  (via (at {via[0]} {via[1]}) (size 1.0) (drill 0.5) (layers "F.Cu" "B.Cu") (net {via[2]}))')
edge=s.find("  (gr_rect ")
assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s,encoding="utf-8")
print(f"Wrote {dst} with {len(parts)} additional A0/buzzer segments")
