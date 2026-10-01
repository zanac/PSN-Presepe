#!/usr/bin/env python3
"""Create a temporary OLED I2C routing candidate from the partially routed source."""
from pathlib import Path
import sys

src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") > 0, "Expected promoted button routing in source"

# OLED I2C experiment.
# Escape left from the Mega, descend through the otherwise quiet left corridor,
# then approach the bottom-edge OLED terminal. Separate layers minimize mutual
# crossings; KiCad DRC remains authoritative.
routes={
  14:("F.Cu",[(111.82,41.20),(108,37),(24,37),(24,176),(52.16,176),(52.16,184)]),
  15:("B.Cu",[(114.36,41.20),(110,34),(21.5,34),(21.5,179),(57.24,179),(57.24,184)]),
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
print(f"Wrote {dst} with {len(parts)} additional OLED I2C segments")
