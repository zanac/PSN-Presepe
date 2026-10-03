#!/usr/bin/env python3
import csv, sys
from pathlib import Path
import pcbnew

if len(sys.argv) != 3:
    raise SystemExit("usage: export_bom_cpl.py BOARD OUTDIR")
board_path=Path(sys.argv[1]); out=Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)
b=pcbnew.LoadBoard(str(board_path))
fps=sorted(b.GetFootprints(),key=lambda f:f.GetReference())
rows=[]; cpl=[]
for f in fps:
    ref=f.GetReference(); value=f.GetValue(); fp=f.GetFPID().GetLibItemName()
    attrs=int(f.GetAttributes())
    pos=f.GetPosition(); side="Bottom" if f.IsFlipped() else "Top"
    rows.append([ref,1,value,fp,side])
    cpl.append([ref,f"{pcbnew.ToMM(pos.x):.4f}mm",f"{pcbnew.ToMM(pos.y):.4f}mm",side,f"{f.GetOrientationDegrees():.2f}"])
with open(out/"BOM.csv","w",newline="") as h:
    w=csv.writer(h); w.writerow(["Designator","Qty","Value","Footprint","Layer"]); w.writerows(rows)
with open(out/"CPL.csv","w",newline="") as h:
    w=csv.writer(h); w.writerow(["Designator","Mid X","Mid Y","Layer","Rotation"]); w.writerows(cpl)
print(f"MANUFACTURING_BOM_CPL_PASS footprints={len(fps)} bom_rows={len(rows)} cpl_rows={len(cpl)}")
