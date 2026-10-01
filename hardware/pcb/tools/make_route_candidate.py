#!/usr/bin/env python3
"""Temporary DRC candidate: route only RELAY12_COIL_LOW (U2.15 -> K12.5).

The official PCB remains untouched. Promote this route only after the candidate
has zero error-severity DRC violations and reduces the unconnected count by one.
"""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
baseline_segments=s.count("(segment ")
assert baseline_segments >= 93, f"Unexpected routing regression: only {baseline_segments} baseline segments"
assert not any("(net 47)" in ln for ln in s.splitlines() if "(segment " in ln), "RELAY12_COIL_LOW is already routed in baseline"
print(f"Baseline segments: {baseline_segments}")

# U2 pad15 = (145.16,99.62)
# K12 pad5 with footprint rotation 90 deg = (211.62,115.00)
# K12 uses a via-free B.Cu escape from the THT U2 pad, avoiding K10/K11 F.Cu corridors.
parts=[
'  (segment (start 145.16 99.62) (end 147.0 101.5) (width 0.3) (layer "B.Cu") (net 47))',
'  (segment (start 147.0 101.5) (end 147.0 136.0) (width 0.3) (layer "B.Cu") (net 47))',
'  (segment (start 147.0 136.0) (end 211.62 136.0) (width 0.3) (layer "B.Cu") (net 47))',
'  (segment (start 211.62 136.0) (end 211.62 115.0) (width 0.3) (layer "B.Cu") (net 47))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s,encoding="utf-8")
print("Added RELAY12_COIL_LOW candidate: U2.15 -> K12.5")
