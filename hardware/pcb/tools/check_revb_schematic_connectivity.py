#!/usr/bin/env python3
import sys,re
import pcbnew

pcb, sch = sys.argv[1], sys.argv[2]
b=pcbnew.LoadBoard(pcb)
expected=set()
for fp in b.GetFootprints():
    ref=fp.GetReference()
    if ref.startswith("H"): continue
    for p in fp.Pads():
        if p.GetNetname():
            expected.add((ref,p.GetNumber() or "NP",p.GetNetname()))
txt=open(sch,encoding="utf-8").read()
found=set(re.findall(r'PIN ([^ ]+) -> ([^"\r\n]+)',txt))
# Bind each PIN line to the nearest preceding component title.
actual=set()
cur=None
for line in txt.splitlines():
    m=re.search(r'\(text "([^ ]+)  ',line)
    if m: cur=m.group(1)
    m=re.search(r'\(text "PIN ([^ ]+) -> ([^"]+)"',line)
    if m and cur: actual.add((cur,m.group(1),m.group(2)))
missing=expected-actual; extra=actual-expected
print("SCHEMATIC_CONNECTIVITY_AUDIT expected=",len(expected),"actual=",len(actual),"missing=",len(missing),"extra=",len(extra))
for x in sorted(missing)[:20]: print("MISSING",x)
for x in sorted(extra)[:20]: print("EXTRA",x)
if missing or extra: raise SystemExit(1)
print("SCHEMATIC_CONNECTIVITY_MATCH")
