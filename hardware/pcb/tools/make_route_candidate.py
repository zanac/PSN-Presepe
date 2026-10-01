#!/usr/bin/env python3
"""Create a temporary next-routing candidate from the partially routed source PCB."""
from pathlib import Path
import sys

src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") > 0, "Expected promoted D22/D23/D24 routing in source"

# Second low-risk experiment: OLED I2C only.
# MCU1: D20=(111.82,41.20), D21=(114.36,41.20)
# OLED: SDA pad3=(52.16,184), SCL pad4=(57.24,184)
routes={
  14:[(111.82,41.2),(105,41.2),(105,158),(70,158),(70,180),(52.16,180),(52.16,184)],
  15:[(114.36,41.2),(108,41.2),(108,161),(73,161),(73,181),(57.24,181),(57.24,184)],
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
print(f"Wrote {dst} with {len(parts)} additional OLED routing segments")
