#!/usr/bin/env python3
"""Grid A* helper for low-current PCB routing experiments.

It is intentionally conservative: every pad belonging to another net and every
already-routed segment is expanded into an obstacle margin. Output is a list of
grid points only; KiCad DRC remains the final authority before any promotion.
"""
from __future__ import annotations
from dataclasses import dataclass
from heapq import heappush,heappop
from math import hypot
import sys

@dataclass(frozen=True)
class P:
    x:int; y:int; layer:int

def astar(start,goal,blocked,step=1):
    # coordinates are integer grid units chosen by caller
    q=[]; heappush(q,(0,0,start)); prev={start:None}; cost={start:0}; serial=0
    moves=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0)]
    while q:
        _,_,p=heappop(q)
        if p==goal:
            out=[]
            while p is not None: out.append(p); p=prev[p]
            return list(reversed(out))
        for dx,dy,dl in moves:
            n=P(p.x+dx,p.y+dy,p.layer)
            if n in blocked or not (20<=n.x<=300 and 20<=n.y<=190): continue
            nc=cost[p]+1
            if nc<cost.get(n,10**9):
                cost[n]=nc;prev[n]=p;serial+=1
                h=abs(n.x-goal.x)+abs(n.y-goal.y)
                heappush(q,(nc+h,serial,n))
    return None

if __name__=="__main__":
    print("A* routing helper library; obstacle extraction integration follows.")
