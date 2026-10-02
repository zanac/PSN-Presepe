from pathlib import Path
import re

src=Path("hardware/pcb/kicad/PSN-Presepe-Mega.kicad_pcb")
dst=Path("hardware/pcb/kicad/PSN-Presepe-Mega-LARGE-2X.kicad_pcb")
text=src.read_text()
OX,OY=20.0,20.0

def blocks(s, token):
    out=[]; pos=0
    while True:
        st=s.find(token,pos)
        if st<0: break
        d=0; q=False; esc=False; end=None
        for i in range(st,len(s)):
            ch=s[i]
            if q:
                if esc: esc=False
                elif ch=="\\": esc=True
                elif ch=='"': q=False
            else:
                if ch=='"': q=True
                elif ch=="(": d+=1
                elif ch==")":
                    d-=1
                    if d==0: end=i+1; break
        if end is None: raise RuntimeError(token)
        out.append((st,end,s[st:end])); pos=end
    return out

# Remove all routed copper; keep footprints/pads/nets.
for token in ("(segment","(via","(zone"):
    bs=blocks(text,token)
    for st,en,b in reversed(bs):
        text=text[:st]+text[en:]

# Spread every footprint position 2x from the top-left board origin.
bs=blocks(text,"(footprint")
for st,en,b in reversed(bs):
    m=re.search(r'[(]at ([-0-9.]+) ([-0-9.]+)([^)]*)[)]',b)
    if not m: continue
    x,y=float(m.group(1)),float(m.group(2))
    nx=OX+2*(x-OX); ny=OY+2*(y-OY)
    nb=b[:m.start()]+f"(at {nx:.4f} {ny:.4f}{m.group(3)})"+b[m.end():]
    text=text[:st]+nb+text[en:]

# 280x170 -> 560x340 while retaining the original top-left origin.
old='''(gr_rect
		(start 20 20)
		(end 300 190)'''
new='''(gr_rect
		(start 20 20)
		(end 580 360)'''
if old not in text: raise RuntimeError("Edge.Cuts rectangle not found")
text=text.replace(old,new,1)
dst.write_text(text)
print("LARGE2X",dst,"bytes",len(text),"footprints",len(blocks(text,"(footprint")),"segments",len(blocks(text,"(segment")),"vias",len(blocks(text,"(via")))
