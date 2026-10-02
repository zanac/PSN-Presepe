#!/usr/bin/env python3
"""Obstacle-aware 2-layer A* router for targeted low-current PCB nets.

Parses KiCad PCB segments/vias/pads conservatively, rasterizes foreign copper
with clearance, and searches F.Cu/B.Cu with optional via transitions.
KiCad DRC remains the final authority; this tool only proposes a route.
"""
from __future__ import annotations
from dataclasses import dataclass
from heapq import heappush, heappop
from math import hypot, floor, ceil
import argparse, re
from pathlib import Path

LAYERS={"F.Cu":0,"B.Cu":1}
@dataclass(frozen=True)
class P: x:int; y:int; layer:int

def astar(start,goal,blocked,bounds,via_cost=18,allow_vias=True,soft_blocked=None,congestion_cost=5000):
    soft_blocked=soft_blocked or set()
    q=[]; serial=0; heappush(q,(0,serial,start)); prev={start:None}; cost={start:0}
    xmin,xmax,ymin,ymax=bounds
    # Grid edges only. Diagonal center-point routing can cut obstacle corners;
    # Manhattan edges are conservative and KiCad DRC-friendly.
    moves=[(1,0,0,10),(-1,0,0,10),(0,1,0,10),(0,-1,0,10)]
    if allow_vias: moves.append((0,0,1,via_cost))
    while q:
        _,_,p=heappop(q)
        if p==goal:
            out=[]
            while p is not None: out.append(p); p=prev[p]
            return out[::-1]
        for dx,dy,flip,w in moves:
            n=P(p.x+dx,p.y+dy,1-p.layer if flip else p.layer)
            if not(xmin<=n.x<=xmax and ymin<=n.y<=ymax) or n in blocked: continue
            nc=cost[p]+w
            if nc<cost.get(n,10**18):
                cost[n]=nc; prev[n]=p; serial+=1
                h=10*(abs(n.x-goal.x)+abs(n.y-goal.y))+ (via_cost if n.layer!=goal.layer else 0)
                heappush(q,(nc+h,serial,n))
    return None

def mark_disc(blocked,cx,cy,r,layers,step):
    ix0=floor((cx-r)/step); ix1=ceil((cx+r)/step)
    iy0=floor((cy-r)/step); iy1=ceil((cy+r)/step)
    rr=r*r
    for la in layers:
        for x in range(ix0,ix1+1):
            for y in range(iy0,iy1+1):
                if (x*step-cx)**2+(y*step-cy)**2<=rr: blocked.add(P(x,y,la))

def mark_segment(blocked,x1,y1,x2,y2,r,layer,step):
    length=hypot(x2-x1,y2-y1); n=max(1,ceil(length/(step/2)))
    for i in range(n+1):
        t=i/n; mark_disc(blocked,x1+(x2-x1)*t,y1+(y2-y1)*t,r,[layer],step)

def balanced_blocks(text, token):
    pos=0
    while True:
        i=text.find(token,pos)
        if i<0:return
        depth=0; quoted=False; esc=False
        for j in range(i,len(text)):
            ch=text[j]
            if quoted:
                if esc: esc=False
                elif ch=="\\": esc=True
                elif ch=='"': quoted=False
            else:
                if ch=='"': quoted=True
                elif ch=='(': depth+=1
                elif ch==')':
                    depth-=1
                    if depth==0:
                        yield text[i:j+1]; pos=j+1; break
        else:return

def extract_obstacles(text,target,step,clearance):
    blocked=set()
    net_names={int(n):name for n,name in re.findall('^ *[(]net ([0-9]+) "([^"]+)"[)] *$',text,re.M)}
    # Parse balanced copper records instead of one fragile multiline regex.
    for seg in balanced_blocks(text,"(segment"):
        st=re.search(r'[(]start ([0-9.-]+) ([0-9.-]+)[)]',seg)
        en=re.search(r'[(]end ([0-9.-]+) ([0-9.-]+)[)]',seg)
        wd=re.search(r'[(]width ([0-9.-]+)[)]',seg)
        ly=re.search(r'[(]layer "?(F[.]Cu|B[.]Cu)"?[)]',seg)
        nt=re.search(r'[(]net ([0-9]+)[)]',seg)
        if not(st and en and wd and ly and nt): continue
        n=int(nt.group(1))
        if net_names.get(n)==target: continue
        mark_segment(blocked,float(st.group(1)),float(st.group(2)),float(en.group(1)),float(en.group(2)),
                     float(wd.group(1))/2+clearance,LAYERS[ly.group(1)],step)
    for via in balanced_blocks(text,"(via"):
        at=re.search(r'[(]at ([0-9.-]+) ([0-9.-]+)[)]',via)
        sz=re.search(r'[(]size ([0-9.-]+)[)]',via)
        nt=re.search(r'[(]net ([0-9]+)[)]',via)
        if not(at and sz and nt): continue
        n=int(nt.group(1))
        if net_names.get(n)==target: continue
        mark_disc(blocked,float(at.group(1)),float(at.group(2)),float(sz.group(1))/2+clearance,[0,1],step)

    # Pads use coordinates local to their footprint; use escape-proof regexes.
    for fp in balanced_blocks(text,"(footprint"):
        head=re.search(r'[(]at ([0-9.-]+) ([0-9.-]+)(?: ([0-9.-]+))?[)]',fp)
        if not head: continue
        fx,fy=float(head.group(1)),float(head.group(2)); rot=float(head.group(3) or 0)
        import math
        ang=math.radians(-rot); ca,sa=math.cos(ang),math.sin(ang)
        for pad in balanced_blocks(fp,"(pad"):
            nm=re.search(r'[(]net ([0-9]+) "([^"]+)"[)]',pad)
            at=re.search(r'[(]at ([0-9.-]+) ([0-9.-]+)',pad)
            sz=re.search(r'[(]size ([0-9.-]+) ([0-9.-]+)[)]',pad)
            if not(at and sz): continue
            if nm and nm.group(2)==target: continue
            px,py=float(at.group(1)),float(at.group(2))
            gx=fx+px*ca-py*sa; gy=fy+px*sa+py*ca
            rad=max(float(sz.group(1)),float(sz.group(2)))/2+clearance
            if "thru_hole" in pad: layers=[0,1]
            elif '(layers "F.Cu"' in pad: layers=[0]
            elif '(layers "B.Cu"' in pad: layers=[1]
            else: layers=[0,1]
            mark_disc(blocked,gx,gy,rad,layers,step)
    return blocked

