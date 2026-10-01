#!/usr/bin/env python3
"""Temporary DRC candidate: route only RELAY14_COIL_LOW (U2.13 -> K14.5).

The official PCB remains untouched. Promote this route only after the candidate
has zero error-severity DRC violations and reduces the unconnected count by one.
"""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
baseline_segments=s.count("(segment ")
assert baseline_segments >= 93, f"Unexpected routing regression: only {baseline_segments} baseline segments"
assert not any("(net 49)" in ln for ln in s.splitlines() if "(segment " in ln), "RELAY14_COIL_LOW is already routed in baseline"
print(f"Baseline segments: {baseline_segments}")

# U2 pad15 = (145.16,99.62)
# K12 pad5 with footprint rotation 90 deg = (247.62,115.00)
# K13 uses a via-free B.Cu escape from the THT U2 pad, avoiding K11/K12 F.Cu corridors.
parts=[
'  (segment (start 145.16 104.70) (end 140.0 105.5) (width 0.3) (layer "F.Cu") (net 49))',
'  (segment (start 140.0 105.5) (end 140.0 119.5) (width 0.3) (layer "F.Cu") (net 49))',
'  (segment (start 140.0 119.5) (end 178.0 119.5) (width 0.3) (layer "F.Cu") (net 49))',
'  (via (at 178.0 119.5) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 49))',
'  (segment (start 178.0 119.5) (end 184.0 119.5) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 184.0 119.5) (end 184.0 133.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (via (at 184.0 133.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 49))',
'  (segment (start 184.0 133.0) (end 184.0 137.0) (width 0.3) (layer "F.Cu") (net 49))',
'  (via (at 184.0 137.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 49))',
'  (segment (start 184.0 137.0) (end 184.0 142.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 184.0 142.0) (end 247.62 142.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 247.62 142.0) (end 247.62 115.0) (width 0.3) (layer "B.Cu") (net 49))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s,encoding="utf-8")
print("Added RELAY14_COIL_LOW candidate: U2.13 -> K14.5")
