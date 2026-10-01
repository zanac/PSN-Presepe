#!/usr/bin/env python3
"""Temporary DRC candidate: route only RELAY1_COIL_LOW (U1.18 -> K1.5)."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") == 74, "Expected promoted 74-segment baseline"

# U1 pad18 = (145.16,62.00)
# K1 pad5 after KiCad 90-degree rotation = (157.62,60.00)
# Very short local connection, kept on F.Cu.
pts=[(145.16,62.0),(150.0,62.0),(153.0,60.0),(157.62,60.0)]
parts=[]
for a,b in zip(pts,pts[1:]):
    parts.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.3) (layer "F.Cu") (net 36))')
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Added RELAY1_COIL_LOW candidate")
