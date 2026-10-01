#!/usr/bin/env python3
from pathlib import Path
import os
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

zones = s.count("(zone ")
assert zones == 0, f"Draft board unexpectedly contains {zones} copper zone(s); contact-zone isolation must be reviewed before adding pours"

segments = s.count("(segment ")
if os.environ.get("ALLOW_ROUTING") != "1":
    assert segments == 0, f"Draft board unexpectedly contains {segments} routed segment(s)"
elif segments == 0:
    print("WARNING: ALLOW_ROUTING=1 but candidate still has zero routed segments")


# Omron G5Q-1 SPDT contact mapping: 1/5 coil, 2 COM, 3 NC, 4 NO.
for i in range(1, 17):
    marker = f'(property "Reference" "K{i}"'
    ri = s.find(marker)
    assert ri >= 0, f"Missing relay K{i}"
    start = s.rfind('(footprint "PSN_Presep_Custom:Relay_Omron_G5Q-1_SPDT"', 0, ri)
    end = s.find('\n  (footprint ', ri)
    if end < 0:
        end = s.find('\n  (gr_', ri)
    block = s[start:end]
    expected = {"2": f"R{i}_COM", "3": f"R{i}_NC", "4": f"R{i}_NO"}
    for pad, net in expected.items():
        assert re.search(rf'\(pad "{pad}"[^\n]*\(net \d+ "{net}"\)', block), f"K{i} pad {pad} must be {net}"
    assert re.search(r'\(pad "3"[^\n]*\(at 17\.78 0(?: 90)?\)', block), f"K{i} pad 3 geometry must be x=17.78 mm"


def footprint_block(ref):
    marker = f'(property "Reference" "{ref}"'
    ri = s.find(marker)
    assert ri >= 0, f"Missing footprint {ref}"
    start = s.rfind("(footprint ", 0, ri)
    depth = 0
    quoted = escaped = False
    for j in range(start, len(s)):
        ch = s[j]
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
        else:
            if ch == '"':
                quoted = True
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return s[start:j+1]
    raise AssertionError(f"Unclosed footprint {ref}")

def pad_net(ref, pad):
    b = footprint_block(ref)
    m = re.search(rf'\(pad "{re.escape(str(pad))}"[^\n]*\(net \d+ "([^"]+)"\)', b)
    assert m, f"Missing net on {ref} pad {pad}"
    return m.group(1)

assert pad_net("J1", 1) == "+12V" and pad_net("J1", 2) == "GND"
assert pad_net("MCU1", "VIN") == "+12V"
for p5 in ("5V1", "5V2", "5V3", "5V4"):
    assert pad_net("MCU1", p5) == "+5V_MEGA"
assert [pad_net("RV1", x) for x in (1,2,3)] == ["GND","A0_POT","+5V_MEGA"]
for cap in ("C1","C2","C3"):
    assert [pad_net(cap,x) for x in (1,2)] == ["+12V","GND"]

drains = ["CIELO_R_NEG","CIELO_G_NEG","CIELO_B_NEG","TRAM_R_NEG","TRAM_G_NEG","TRAM_B_NEG","ALBA_R_NEG","ALBA_G_NEG","ALBA_B_NEG"]
for i, drain in enumerate(drains, 1):
    assert pad_net(f"Q{i}",1) == f"GATE_Q{i}"
    assert pad_net(f"Q{i}",2) == drain
    assert pad_net(f"Q{i}",3) == "GND"

for bank, first in ((1,1),(2,9)):
    u=f"U{bank}"
    assert pad_net(u,9) == "GND"
    assert pad_net(u,10) == "+12V"
    for ch in range(8):
        relay=first+ch
        assert pad_net(u,ch+1) == f"D{24+relay}_RELAY{relay}"
        assert pad_net(u,18-ch) == f"RELAY{relay}_COIL_LOW"
        assert pad_net(f"K{relay}",1) == "+12V"
        assert pad_net(f"K{relay}",5) == f"RELAY{relay}_COIL_LOW"

# External terminal pad order must match the printed wiring labels.
for i in range(1, 17):
    assert [pad_net(f"JR{i}",x) for x in (1,2,3)] == [f"R{i}_COM",f"R{i}_NO",f"R{i}_NC"]

assert [pad_net("J_CIELO",x) for x in (1,2,3,4)] == ["+12V","CIELO_R_NEG","CIELO_G_NEG","CIELO_B_NEG"]
assert [pad_net("J_TRAMONTO",x) for x in (1,2,3,4)] == ["+12V","TRAM_R_NEG","TRAM_G_NEG","TRAM_B_NEG"]
assert [pad_net("J_ALBA",x) for x in (1,2,3,4)] == ["+12V","ALBA_R_NEG","ALBA_G_NEG","ALBA_B_NEG"]
assert [pad_net("J_STELLE",x) for x in (1,2,3)] == ["+12V","GND","D5_STELLE_DATA"]
assert [pad_net("J_CASETTE",x) for x in (1,2,3)] == ["+12V","GND","D8_CASETTE_DATA"]
assert [pad_net("J_OLED",x) for x in (1,2,3,4)] == ["+5V_MEGA","GND","D20_SDA","D21_SCL"]
assert [pad_net("J_START",x) for x in (1,2)] == ["D22_START","GND"]
assert [pad_net("J_NEXT",x) for x in (1,2)] == ["D23_NEXT","GND"]
assert [pad_net("J_TEST",x) for x in (1,2)] == ["D24_TEST","GND"]


# Mechanical perimeter invariants: external terminals must remain on board edges.
def footprint_at(ref):
    b = footprint_block(ref)
    m = re.search(r'\(footprint [^\n]*\(layer "[^"]+"\) \(at ([0-9.]+) ([0-9.]+)(?: ([0-9.]+))?\)', b)
    assert m, f"Cannot read placement for {ref}"
    return tuple(float(x) if x is not None else 0.0 for x in m.groups())

bottom = ["J1","J_OLED","J_START","J_NEXT","J_TEST","J_CIELO","J_TRAMONTO","J_ALBA","J_STELLE","J_CASETTE"]
for ref in bottom:
    x,y,rot = footprint_at(ref)
    assert y >= 183.0, f"{ref} moved away from bottom perimeter: y={y}"
for i in range(1,9):
    x,y,rot = footprint_at(f"JR{i}")
    assert y <= 28.0, f"JR{i} moved away from top perimeter: y={y}"
for i in range(9,17):
    x,y,rot = footprint_at(f"JR{i}")
    assert x >= 291.0, f"JR{i} moved away from right perimeter: x={x}"

print(f"OK: {len(refs)} refs, {len(global_nets)} nets, {segments} segments, electrical + external-terminal invariants verified, no unreviewed zones")
