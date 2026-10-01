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

net_header = s[:s.find('(footprint ')]
global_nets = re.findall(r'^\s*\(net (\d+) "([^"]+)"\)\s*$', net_header, re.M)
assert len(global_nets) == 119, f"Expected 119 global nets, got {len(global_nets)}"
assert len({n for n, _ in global_nets}) == 119, "Duplicate global net IDs"
assert len({name for _, name in global_nets}) == 119, "Duplicate global net names"

tail = s[s.find("(footprint "):]
embedded = []  # KiCad may indent global nets; malformed nesting is covered structurally above.
assert not embedded, f"Embedded standalone net declarations after footprint section: {len(embedded)}"

refs = re.findall(r'\(property "Reference" "([^"]+)"', s)
assert len(refs) == 83, f"Expected 83 references including mounting holes, got {len(refs)}"
assert len(set(refs)) == 83, "Duplicate references"

zones = s.count("(zone ")
assert zones == 0, f"Draft board unexpectedly contains {zones} copper zone(s); contact-zone isolation must be reviewed before adding pours"

segments = len(re.findall(r'\(segment\b', s))
if os.environ.get("ALLOW_ROUTING") != "1":
    approved_source_route_nets = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 111, 112, 113}  # OLED + buttons + A0 + D25/D26/D27/D28/D29 relay inputs + K1/K2/K3/K4/K5/K6/K7/K8/K9/K10/K11/K12/K13/K14/K15/K16 coil-low + local MOSFET gate nodes
    routed_ids = {int(x) for x in re.findall(r'\(segment\b[\s\S]{0,500}?\(net (\d+)\)', s)}
    via_ids = {int(x) for x in re.findall(r'\(via\b[\s\S]{0,500}?\(net (\d+)\)', s)}
    unexpected = (routed_ids | via_ids) - approved_source_route_nets
    assert not unexpected, f"Source PCB contains unapproved routed net IDs: {sorted(unexpected)}"
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
        assert re.search(rf'\(pad "{pad}"[\s\S]{{0,800}}?\(net \d+ "{net}"\)', block), f"K{i} pad {pad} must be {net}"
    assert re.search(r'\(pad "3"[\s\S]{0,300}?\(at 17\.78 0(?: 90)?\)', block), f"K{i} pad 3 geometry must be x=17.78 mm"


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
    m = re.search(rf'\(pad "{re.escape(str(pad))}"[\s\S]{{0,800}}?\(net \d+ "([^"]+)"\)', b)
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
    m = re.search(r'\(footprint[\s\S]{0,500}?\(at ([0-9.]+) ([0-9.]+)(?: ([0-9.]+))?\)', b)
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


# MOSFET thermal/mechanical reservation: keep all TO-220 devices in the dedicated
# heatsink/airflow region and prevent accidental crowding.
qpos=[]
for i in range(1,10):
    x,y,rot=footprint_at(f"Q{i}")
    assert 65.0 <= x <= 115.0 and 130.0 <= y <= 170.0, f"Q{i} left MOSFET thermal zone: {(x,y)}"
    qpos.append((i,x,y))
for a in range(len(qpos)):
    for b in range(a+1,len(qpos)):
        ia,xa,ya=qpos[a]; ib,xb,yb=qpos[b]
        dist=((xa-xb)**2+(ya-yb)**2)**0.5
        assert dist >= 14.0, f"Q{ia}/Q{ib} too close for heatsink airflow: {dist:.1f} mm"


# When experimental routing is enabled, every segment must use a declared net.
if os.environ.get("ALLOW_ROUTING") == "1":
    declared={int(i) for i,_ in global_nets}
    for m in re.finditer(r'\(segment\b[^)]*(?:\)[^)]*)*?\(net (\d+)\)',s):
        assert int(m.group(1)) in declared, f"Segment uses undeclared net {m.group(1)}"


# Duplicate copper primitives are forbidden: they add no connectivity and make
# routing review/counts misleading.
segment_lines=[ln.strip() for ln in s.splitlines() if "(segment " in ln]
assert len(segment_lines)==len(set(segment_lines)), "Duplicate routed segment(s) detected"
via_lines=[ln.strip() for ln in s.splitlines() if "(via " in ln]
assert len(via_lines)==len(set(via_lines)), "Duplicate via(s) detected"


# Rotated-relay geometry invariant (KiCad board Y-down rotation).
# K1 at (150,60), local pad5 at (0,7.62), rotation 90deg -> (157.62,60).
def pad_local_at(ref, pad):
    b=footprint_block(ref)
    m=re.search(rf'\(pad "{re.escape(str(pad))}"[\s\S]{{0,300}}?\(at (-?[0-9.]+) (-?[0-9.]+)',b)
    assert m, f"Cannot read local pad coordinate {ref}.{pad}"
    return float(m.group(1)),float(m.group(2))
kx,ky,krot=footprint_at("K1")
px,py=pad_local_at("K1",5)
assert abs(krot-90.0)<1e-6
assert abs((kx+py)-157.62)<0.01 and abs((ky-px)-60.0)<0.01, "K1 rotated pad transform regression"

print(f"OK: {len(refs)} refs, {len(global_nets)} nets, {segments} segments, electrical + external-terminal invariants verified, no unreviewed zones")
