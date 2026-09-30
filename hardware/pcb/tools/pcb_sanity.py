#!/usr/bin/env python3
from pathlib import Path
import re
import sys

p = Path(sys.argv[1] if len(sys.argv) > 1 else "hardware/pcb/kicad/PSN-Presepe-Mega.kicad_pcb")
s = p.read_text(encoding="utf-8")

depth = minimum = 0
for ch in s:
    if ch == "(":
        depth += 1
    elif ch == ")":
        depth -= 1
        minimum = min(minimum, depth)
assert depth == 0 and minimum == 0, f"Unbalanced PCB S-expression: depth={depth}, min={minimum}"

bad = re.findall(r'\(layers [^)]*\(net \d+ "[^"]+"\)', s)
assert not bad, f"Malformed net nested inside layers: {len(bad)} occurrence(s)"

global_nets = re.findall(r'^  \(net (\d+) "([^"]+)"\)$', s, re.M)
assert len(global_nets) == 119, f"Expected 119 global nets, got {len(global_nets)}"
assert len({n for n, _ in global_nets}) == 119, "Duplicate global net IDs"
assert len({name for _, name in global_nets}) == 119, "Duplicate global net names"

tail = s[s.find("  (footprint "):]
embedded = re.findall(r'^\s+\(net \d+ "[^"]+"\)$', tail, re.M)
assert not embedded, f"Embedded standalone net declarations after footprint section: {len(embedded)}"

refs = re.findall(r'\(property "Reference" "([^"]+)"', s)
assert len(refs) == 83, f"Expected 83 references including mounting holes, got {len(refs)}"
assert len(set(refs)) == 83, "Duplicate references"

segments = s.count("(segment ")
assert segments == 0, f"Draft board unexpectedly contains {segments} routed segment(s)"

print(f"OK: {len(refs)} refs, {len(global_nets)} nets, {segments} segments, balanced S-expression")
