#!/usr/bin/env python3
"""Temporary DRC candidate: route only RELAY10_COIL_LOW (U2.17 -> K10.5).

The official PCB remains untouched. Promote this route only after the candidate
has zero error-severity DRC violations and reduces the unconnected count by one.
"""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
baseline_segments=s.count("(segment ")
assert baseline_segments >= 93, f"Unexpected routing regression: only {baseline_segments} baseline segments"
assert not any("(net 45)" in ln for ln in s.splitlines() if "(segment " in ln), "RELAY10_COIL_LOW is already routed in baseline"
print(f"Baseline segments: {baseline_segments}")

# U2 pad17 = (145.16,94.54)
# K10 pad5 with footprint rotation 90 deg = (175.62,115.00)
# Route around the left/bottom side of K9 to avoid its contact pads and the K9 coil trace.
pts=[(145.16,94.54),(142.0,96.5),(142.0,118.0),(175.62,118.0),(175.62,115.0)]
parts=[]
for a,b in zip(pts,pts[1:]):
    parts.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.3) (layer "F.Cu") (net 45))')
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s,encoding="utf-8")
print("Added RELAY10_COIL_LOW candidate: U2.17 -> K10.5")
