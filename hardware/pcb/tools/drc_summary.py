#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import re, sys

p=Path(sys.argv[1])
s=p.read_text(encoding="utf-8")
cats=Counter(re.findall(r'^\[([^\]]+)\]:',s,re.M))
drc=sum(v for k,v in cats.items() if k!="unconnected_items")
unc=cats.get("unconnected_items",0)
print(f"DRC categories: {dict(sorted(cats.items()))}")
print(f"Non-routing violations: {drc}")
print(f"Unconnected-item records: {unc}")
critical={k:v for k,v in cats.items() if k in {"shorting_items","clearance","hole_clearance","drill_out_of_range","solder_mask_bridge","board_edge_clearance"}}
print(f"Critical geometry/electrical categories: {critical or 'none'}")
