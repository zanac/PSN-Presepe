#!/usr/bin/env python3
"""Temporary DRC candidate: route only RELAY2_COIL_LOW (U1.17 -> K2.5)."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") == 77, "Expected promoted 77-segment baseline"

# KiCad-verified Y-down geometry:
# U1 pad17 = (145.16,64.54)
# K2 pad5, footprint rotation 90 deg = (175.62,60.00)
# Keep above the K1 coil route corridor.
pts=[(145.16,64.54),(148.0,66.5),(173.0,66.5),(175.62,64.0),(175.62,60.0)]
parts=[]
for a,b in zip(pts,pts[1:]):
    parts.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.3) (layer "F.Cu") (net 37))')
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added RELAY2_COIL_LOW candidate")
