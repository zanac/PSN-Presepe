#!/usr/bin/env python3
from pathlib import Path
import sys

bom=Path("hardware/pcb/BOM.md").read_text()
ass=Path("hardware/pcb/ASSEMBLY.md").read_text()
fp=Path("hardware/pcb/kicad/PSN_Presep_Custom.pretty/Arduino_Mega2560_R3_Shield.kicad_mod").read_text()

errors=[]
for token in ["HDR-MEGA-STACK","FITTED / MANDATORY","long male tails","Female sockets"]:
    if token not in bom: errors.append("BOM missing "+token)
if "never DNI/DNP" not in bom: errors.append("BOM does not explicitly prohibit DNI/DNP")
for token in ["female stackable / pass-through headers","mandatory fitted components"]:
    if token not in ass: errors.append("ASSEMBLY missing "+token)
for token in ['fp_text user "USB"','fp_text user "Barrel Jack"']:
    if token not in fp: errors.append("Mega footprint missing "+token)

# Mechanical reference geometry encoded in the Mega footprint:
# board body nominal x=0..101.6, y=-53.34..0 mm.
# USB-B body reaches x=-6.34; courtyard reaches x=-6.594.
# Barrel jack body reaches x=-1.68; courtyard reaches x=-1.934.
required=["-6.594 -44.2576","-6.594 -31.9396","-1.934 -12.5476","-1.934 -3.0486"]
for token in required:
    if token not in fp: errors.append("Mega connector courtyard geometry missing "+token)

if errors:
    print("\n".join("MEGA_MECH_BOM_FAIL "+x for x in errors))
    sys.exit(1)
print("MEGA_MECH_BOM_PASS stackable_headers=FITTED usb_protrusion=6.594mm barrel_protrusion=1.934mm")
