#!/usr/bin/env python3
import sys,uuid
from pathlib import Path
import pcbnew
U=lambda:str(uuid.uuid4())
board=pcbnew.LoadBoard(sys.argv[1]); out=Path(sys.argv[2])
parts=[]
for fp in sorted(board.GetFootprints(),key=lambda x:x.GetReference()):
    ref,val=fp.GetReference(),fp.GetValue()
    if ref.startswith("H"): continue
    pads=[(str(p.GetNumber() or "NP"),p.GetNetname()) for p in fp.Pads() if p.GetNetname()]
    if pads: parts.append((ref,val,pads))
root=U()
L=["(kicad_sch","  (version 20260306)",'  (generator "eeschema")','  (generator_version "10.0")',f'  (uuid "{root}")','  (paper "A3")',"  (lib_symbols"]
for ref,val,pads in parts:
    lid="PSN:"+ref
    L += [f'    (symbol "{lid}"','      (pin_names (offset 0))','      (exclude_from_sim no) (in_bom yes) (on_board yes) (in_pos_files yes)','      (duplicate_pin_numbers_are_jumpers no)',
          f'      (property "Reference" "{ref[0]}" (at 0 4 0) (effects (font (size 1.27 1.27))))',
          f'      (property "Value" "{val.replace(chr(34),chr(39))}" (at 0 -4 0) (effects (font (size 1.27 1.27))))',
          '      (property "Footprint" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))',
          '      (property "Datasheet" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))',
          '      (property "Description" "" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))',
          f'      (symbol "{ref}_0_1"']
    h=max(2.54,len(pads)*1.27)
    L.append(f'        (rectangle (start -5 {h:.2f}) (end 5 {-h:.2f}) (stroke (width 0) (type default)) (fill (type background)))')
    for i,(pin,net) in enumerate(pads):
        y=(len(pads)-1-i*2)*1.27
        L.append(f'        (pin passive line (at -7.54 {y:.2f} 0) (length 2.54) (name "{net}" (effects (font (size 1.0 1.0)))) (number "{pin}" (effects (font (size 1.0 1.0)))))')
    L += ["      )","      (embedded_fonts no)","    )"]
L += ["  )"]
for idx,(ref,val,pads) in enumerate(parts):
    x=25+(idx//12)*35; y=20+(idx%12)*22; sid=U()
    for i,(pin,net) in enumerate(pads):
        py=y+(len(pads)-1-i*2)*1.27; lx=x-7.54
        safe=net.replace('"',"'")
        L.append(f'  (global_label "{safe}" (shape bidirectional) (at {lx:.2f} {py:.2f} 180) (effects (font (size 1.0 1.0)) (justify right)) (uuid "{U()}"))')
    L += [f'  (symbol (lib_id "PSN:{ref}") (at {x:.2f} {y:.2f} 0) (unit 1) (body_style 1)',
          '    (exclude_from_sim no) (in_bom yes) (on_board yes) (in_pos_files yes) (dnp no)',f'    (uuid "{sid}")',
          f'    (property "Reference" "{ref}" (at {x:.2f} {y-5:.2f} 0) (effects (font (size 1.27 1.27))))',
          f'    (property "Value" "{val.replace(chr(34),chr(39))}" (at {x:.2f} {y+5:.2f} 0) (effects (font (size 1.0 1.0))))',
          f'    (property "Footprint" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))',
          f'    (property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))',
          f'    (property "Description" "" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))']
    for pin,net in pads: L.append(f'    (pin "{pin}" (uuid "{U()}"))')
    L += [f'    (instances (project "PSN-Presepe-Mega-RevB" (path "/{root}" (reference "{ref}") (unit 1))))',"  )"]
L += ['  (sheet_instances (path "/" (page "1")))','  (embedded_fonts no)',")"]
out.write_text("\n".join(L)+"\n")
print("REV_B_REAL_SCHEMATIC components=",len(parts),"connected_pads=",sum(len(p[2]) for p in parts))
