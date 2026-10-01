#!/usr/bin/env python3
"""Temporary DRC candidate: route only RELAY3_COIL_LOW (U1.16 -> K3.5)."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") == 81, "Expected promoted K1+K2 81-segment baseline"

# KiCad-verified Y-down geometry:
# U1 pad16 = (145.16,67.08)
# K3 pad5, footprint rotation 90 deg = (193.62,60.00)
# Keep a separate corridor from K2.
pts=[(145.16,67.08),(148.0,69.0),(191.0,69.0),(193.62,64.0),(193.62,60.0)]
parts=[]
for a,b in zip(pts,pts[1:]):
    parts.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.3) (layer "F.Cu") (net 38))')
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added RELAY3_COIL_LOW candidate")
