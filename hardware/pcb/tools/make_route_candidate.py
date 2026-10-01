#!/usr/bin/env python3
"""Temporary DRC candidate: route only RELAY6_COIL_LOW (U1.13 -> K6.5).

The official PCB remains untouched. Promote this route only after the candidate
has zero error-severity DRC violations and reduces the unconnected count by one.
"""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
baseline_segments=s.count("(segment ")
assert baseline_segments >= 93, f"Unexpected routing regression: only {baseline_segments} baseline segments"
assert not any("(net 41)" in ln for ln in s.splitlines() if "(segment " in ln), "RELAY6_COIL_LOW is already routed in baseline"
print(f"Baseline segments: {baseline_segments}")

# U1 pad13 = (145.16,74.70)
# K6 pad5 with footprint rotation 90 deg = (247.62,60.00)
# Keep this corridor below K5's y=74 route.
pts=[(145.16,74.70),(148.0,76.5),(245.0,76.5),(247.62,64.0),(247.62,60.0)]
parts=[]
for a,b in zip(pts,pts[1:]):
    parts.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.3) (layer "F.Cu") (net 41))')
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s,encoding="utf-8")
print("Added RELAY6_COIL_LOW candidate: U1.13 -> K6.5")
