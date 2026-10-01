#!/usr/bin/env python3
from pathlib import Path
import os,re,sys

def count(path):
    s=Path(path).read_text(encoding="utf-8")
    m=re.search(r'Found\s+(\d+)\s+unconnected items',s)
    if m:return int(m.group(1))
    return len(re.findall(r'^\[unconnected_items\]:',s,re.M))

base=count(sys.argv[1]); cand=count(sys.argv[2])
print(f"Baseline unconnected: {base}")
print(f"Candidate unconnected: {cand}")
print(f"Reduction: {base-cand}")
mode=os.environ.get("CANDIDATE_MODE","improve")
if mode=="baseline":
    if cand!=base:
        raise SystemExit(f"Baseline candidate changed connectivity: {base} -> {cand}")
elif cand>=base:
    raise SystemExit("Routing candidate did not reduce unconnected items")
