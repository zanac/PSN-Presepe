#!/usr/bin/env python3
from pathlib import Path
import re, sys

pcb=Path("hardware/pcb/kicad/PSN-Presepe-Mega.kicad_pcb").read_text()
p=pcb.find('(property "Reference" "MCU1"')
if p<0: raise SystemExit("MEGA_PINMAP_FAIL MCU1 missing")
a=pcb.rfind("\n\t(footprint",0,p)+1
depth=0; end=None
for i,ch in enumerate(pcb[a:],a):
    if ch=="(": depth+=1
    elif ch==")":
        depth-=1
        if depth==0: end=i+1; break
block=pcb[a:end]

actual={}
for m in re.finditer(r'\(pad "([^"]+)"',block):
    start=m.start(); depth=0; stop=None
    for i,ch in enumerate(block[start:],start):
        if ch=="(": depth+=1
        elif ch==")":
            depth-=1
            if depth==0: stop=i+1; break
    pb=block[start:stop]
    n=re.search(r'\(net \d+ "([^"]+)"\)',pb)
    actual[m.group(1)]=n.group(1) if n else None

expected={
"A0":"A0_POT","D2":"D2_CIELO_R","D3":"D3_CIELO_G","D4":"D4_CIELO_B",
"D5":"D5_STELLE_DATA","D6":"D6_BUZZER","D7":"D7_TRAM_R","D8":"D8_CASETTE_DATA",
"D11":"D11_TRAM_G","D12":"D12_TRAM_B","D20":"D20_SDA","D21":"D21_SCL",
"D22":"D22_START","D23":"D23_NEXT","D24":"D24_TEST",
**{f"D{i}":f"D{i}_RELAY{i-24}" for i in range(25,41)},
"D44":"D44_ALBA_R","D45":"D45_ALBA_G","D46":"D46_ALBA_B","VIN":"+12V",
}
errors=[f"{pad}: expected {net}, got {actual.get(pad)}" for pad,net in expected.items() if actual.get(pad)!=net]
for pad in ["A1","D9","D10","D13","D41","D42","D43","IORF"]:
    if actual.get(pad) is not None: errors.append(f"{pad}: expected free, got {actual.get(pad)}")
if errors:
    print("\n".join("MEGA_PINMAP_FAIL "+e for e in errors)); sys.exit(1)
print(f"MEGA_PINMAP_PASS used_signals={len(expected)} protected_free_pins=8")
