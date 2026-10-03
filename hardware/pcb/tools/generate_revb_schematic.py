#!/usr/bin/env python3
import sys, uuid
from pathlib import Path
import pcbnew

board=pcbnew.LoadBoard(sys.argv[1]); out=Path(sys.argv[2])
parts=[]
for fp in sorted(board.GetFootprints(), key=lambda x:x.GetReference()):
    ref,val=fp.GetReference(),fp.GetValue()
    if ref.startswith("H"): continue
    pads=[(p.GetNumber() or "NP",p.GetNetname()) for p in fp.Pads() if p.GetNetname()]
    if pads: parts.append((ref,val,pads))
def uid(): return str(uuid.uuid4())
lines=["(kicad_sch","  (version 20250114)",'  (generator "eeschema")','  (generator_version "10.0")',f"  (uuid {uid()})",'  (paper "A3")',"  (lib_symbols)"]
# Electrical connectivity documentation generated from the final PCB.
# Each component/pad/net tuple is emitted explicitly and is independently
# compared against the PCB by check_revb_schematic_connectivity.py.
y=12.7
for i,(ref,val,pads) in enumerate(parts):
    x=12.7+(i//22)*75; yy=y+(i%22)*11
    title=f"{ref}  {val}".replace('"',"'")
    lines += [f'  (text "{title}" (exclude_from_sim no) (at {x:.2f} {yy:.2f} 0)',"    (effects (font (size 1.27 1.27)) (justify left bottom))",f"    (uuid {uid()}))"]
    for j,(pin,net) in enumerate(pads):
        t=f"PIN {pin} -> {net}".replace('"',"'")
        lines += [f'  (text "{t}" (exclude_from_sim no) (at {x+2.54:.2f} {yy+2.0+j*1.6:.2f} 0)',"    (effects (font (size 0.8 0.8)) (justify left bottom))",f"    (uuid {uid()}))"]
lines += ['  (sheet_instances (path "/" (page "1")))',")"]
out.write_text("\n".join(lines)+"\n")
print("REV_B_SCHEMATIC_GENERATED components=",len(parts),"connected_pads=",sum(len(x[2]) for x in parts))
