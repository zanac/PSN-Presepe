#!/usr/bin/env python3
from pathlib import Path
import re, math, subprocess

PCB=Path("hardware/pcb/kicad/PSN-Presepe-Mega-LARGE-2X.kicad_pcb")
TARGETS=["D4_CIELO_B","D26_RELAY2","D30_RELAY6"]
text=PCB.read_text()

def blocks_pos(s,token):
    out=[]; pos=0
    while True:
        st=s.find(token,pos)
        if st<0:return out
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
                        out.append((st,i+1,s[st:i+1]));pos=i+1;break

net_ids={name:int(n) for n,name in re.findall(r'^\s*\(net (\d+) "([^"]+)"\)\s*$',text,re.M)}
ids={net_ids[n] for n in TARGETS}
for token in ("(segment","(via"):
    for st,en,b in reversed(blocks_pos(text,token)):
        m=re.search(r'\(net (\d+)\)',b)
        if m and int(m.group(1)) in ids:
            text=text[:st]+text[en:]

def blocks(s,token): return [b for _,_,b in blocks_pos(s,token)]
pads={}
for fp in blocks(text,"(footprint"):
    hm=re.search(r'\(at ([-0-9.]+) ([-0-9.]+)(?: ([-0-9.]+))?\)',fp)
    if not hm:continue
    fx,fy,rot=float(hm.group(1)),float(hm.group(2)),float(hm.group(3) or 0)
    aa=math.radians(-rot);ca,sa=math.cos(aa),math.sin(aa)
    for pb in blocks(fp,"(pad"):
        nm=re.search(r'\(net (\d+) "([^"]+)"\)',pb);am=re.search(r'\(at ([-0-9.]+) ([-0-9.]+)',pb)
        if not(nm and am) or nm.group(2) not in TARGETS:continue
        px,py=float(am.group(1)),float(am.group(2))
        pads.setdefault(nm.group(2),[]).append((fx+px*ca-py*sa,fy+px*sa+py*ca))

def critical(s):
    p=Path("/tmp/local-check.kicad_pcb");p.write_text(s)
    r=Path("/tmp/local-check.drc")
    subprocess.run(["kicad-cli","pcb","drc","--severity-all","--output",str(r),str(p)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    z=r.read_text() if r.exists() else ""
    keys={"clearance","shorting_items","tracks_crossing","hole_clearance"}
    return sum(1 for x in z.splitlines() if x.strip().startswith("[") and x.strip()[1:x.strip().find("]:")] in keys)

print("LOCAL2_GROUP",TARGETS)
for name in TARGETS:
    ps=pads.get(name,[])
    if len(ps)!=2:
        print("LOCAL2_FAIL_PADS",name,len(ps));continue
    a,b=ps;nid=net_ids[name];accepted=False
    for step,clr,margin,via in [("0.5","0.8","180","100"),("0.25","0.8","240","140"),("0.5","1.1","220","120")]:
        p=Path("/tmp/local-work.kicad_pcb");p.write_text(text)
        cmd=["python3","hardware/pcb/tools/grid_router.py",str(p),"--net",name,"--start",f"{a[0]},{a[1]},B.Cu","--goal",f"{b[0]},{b[1]},B.Cu","--step",step,"--clearance",clr,"--margin",margin,"--via-cost",via]
        try:r=subprocess.run(cmd,text=True,capture_output=True,timeout=35)
        except subprocess.TimeoutExpired:continue
        if r.returncode:continue
        pts=[]
        for line in r.stdout.splitlines():
            if re.match(r"^-?[0-9]",line):
                x,y,la=line.split(",");pts.append((float(x),float(y),la))
        if not pts:continue
        pts[0]=(a[0],a[1],pts[0][2]);pts[-1]=(b[0],b[1],pts[-1][2])
        items=[]
        for u,v in zip(pts,pts[1:]):
            if u[2]!=v[2]:items.append(f'\t(via (at {u[0]} {u[1]}) (size 1.2) (drill 0.6) (layers "F.Cu" "B.Cu") (net {nid}))\n')
            else:items.append(f'\t(segment (start {u[0]} {u[1]}) (end {v[0]} {v[1]}) (width 0.5) (layer "{u[2]}") (net {nid}))\n')
        idx=text.rfind(")");cand=text[:idx]+"".join(items)+text[idx:]
        if critical(cand)==0:
            text=cand;accepted=True;print("LOCAL2_OK",name,"step",step,"clr",clr);break
    if not accepted:print("LOCAL2_FAIL",name)
PCB.write_text(text)
print("LOCAL2_FINAL_CRITICAL",critical(text))
