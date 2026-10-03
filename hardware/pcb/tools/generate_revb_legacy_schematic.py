#!/usr/bin/env python3
import sys
from pathlib import Path
import pcbnew

board=pcbnew.LoadBoard(sys.argv[1]); out=Path(sys.argv[2]); cache=out.with_name(out.stem+"-cache.lib")
parts=[]
for fp in sorted(board.GetFootprints(),key=lambda x:x.GetReference()):
    ref,val=fp.GetReference(),fp.GetValue()
    if ref.startswith("H"): continue
    pads=[(p.GetNumber() or "NP",p.GetNetname()) for p in fp.Pads() if p.GetNetname()]
    if pads: parts.append((ref,val,pads))

lib=["EESchema-LIBRARY Version 2.4","#encoding utf-8"]
for ref,val,pads in parts:
    name=("PSN_"+ref).replace("-","_")
    lib += [f"#\n# {name}\n#",f"DEF {name} {ref[0]} 0 40 Y Y 1 F N",
            f'F0 "{ref}" 0 100 50 H V C CNN',f'F1 "{val}" 0 -100 50 H V C CNN',"DRAW"]
    h=max(100,len(pads)*50)
    lib.append(f"S -300 {h} 300 {-h} 0 1 10 f")
    for i,(pin,net) in enumerate(pads):
        y=(len(pads)-1-i*2)*50
        lib.append(f"X {pin} {pin} -500 {y} 200 R 40 40 1 1 B")
    lib += ["ENDDRAW","ENDDEF"]
lib += ["#End Library"]
cache.write_text("\n".join(lib)+"\n")

sch=["EESchema Schematic File Version 4","LIBS:"+out.stem+"-cache","EELAYER 29 0","EELAYER END",
"$Descr A3 16535 11693","Sheet 1 1",'Title "PSN-Presepe Mega Controller Rev B"', 'Rev "B"',
'Comp "zanac / PSN-Presepe"','Comment1 "Generated from validated Rev-B PCB connectivity"','$EndDescr']
x0,y0=1200,1200
for idx,(ref,val,pads) in enumerate(parts):
    col,row=idx//18,idx%18; x=x0+col*2600; y=y0+row*520
    name=("PSN_"+ref).replace("-","_")
    sch += ["$Comp",f"L {out.stem}-cache:{name} {ref}",f"U 1 1 {0x60000000+idx:X}",f"P {x} {y}",
            f'F 0 "{ref}" H {x} {y-80} 40  0000 C CNN',f'F 1 "{val}" H {x} {y+80} 30  0000 C CNN',
            f"\t1    {x} {y}", "\t1    0    0    -1","$EndComp"]
    for i,(pin,net) in enumerate(pads):
        py=y+(len(pads)-1-i*2)*50
        sch += [f"Text Label {x-700} {py} 2    35   ~ 0",net,f"Wire Wire Line",f"\t{x-700} {py} {x-500} {py}"]
sch += ["$EndSCHEMATC"]
out.write_text("\n".join(sch)+"\n")
print("LEGACY_REAL_SCHEMATIC components=",len(parts),"pins=",sum(len(p[2]) for p in parts),out,cache)
