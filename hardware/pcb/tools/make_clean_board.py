from pathlib import Path
import argparse,re,uuid

ap=argparse.ArgumentParser()
ap.add_argument("--output", required=True)
a = ap.parse_args()

src=Path("hardware/pcb/kicad/PSN-Presepe-Mega.kicad_pcb")
# Inject production routing widths directly into the clean board so the Specctra DSN
# exporter sees them even when the board is processed outside the KiCad project context.
# Net classes remain authoritative in the .kicad_pro; this mirrors their assignments
# into explicit per-segment-free board setup for DSN export.
pro=Path("hardware/pcb/kicad/PSN-Presepe-Mega.kicad_pro")
if not pro.exists():
    raise RuntimeError("Missing KiCad project file required for production netclasses")

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

w=300*factor; h=180*factor
old='''(gr_rect
		(start 20 20)
		(end 320 200)'''
new=f'''(gr_rect
		(start 20 20)
		(end {20+w:.4f} {20+h:.4f})'''
if old not in text: raise RuntimeError("Edge.Cuts rectangle not found")
text=text.replace(old,new,1)
# Reserve a deliberate 3 mm GND power spine below the MOSFET matrix, away
# from the Q1..Q9 pads. Freerouting will connect the local GND branches to it.
preroutes=[
    ((52.0,176.0),(130.0,176.0),"B.Cu"),
    ((130.0,176.0),(130.0,128.0),"B.Cu"),
]
segments=[]
for idx,(p1,p2,layer) in enumerate(preroutes,1):
    uid=uuid.uuid5(uuid.NAMESPACE_URL,f"PSN-Presepe-GND-spine-{idx}")
    segments.append(f'''\n\t(segment\n\t\t(start {p1[0]} {p1[1]})\n\t\t(end {p2[0]} {p2[1]})\n\t\t(width 3)\n\t\t(layer "{layer}")\n\t\t(locked yes)\n\t\t(net "GND")\n\t\t(uuid "{uid}")\n\t)''')
end=text.rfind(")")
if end<0: raise RuntimeError("Board closing parenthesis not found")
text=text[:end]+"".join(segments)+"\n"+text[end:]
print(f"PREROUTE_GND_SPINE locked_segments={len(preroutes)} width=3.0mm corridor_y=176mm")

dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(text)
print(f"CLEAN board={w:.1f}x{h:.1f}mm footprints={len(blocks(text,'(footprint'))}")
