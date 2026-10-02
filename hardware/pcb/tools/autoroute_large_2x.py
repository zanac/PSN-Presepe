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
hard={"D40_RELAY16","D44_ALBA_R","D46_ALBA_B","R15_COM","R16_NC","R14_NO","R16_COM","D30_RELAY6","D28_RELAY4","D34_RELAY10",
      "R16_NO","R14_NC","R13_NO","R13_NC","R13_COM","D26_RELAY2","D36_RELAY12","D38_RELAY14","D24_TEST","D22_START","D21_SCL","D20_SDA"}
failed_first=["D32_RELAY8","D26_RELAY2","D38_RELAY14","D24_TEST","D22_START","D21_SCL","D20_SDA",
              "R16_COM","R16_NC","D40_RELAY16","R15_COM","R14_NO","D44_ALBA_R","D46_ALBA_B","D30_RELAY6","D28_RELAY4","D34_RELAY10"]
priority={n:i for i,n in enumerate(failed_first)}
pairs.sort(key=lambda z: (0,priority[z[1]]) if z[1] in priority else (1 if z[1] in hard else 2, math.dist(z[2][0],z[2][1])))
print("PAIR_NETS",len(pairs))
def drc_critical(board):
    report=Path("/tmp/large-step.drc.txt")
    subprocess.run(["kicad-cli","pcb","drc","--severity-all","--output",str(report),str(board)],
                   stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    s=report.read_text() if report.exists() else ""
    counts={}
    for line in s.splitlines():
        z=line.strip()
        if z.startswith("[") and "]:" in z:
            cat=z[1:z.index("]:")]
            counts[cat]=counts.get(cat,0)+1
    keys=("clearance","shorting_items","tracks_crossing","hole_clearance")
    return sum(counts.get(k,0) for k in keys),counts

base=Path("/tmp/large-base.kicad_pcb");base.write_text(text)
baseline_critical,baseline_counts=drc_critical(base)
print("BASE_CRITICAL",baseline_critical,baseline_counts)
done=[];failed=[];rejected=[]
for k,(nid,name,ps) in enumerate(pairs,1):
    a,b=ps
    tmp=Path("/tmp/large-work.kicad_pcb");tmp.write_text(text)
    # Contact nets get the conservative 1.50 mm routing clearance.
    contact=bool(re.fullmatch(r"R[0-9]+_(COM|NO|NC)",name))
    width=1.0 if contact else 0.5
    # Try increasingly conservative geometry inside the same CI job.
    clearances=[2.10,2.50] if contact else [0.80,1.10,1.40]
    attempts=[("1.0","120","240",True),("0.5","180","300",True),
              ("1.0","120","80",False),("0.5","180","100",False)]
    # Dense/hard nets get a fine-grid, low-via-cost escape attempt. On the
    # oversized board it is preferable to change layer early rather than
    # compete for the same local B.Cu corridor.
    # Keep the fine-grid fallback conservative: the previous globally cheap-via
    # experiment regressed the clean result from 97 to 98 unconnected.
    if name in hard:
        attempts += [("0.25","240","140",False)]
    accepted=False
    had_route=False
    for clearance in clearances:
        if accepted: break
        for step,margin,via,no_vias in attempts:
            tmp=Path("/tmp/large-work.kicad_pcb");tmp.write_text(text)
            cmd=["python3","hardware/pcb/tools/grid_router.py",str(tmp),"--net",name,
                 "--start",f"{a[0]},{a[1]},B.Cu","--goal",f"{b[0]},{b[1]},B.Cu",
                 "--step",step,"--clearance",str(clearance),"--margin",margin,"--via-cost",via]
            if no_vias: cmd.append("--no-vias")
            try:
                r=subprocess.run(cmd,text=True,capture_output=True,timeout=20)
            except subprocess.TimeoutExpired:
                continue
            if r.returncode!=0: continue
            had_route=True
            pts=[]
            for line in r.stdout.splitlines():
                if re.match(r"^-?[0-9]",line):
                    x,y,la=line.split(",");pts.append((float(x),float(y),la))
            if not pts: continue
            pts[0]=(a[0],a[1],pts[0][2]);pts[-1]=(b[0],b[1],pts[-1][2])
            items=[]
            for u,v in zip(pts,pts[1:]):
                if u[2]!=v[2]:
                    items.append(chr(9)+f'(via (at {u[0]} {u[1]}) (size 1.2) (drill 0.6) (layers "F.Cu" "B.Cu") (net {nid}))'+chr(10))
                else:
                    items.append(chr(9)+f'(segment (start {u[0]} {u[1]}) (end {v[0]} {v[1]}) (width {width}) (layer "{u[2]}") (net {nid}))'+chr(10))
            idx=text.rfind(")")
            candidate=text[:idx]+"".join(items)+text[idx:]
            check=Path("/tmp/large-candidate.kicad_pcb");check.write_text(candidate)
            crit,counts=drc_critical(check)
            if crit<=baseline_critical:
                text=candidate
                baseline_critical=crit
                done.append(name)
                print("OK_DRC",k,name,"critical",crit,"clr",clearance,"step",step,"novia",no_vias)
                accepted=True
                break
    if not accepted:
        (rejected if had_route else failed).append(name)
        print("REJECT_DRC" if had_route else "FAIL",k,name)
PCB.write_text(text)
print("ROUTED",len(done),"FAILED",len(failed),failed,"REJECTED_DRC",len(rejected),rejected,"FINAL_CRITICAL",baseline_critical)
