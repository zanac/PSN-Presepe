#!/usr/bin/env python3
from pathlib import Path
import re, sys

pcb=Path("hardware/pcb/kicad/PSN-Presepe-Mega.kicad_pcb").read_text()
required={
"J1":["12V","GND"],"J_OLED":["5V","GND","SDA","SCL"],
"J_START":["START","GND"],"J_NEXT":["NEXT","GND"],"J_TEST":["TEST","GND"],
"J_CIELO":["12V","R","G","B"],"J_TRAMONTO":["12V","R","G","B"],"J_ALBA":["12V","R","G","B"],
"J_STELLE":["12V","GND","DATA"],"J_CASETTE":["12V","GND","DATA"],
}
for i in range(1,17): required[f"JR{i}"]=["COM","NO","NC"]

def footprint_block(ref):
    p=pcb.find(f'(property "Reference" "{ref}"')
    if p<0: return None
    a=pcb.rfind("\n\t(footprint",0,p)+1
    depth=0
    for i in range(a,len(pcb)):
        if pcb[i]=="(": depth+=1
        elif pcb[i]==")":
            depth-=1
            if depth==0: return pcb[a:i+1]
    return None

errors=[]
for ref,labels in required.items():
    b=footprint_block(ref)
    if not b:
        errors.append(f"{ref}: footprint missing"); continue
    silk=re.findall(r'\(fp_text user "([^"]+)"[\s\S]*?\(layer "F\.SilkS"\)',b)
    for label in labels:
        if label not in silk: errors.append(f"{ref}: missing F.SilkS label {label}")
    if "TERMINAL_LABELS" not in b: errors.append(f"{ref}: terminal label marker missing")
if errors:
    print("\n".join("TERMINAL_SILK_FAIL "+x for x in errors))
    sys.exit(1)
print(f"TERMINAL_SILK_PASS connectors={len(required)} labels={sum(map(len,required.values()))}")