def compress(path):
    if not path:return path
    # Preserve every bend. Only remove a middle point when the two adjacent
    # steps are collinear on the same layer; layer changes must remain explicit.
    out=[path[0]]
    for i in range(1,len(path)-1):
        a,b,c=path[i-1],path[i],path[i+1]
        if a.layer!=b.layer or b.layer!=c.layer:
            out.append(b); continue
        dx1=b.x-a.x; dy1=b.y-a.y; dx2=c.x-b.x; dy2=c.y-b.y
        if dx1*dy2 != dy1*dx2: out.append(b)
    out.append(path[-1]); return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("pcb"); ap.add_argument("--net",required=True)
    ap.add_argument("--start",required=True,help="x,y,layer"); ap.add_argument("--goal",required=True)
    ap.add_argument("--step",type=float,default=.5); ap.add_argument("--clearance",type=float,default=.35)
    ap.add_argument("--margin",type=float,default=15)
    ap.add_argument("--no-vias",action="store_true")
    ap.add_argument("--via-cost",type=int,default=18)
    ap.add_argument("--soft-congestion",action="store_true",help="allow foreign routed tracks at very high cost; pads/vias remain hard obstacles")
    ap.add_argument("--congestion-cost",type=int,default=5000)
    a=ap.parse_args(); text=Path(a.pcb).read_text()
    def pt(s):
        x,y,la=s.split(","); return float(x),float(y),LAYERS[la]
    sx,sy,sl=pt(a.start); gx,gy,gl=pt(a.goal); step=a.step
    blocked=extract_obstacles(text,a.net,step,a.clearance)
    soft=set()
    if a.soft_congestion:
        # Existing routed track corridors are negotiable at high cost.
        # Pads and vias are re-applied as hard obstacles.
        net_names={int(n):name for n,name in re.findall(r'^ *[(]net ([0-9]+) "([^"]+)"[)] *$',text,re.M)}
        for seg in balanced_blocks(text,"(segment"):
            st=re.search(r'[(]start ([0-9.-]+) ([0-9.-]+)[)]',seg)
            en=re.search(r'[(]end ([0-9.-]+) ([0-9.-]+)[)]',seg)
            wd=re.search(r'[(]width ([0-9.-]+)[)]',seg)
            ly=re.search(r'[(]layer "?(F[.]Cu|B[.]Cu)"?[)]',seg)
            nt=re.search(r'[(]net ([0-9]+)[)]',seg)
            if not(st and en and wd and ly and nt) or net_names.get(int(nt.group(1)))==a.net:
                continue
            cells=set()
            mark_segment(cells,float(st.group(1)),float(st.group(2)),float(en.group(1)),float(en.group(2)),
                         float(wd.group(1))/2+a.clearance,LAYERS[ly.group(1)],step)
            soft.update(cells)
            blocked.difference_update(cells)
        noseg=text
        for seg in list(balanced_blocks(text,"(segment")):
            noseg=noseg.replace(seg,"")
        blocked.update(extract_obstacles(noseg,a.net,step,a.clearance))
    S=P(round(sx/step),round(sy/step),sl); G=P(round(gx/step),round(gy/step),gl)
    # Endpoints belong to target net; allow a small escape disk.
    # Only free the exact target endpoints. Clearing a disk around them allowed
    # routes to cut through neighboring copper immediately after the pad.
    blocked.discard(S); blocked.discard(G)
    bounds=(floor((min(sx,gx)-a.margin)/step),ceil((max(sx,gx)+a.margin)/step),
            floor((min(sy,gy)-a.margin)/step),ceil((max(sy,gy)+a.margin)/step))
    path=compress(astar(S,G,blocked,bounds,via_cost=a.via_cost,allow_vias=not a.no_vias,soft_blocked=soft,congestion_cost=a.congestion_cost))
    if not path: raise SystemExit("NO_ROUTE")
    print("ROUTE",len(path))
    for p in path: print(f"{p.x*step:.3f},{p.y*step:.3f},{'F.Cu' if p.layer==0 else 'B.Cu'}")
if __name__=="__main__": main()
