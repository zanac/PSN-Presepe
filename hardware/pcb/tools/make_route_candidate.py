#!/usr/bin/env python3
"""Create temporary WS2811 DATA routing candidate from promoted logic baseline."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") == 47, "Expected clean promoted buttons + OLED + A0 baseline"

# Escape Mega to the left/central SELV area, descend west of the driver bank,
# then cross along the quiet bottom corridor immediately above the terminals.
routes={
  12:("B.Cu",[(78.8,41.2),(82,47),(122,47),(122,169),(125,172),(190.16,172),(190.16,184)]),
  13:("F.Cu",[(69.656,41.2),(69.656,101),(124,101),(124,166),(128,170),(208.16,170),(208.16,184)]),
}
parts=[]
for net,(layer,pts) in routes.items():
    for a,b in zip(pts,pts[1:]):
        parts.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.3) (layer "{layer}") (net {net}))')
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print(f"Wrote {dst} with {len(parts)} additional WS2811 DATA segments")
