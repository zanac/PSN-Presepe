#!/usr/bin/env python3
"""Create temporary A0 + buzzer routing candidate from promoted button/OLED board."""
from pathlib import Path
import sys

src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") == 42, "Expected clean promoted button + OLED baseline"

# Escape perpendicular to Mega header rows before turning into left corridors.
# A0=(78.8,89.46) -> below analog header, then left/down to RV1 wiper=(50.5,145)
# D6=(76.26,41.2) -> above digital header, then left/down to BZ1 pad1=(48,156)
routes={
  19:("F.Cu",[(78.8,89.46),(78.8,96),(64,96),(64,139),(50.5,139),(50.5,145)]),
  62:("B.Cu",[(76.26,41.2),(76.26,31),(27,31),(27,150),(42,150),(48,156)]),
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
print(f"Wrote {dst} with {len(parts)} additional A0/buzzer segments")
