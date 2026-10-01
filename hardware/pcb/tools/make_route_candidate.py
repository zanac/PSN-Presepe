#!/usr/bin/env python3
"""Temporary DRC candidate: route only RELAY9_COIL_LOW (U2.18 -> K9.5).

The official PCB remains untouched. Promote this route only after the candidate
has zero error-severity DRC violations and reduces the unconnected count by one.
"""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
baseline_segments=s.count("(segment ")
assert baseline_segments >= 93, f"Unexpected routing regression: only {baseline_segments} baseline segments"
assert not any("(net 44)" in ln for ln in s.splitlines() if "(segment " in ln), "RELAY9_COIL_LOW is already routed in baseline"
print(f"Baseline segments: {baseline_segments}")

# U2 pad18 = (145.16,92.00)
# K9 pad5 with footprint rotation 90 deg = (157.62,115.00)
# Short local corridor for the second ULN2803 relay bank.
pts=[(145.16,92.0),(147.5,94.0),(147.5,112.0),(157.62,112.0),(157.62,115.0)]
parts=[]
for a,b in zip(pts,pts[1:]):
    parts.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.3) (layer "F.Cu") (net 44))')
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s,encoding="utf-8")
print("Added RELAY9_COIL_LOW candidate: U2.18 -> K9.5")
