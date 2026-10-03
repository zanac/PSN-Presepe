#!/usr/bin/env python3
import sys
import pcbnew

b = pcbnew.LoadBoard(sys.argv[1])
rows = []
for fp in sorted(b.GetFootprints(), key=lambda x: x.GetReference()):
    ref = fp.GetReference()
    value = fp.GetValue()
    if ref.startswith("H"):
        continue
    for p in sorted(fp.Pads(), key=lambda x: x.GetNumber()):
        rows.append((ref, value, p.GetNumber(), p.GetNetname()))
for r in rows:
    print("\t".join(r))
if len(rows) < 100:
    raise SystemExit("Unexpectedly small pad map")
