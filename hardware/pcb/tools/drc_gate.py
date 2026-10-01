#!/usr/bin/env python3
from pathlib import Path
import argparse,re
ap=argparse.ArgumentParser()
ap.add_argument("report"); ap.add_argument("--allow-unconnected",type=int,default=0)
a=ap.parse_args()
s=Path(a.report).read_text(encoding="utf-8")
cats={}
for k in re.findall(r'^\[([^\]]+)\]:',s,re.M): cats[k]=cats.get(k,0)+1
viol={k:v for k,v in cats.items() if k!="unconnected_items"}
unc=cats.get("unconnected_items",0)
print(f"Error-severity DRC violations: {viol or 'none'}")
print(f"Unconnected-item records: {unc} (allowed <= {a.allow_unconnected})")
if viol: raise SystemExit(2)
if unc>a.allow_unconnected: raise SystemExit(5)
