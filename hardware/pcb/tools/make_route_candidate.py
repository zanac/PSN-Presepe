#!/usr/bin/env python3
"""Create temporary WS2811 DATA routing candidate from promoted logic baseline."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") == 47, "Expected clean promoted buttons + OLED + A0 baseline"

# D5 Mega=(78.8,41.2) -> STELLE DATA=(190.16,184)
# D8 Mega=(69.656,41.2) -> CASETTE DATA=(208.16,184)
# Escape upward from the Mega header, then use separate SELV corridors east of
# the Mega but west of the relay bank.
routes={
  12:("F.Cu",[(78.8,41.2),(78.8,28),(132,28),(132,172),(190.16,172),(190.16,184)]),
  13:("B.Cu",[(69.656,41.2),(69.656,26),(136,26),(136,175),(208.16,175),(208.16,184)]),
}
parts=[]
for net,(layer,pts) in routes.items():
    for a,b in zip(pts,pts[1:]):
        parts.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.3) (layer "{layer}") (net {net}))')
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print(f"Wrote {dst} with {len(parts)} additional WS2811 DATA segments")
