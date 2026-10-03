#!/usr/bin/env python3
from pathlib import Path
import re,sys

s=Path(sys.argv[1]).read_text(encoding="utf-8")
wanted={"shorting_items","tracks_crossing","clearance","hole_clearance","solder_mask_bridge"}
blocks=re.split(r'(?=^\[[^\]]+\]:)',s,flags=re.M)
found=0
for b in blocks:
    m=re.match(r'^\[([^\]]+)\]:',b)
    if m and m.group(1) in wanted:
        print(b.rstrip())
        print("---")
        found+=1
print(f"Critical/detail blocks printed: {found}")
