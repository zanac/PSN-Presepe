#!/usr/bin/env python3
"""Temporary DRC candidate: route only RELAY11_COIL_LOW (U2.16 -> K11.5).

The official PCB remains untouched. Promote this route only after the candidate
has zero error-severity DRC violations and reduces the unconnected count by one.
"""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
baseline_segments=s.count("(segment ")
assert baseline_segments >= 93, f"Unexpected routing regression: only {baseline_segments} baseline segments"
assert not any("(net 46)" in ln for ln in s.splitlines() if "(segment " in ln), "RELAY11_COIL_LOW is already routed in baseline"
print(f"Baseline segments: {baseline_segments}")

# U2 pad16 = (145.16,97.08)
# K11 pad5 with footprint rotation 90 deg = (193.62,115.00)
# Avoid existing x=128.5 F.Cu and x=130.5 B.Cu backbones: escape right of U2/K9, drop on B.Cu at x=152, then use y=132 below relay row.
parts=[
'  (segment (start 145.16 97.08) (end 150.5 97.08) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 150.5 97.08) (end 152.0 99.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (via (at 152.0 99.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 46))',
'  (segment (start 152.0 99.0) (end 152.0 132.0) (width 0.3) (layer "B.Cu") (net 46))',
'  (segment (start 152.0 132.0) (end 193.62 132.0) (width 0.3) (layer "B.Cu") (net 46))',
'  (segment (start 193.62 132.0) (end 193.62 115.0) (width 0.3) (layer "B.Cu") (net 46))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s,encoding="utf-8")
print("Added RELAY11_COIL_LOW candidate: U2.16 -> K11.5")
