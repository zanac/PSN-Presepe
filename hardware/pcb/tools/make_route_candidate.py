#!/usr/bin/env python3
"""Create temporary local MOSFET gate-node routing candidate."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") == 47, "Expected promoted buttons + OLED + A0 baseline"

# GATE_Q1..Q9 are nets 63..71. For each channel:
# RG pad2 = (RG.x+10.16, RG.y), RPD pad1=(RPD.x,RPD.y), Q pad1=(Q.x,Q.y).
# Route a short local T-like connection on F.Cu, staying inside the thermal zone.
positions=[
 (63,58,132.5,58,137.5,70,135),
 (64,78,132.5,78,137.5,90,135),
 (65,98,132.5,98,137.5,110,135),
 (66,58,147.5,58,152.5,70,150),
 (67,78,147.5,78,152.5,90,150),
 (68,98,147.5,98,152.5,110,150),
 (69,58,162.5,58,167.5,70,165),
 (70,78,162.5,78,167.5,90,165),
 (71,98,162.5,98,167.5,110,165),
]
parts=[]
for net,rgx,rgy,rpx,rpy,qx,qy in positions:
    rg2=(rgx+10.16,rgy)
    junction=(rgx+10.16,qy)
    pts=[rg2,junction,(qx,qy)]
    for a,b in zip(pts,pts[1:]):
        parts.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.3) (layer "F.Cu") (net {net}))')
    parts.append(f'  (segment (start {rpx} {rpy}) (end {junction[0]} {junction[1]}) (width 0.3) (layer "F.Cu") (net {net}))')
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print(f"Wrote {dst} with {len(parts)} local MOSFET gate segments")
