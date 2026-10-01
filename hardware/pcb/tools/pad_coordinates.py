#!/usr/bin/env python3
"""Report absolute pad coordinates from the Rev A KiCad PCB.

This is an engineering helper, not a router. It handles the rotations currently
used by the board and is intended to make routing reviews reproducible.
"""
from pathlib import Path
import math,re,sys

p=Path(sys.argv[1] if len(sys.argv)>1 else "hardware/pcb/kicad/PSN-Presepe-Mega.kicad_pcb")
s=p.read_text(encoding="utf-8")

def blocks():
    pos=0
    while True:
        st=s.find("(footprint ",pos)
        if st<0:return
        d=0;q=False;esc=False
        for i in range(st,len(s)):
            ch=s[i]
            if q:
                if esc:esc=False
                elif ch=="\\":esc=True
                elif ch=='"':q=False
            else:
                if ch=='"':q=True
                elif ch=="(":d+=1
                elif ch==")":
                    d-=1
                    if d==0:
                        yield s[st:i+1]
                        pos=i+1
                        break

rows=[]
for b in blocks():
    refm=re.search(r'\(property "Reference" "([^"]+)"',b)
    atm=re.search(r'\(at\s+(-?[\d.]+)\s+(-?[\d.]+)(?:\s+(-?[\d.]+))?\)', b)
    if not refm or not atm:continue
    ref=refm.group(1); fx,fy=float(atm.group(1)),float(atm.group(2)); fr=float(atm.group(3) or 0)
    a=math.radians(fr)
    for m in re.finditer(r'\(pad "([^"]+)"[^\n]*',b):
        line=m.group(0)
        am=re.search(r'\(at (-?[\d.]+) (-?[\d.]+)(?: (-?[\d.]+))?\)',line)
        nm=re.search(r'\(net \d+ "([^"]+)"\)',line)
        if not am or not nm:continue
        px,py=float(am.group(1)),float(am.group(2))
        # KiCad footprint rotation uses the standard 2D transform in board coordinates.
        x=fx+px*math.cos(a)-py*math.sin(a)
        y=fy+px*math.sin(a)+py*math.cos(a)
        rows.append((ref,m.group(1),nm.group(1),x,y))
for r in rows:
    print(f"{r[0]},{r[1]},{r[2]},{r[3]:.3f},{r[4]:.3f}")
