#!/usr/bin/env python3
from pathlib import Path
import re, sys

s=Path(sys.argv[1]).read_text(encoding="utf-8")
cats={}
for k in re.findall(r'^\[([^\]]+)\]:',s,re.M):
    cats[k]=cats.get(k,0)+1
viol={k:v for k,v in cats.items() if k!="unconnected_items"}
unc=cats.get("unconnected_items",0)
print(f"Error-severity DRC violations: {viol or 'none'}")
print(f"Unconnected-item records: {unc}")
if viol:
    raise SystemExit(2)
if unc:
    raise SystemExit(5)
