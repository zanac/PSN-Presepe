#!/usr/bin/env python3
from pathlib import Path
import re,math,subprocess,tempfile

PCB=Path("hardware/pcb/kicad/PSN-Presepe-Mega-LARGE-2X.kicad_pcb")
text=PCB.read_text()

def blocks(s,token):
    out=[]; pos=0
    while True:
        st=s.find(token,pos)
        if st<0: return out
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
                        out.append(s[st:i+1]);pos=i+1;break

pads={}
for fp in blocks(text,"(footprint"):
    hm=re.search(r'[(]at ([-0-9.]+) ([-0-9.]+)(?: ([-0-9.]+))?[)]',fp)
    if not hm: continue
    fx,fy,rot=float(hm.group(1)),float(hm.group(2)),float(hm.group(3) or 0)
    aa=math.radians(-rot); ca,sa=math.cos(aa),math.sin(aa)
    for pb in blocks(fp,"(pad"):
        nm=re.search(r'[(]net ([0-9]+) "([^"]+)"[)]',pb)
        am=re.search(r'[(]at ([-0-9.]+) ([-0-9.]+)',pb)
        if not(nm and am):continue
        px,py=float(am.group(1)),float(am.group(2))
        x=fx+px*ca-py*sa;y=fy+px*sa+py*ca
        pads.setdefault((int(nm.group(1)),nm.group(2)),[]).append((x,y))

pairs=[(nid,name,ps) for (nid,name),ps in pads.items() if len(ps)==2 and nid]
pairs.sort(key=lambda z: math.dist(z[2][0],z[2][1]))
print("PAIR_NETS",len(pairs))
done=[];failed=[]
for k,(nid,name,ps) in enumerate(pairs,1):
    a,b=ps
    tmp=Path("/tmp/large-work.kicad_pcb");tmp.write_text(text)
    # Contact nets get the conservative 1.50 mm routing clearance.
    contact=bool(re.fullmatch(r"R[0-9]+_(COM|NO|NC)",name))
    clearance="1.50" if contact else "0.50"
    width=1.0 if contact else 0.5
    attempts=[("1.0","35","160"),("1.0","100","220"),("0.5","140","260")]
    q=None
    for step,margin,via in attempts:
        cmd=["python3","hardware/pcb/tools/grid_router.py",str(tmp),"--net",name,
             "--start",f"{a[0]},{a[1]},B.Cu","--goal",f"{b[0]},{b[1]},B.Cu",
             "--step",step,"--clearance",clearance,"--margin",margin,"--via-cost",via]
        r=subprocess.run(cmd,text=True,capture_output=True,timeout=15)
        if r.returncode==0:q=r;break
    if q is None:
        failed.append(name);print("FAIL",k,name);continue
    pts=[]
    for line in q.stdout.splitlines():
        if re.match(r"^-?[0-9]",line):
            x,y,la=line.split(",");pts.append((float(x),float(y),la))
    if not pts:failed.append(name);continue
    pts[0]=(a[0],a[1],pts[0][2]);pts[-1]=(b[0],b[1],pts[-1][2])
    items=[]
    for u,v in zip(pts,pts[1:]):
        if u[2]!=v[2]:
            items.append(f'\t(via (at {u[0]} {u[1]}) (size 1.2) (drill 0.6) (layers "F.Cu" "B.Cu") (net {nid}))\n')
        else:
            items.append(f'\t(segment (start {u[0]} {u[1]}) (end {v[0]} {v[1]}) (width {width}) (layer "{u[2]}") (net {nid}))\n')
    idx=text.rfind(")");text=text[:idx]+"".join(items)+text[idx:]
    done.append(name);print("OK",k,name,"contact" if contact else "signal")
PCB.write_text(text)
print("ROUTED",len(done),"FAILED",len(failed),failed)
