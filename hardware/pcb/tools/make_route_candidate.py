#!/usr/bin/env python3
"""Create temporary A0 + buzzer routing candidate from promoted button/OLED board."""
from pathlib import Path
import sys

src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") >= 42, "Expected promoted button + OLED routing"

# A0: Mega A0=(78.8,89.46), RV1 wiper=(50.5,145)
# D6: Mega D6=(76.26,41.2), BZ1 pad1=(48,156)
# Use opposite layers and left-side corridors; KiCad DRC is authoritative.
routes={
  19:("F.Cu",[(78.8,89.46),(62,89.46),(62,140),(50.5,140),(50.5,145)]),
  62:("B.Cu",[(76.26,41.2),(60,41.2),(60,136),(45,136),(45,153),(48,156)]),
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
