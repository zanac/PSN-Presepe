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

def astar(start,goal,blocked,bounds,via_cost=18):
    q=[]; serial=0; heappush(q,(0,serial,start)); prev={start:None}; cost={start:0}
    xmin,xmax,ymin,ymax=bounds
    moves=[(1,0,0,10),(-1,0,0,10),(0,1,0,10),(0,-1,0,10),
           (1,1,0,14),(1,-1,0,14),(-1,1,0,14),(-1,-1,0,14),(0,0,1,via_cost)]
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

def extract_obstacles(text,target,step,clearance):
    blocked=set()
    # KiCad v20240108-style segment records.
    seg_re=re.compile(r'\(segment\s+\(start ([\d.-]+) ([\d.-]+)\)\s+\(end ([\d.-]+) ([\d.-]+)\)\s+\(width ([\d.-]+)\)\s+\(layer "?(F\.Cu|B\.Cu)"?\).*?\(net (\d+)\)',re.S)
    net_names={int(n):name for n,name in re.findall(r'^\s*\(net (\d+) "([^"]+)"\)\s*$',text,re.M)}
    for m in seg_re.finditer(text):
        x1,y1,x2,y2,w,la,n=m.groups(); n=int(n)
        if net_names.get(n)==target: continue
        mark_segment(blocked,*map(float,(x1,y1,x2,y2)),float(w)/2+clearance,LAYERS[la],step)
    # All vias are treated as through-hole copper obstacles unless on target net.
    via_re=re.compile(r'\(via\s+\(at ([\d.-]+) ([\d.-]+)\).*?\(size ([\d.-]+)\).*?\(net (\d+)\)',re.S)
    for m in via_re.finditer(text):
        x,y,size,n=m.groups(); n=int(n)
        if net_names.get(n)==target: continue
        mark_disc(blocked,float(x),float(y),float(size)/2+clearance,[0,1],step)
    # Conservative approximation for foreign through-hole pads: locate pad blocks with net.
    pad_re=re.compile(r'\(pad\s+"?[^"]*"?\s+thru_hole.*?\(at ([\d.-]+) ([\d.-]+)(?: [\d.-]+)?\).*?\(size ([\d.-]+) ([\d.-]+)\).*?\(net (\d+) "([^"]+)"\)',re.S)
    for m in pad_re.finditer(text):
        x,y,sx,sy,n,name=m.groups()
        if name==target: continue
        mark_disc(blocked,float(x),float(y),max(float(sx),float(sy))/2+clearance,[0,1],step)
    return blocked

def compress(path):
    if not path:return path
    out=[path[0]]
    for i in range(1,len(path)-1):
        a,b,c=path[i-1],path[i],path[i+1]
        d1=(b.x-a.x,b.y-a.y,b.layer-a.layer); d2=(c.x-b.x,c.y-b.y,c.layer-b.layer)
        if d1!=d2: out.append(b)
    out.append(path[-1]); return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("pcb"); ap.add_argument("--net",required=True)
    ap.add_argument("--start",required=True,help="x,y,layer"); ap.add_argument("--goal",required=True)
    ap.add_argument("--step",type=float,default=.5); ap.add_argument("--clearance",type=float,default=.35)
    ap.add_argument("--margin",type=float,default=15)
    a=ap.parse_args(); text=Path(a.pcb).read_text()
    def pt(s):
        x,y,la=s.split(","); return float(x),float(y),LAYERS[la]
    sx,sy,sl=pt(a.start); gx,gy,gl=pt(a.goal); step=a.step
    blocked=extract_obstacles(text,a.net,step,a.clearance)
    S=P(round(sx/step),round(sy/step),sl); G=P(round(gx/step),round(gy/step),gl)
    # Endpoints belong to target net; allow a small escape disk.
    for p in list(blocked):
        if hypot(p.x*step-sx,p.y*step-sy)<1.2 or hypot(p.x*step-gx,p.y*step-gy)<1.2: blocked.discard(p)
    bounds=(floor((min(sx,gx)-a.margin)/step),ceil((max(sx,gx)+a.margin)/step),
            floor((min(sy,gy)-a.margin)/step),ceil((max(sy,gy)+a.margin)/step))
    path=compress(astar(S,G,blocked,bounds))
    if not path: raise SystemExit("NO_ROUTE")
    print("ROUTE",len(path))
    for p in path: print(f"{p.x*step:.3f},{p.y*step:.3f},{'F.Cu' if p.layer==0 else 'B.Cu'}")
if __name__=="__main__": main()
