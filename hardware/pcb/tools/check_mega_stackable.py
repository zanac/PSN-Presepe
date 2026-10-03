#!/usr/bin/env python3
"""Fail if a component is placed in the Arduino Mega shield stacking envelope."""
import re
from pathlib import Path

pcb = Path("hardware/pcb/kicad/PSN-Presepe-Mega.kicad_pcb").read_text()
# MCU1 origin is fixed by the approved mechanical design.
origin = re.search(r'\(footprint "PSN_Presep_Custom:Arduino_Mega2560_R3_Shield"[\s\S]*?\(at ([0-9.]+) ([0-9.]+)[^)]*\)[\s\S]*?\(property "Reference" "MCU1"', pcb)
if not origin:
    raise SystemExit("MCU1 Mega shield footprint not found")
ox, oy = map(float, origin.groups())
# Mega R3 nominal outline: 101.6 x 53.34 mm; footprint extends in negative Y.
xmin, xmax = ox, ox + 101.6
ymin, ymax = oy - 53.34, oy

hits = []
pat = re.compile(r'\(footprint "([^"]+)"[\s\S]*?\(at ([0-9.]+) ([0-9.]+)[^)]*\)[\s\S]*?\(property "Reference" "([^"]+)"')
for m in pat.finditer(pcb):
    fp, xs, ys, ref = m.groups()
    if ref == "MCU1":
        continue
    x, y = float(xs), float(ys)
    if xmin <= x <= xmax and ymin <= y <= ymax:
        hits.append(f"{ref} ({fp}) at {x},{y}")

if hits:
    raise SystemExit("STACKING_ENVELOPE_BLOCKED: " + "; ".join(hits))
print(f"STACKING_ENVELOPE_CLEAR Mega={xmin:.2f}..{xmax:.2f} x {ymin:.2f}..{ymax:.2f}; use stackable/pass-through Mega R3 headers")
