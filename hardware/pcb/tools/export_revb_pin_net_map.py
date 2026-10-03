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
        net = p.GetNetname()
        if not net:
            continue
        rows.append((ref, value, p.GetNumber(), net))
print("ref\tvalue\tpad\tnet")
for r in rows:
    print("\t".join(r))
if len(rows) < 100:
    raise SystemExit("Unexpectedly small pad map")
