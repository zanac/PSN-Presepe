from pathlib import Path
import argparse,re

ap=argparse.ArgumentParser()
ap.add_argument("--output",required=True)\na=ap.parse_args()

src=Path("hardware/pcb/kicad/PSN-Presepe-Mega.kicad_pcb")
dst=Path(a.output)
text=src.read_text()
OX,OY=20.0,20.0
factor=1.0

def blocks(s,token):
    out=[]; pos=0
    while True:
        st=s.find(token,pos)
        if st<0: break
        d=0;q=False;esc=False;end=None
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
        out.append((st,end,s[st:end]));pos=end
    return out

for token in ("(segment","(via","(zone"):
    for st,en,b in reversed(blocks(text,token)): text=text[:st]+text[en:]

for st,en,b in reversed(blocks(text,"(footprint")):
    m=re.search(r'[(]at ([-0-9.]+) ([-0-9.]+)([^)]*)[)]',b)
    if not m: continue
    x,y=float(m.group(1)),float(m.group(2))
    nx=OX+factor*(x-OX); ny=OY+factor*(y-OY)
    nb=b[:m.start()]+f"(at {nx:.4f} {ny:.4f}{m.group(3)})"+b[m.end():]
    text=text[:st]+nb+text[en:]

w=280*factor; h=170*factor
old='''(gr_rect
		(start 20 20)
		(end 300 190)'''
new=f'''(gr_rect
		(start 20 20)
		(end {20+w:.4f} {20+h:.4f})'''
if old not in text: raise RuntimeError("Edge.Cuts rectangle not found")
text=text.replace(old,new,1)
dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(text)
print(f"CLEAN board={w:.1f}x{h:.1f}mm footprints={len(blocks(text,'(footprint'))}")
