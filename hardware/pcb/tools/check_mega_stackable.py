#!/usr/bin/env python3
"""Mechanical stacking gate for Arduino Mega 2560 R3."""
from pathlib import Path
import re, sys

board_path="hardware/pcb/kicad/PSN-Presepe-Mega.kicad_pcb"
try:
    import pcbnew
except ImportError:
    raise SystemExit("pcbnew required: run inside KiCad CI")
board=pcbnew.LoadBoard(board_path)
fps=list(board.GetFootprints())
mega=next((f for f in fps if f.GetReference()=="MCU1"),None)
if mega is None: raise SystemExit("MCU1 Mega shield footprint not found")
ox=mega.GetPosition().x/1e6; oy=mega.GetPosition().y/1e6
# Approved Mega R3 body projection on the shield plane.
xmin,xmax=ox,ox+101.6; ymin,ymax=oy-53.34,oy
# Connector protrusions represented by the custom footprint courtyards.
usb=(ox-6.594,ox-0.254,oy-44.2576,oy-31.9396)
barrel=(ox-1.934,ox-0.254,oy-12.5476,oy-3.0486)

def intersects(box,rect):
    x0=box.GetX()/1e6; y0=box.GetY()/1e6
    x1=(box.GetX()+box.GetWidth())/1e6; y1=(box.GetY()+box.GetHeight())/1e6
    a,b,c,d=rect
    return not (x1<a or x0>b or y1<c or y0>d)

regions=[("Mega body",(xmin,xmax,ymin,ymax)),("USB-B",usb),("barrel jack",barrel)]
hits=[]
for fp in fps:
    if fp.GetReference()=="MCU1": continue
    box=fp.GetBoundingBox(False,False)
    for name,rect in regions:
        if intersects(box,rect): hits.append(f"{fp.GetReference()} intersects {name}")
if hits:
    print("\\n".join("MEGA_MECH_COLLISION "+x for x in sorted(set(hits))))
    sys.exit(1)
print(f"MEGA_STACKING_GEOMETRY_PASS body={xmin:.2f}..{xmax:.2f}x{ymin:.2f}..{ymax:.2f} usb_protrusion=6.594mm barrel_protrusion=1.934mm")
