#!/usr/bin/env python3
"""Deterministic routing of the 48 relay-contact (MAINS) nets.

Every relay sits directly behind its own terminal block, so each contact is a
short dedicated path. Each path is drawn on BOTH copper layers (2 mm each) for
current capacity. Tracks are locked so the autorouter cannot move them.

Usage: route_mains.py <in.kicad_pcb> <out.kicad_pcb> [<keepout_out.kicad_pcb>]
The optional third file additionally contains 6 mm SELV keep-out rule areas
around all MAINS copper; it is only used as autorouter input.
"""
import sys, pcbnew
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

mm = pcbnew.FromMM
src, dst = sys.argv[1], sys.argv[2]
keep = sys.argv[3] if len(sys.argv) > 3 else None
b = pcbnew.LoadBoard(src)

# must match build_board.py
P, TOP_X0, TOP_YC, TOP_YT = 19.3, 140.2, 53.0, 25.5
COL_X0, COL_Y0, COL_T = 289.0, 45.0, 314.8
W = 2.0
J = 4.3   # COM detour offset (keeps >= 2 mm from the NO pad of the same relay)

paths = {}
for i in range(8):
    x0, k = TOP_X0 + P * i, i + 1
    paths[f"R{k}_NC"] = [(x0 - 7.62, TOP_YC - 15.24), (x0 - 7.62, TOP_YT)]
    paths[f"R{k}_NO"] = [(x0, TOP_YC - 17.78), (x0, TOP_YT + 5.08), (x0 - 2.54, TOP_YT + 2.54), (x0 - 2.54, TOP_YT)]
    paths[f"R{k}_COM"] = [(x0, TOP_YC - 10.16), (x0 + J, TOP_YC - 10.16), (x0 + J, TOP_YT + 1.76), (x0 + 2.54, TOP_YT)]
for j in range(8):
    y0, k = COL_Y0 + P * j, j + 9
    x = COL_X0
    paths[f"R{k}_NC"] = [(x + 15.24, y0 - 7.62), (COL_T, y0 - 7.62)]
    paths[f"R{k}_NO"] = [(x + 17.78, y0), (x + 17.78 + 2.54, y0 - 2.54), (COL_T, y0 - 2.54)]
    paths[f"R{k}_COM"] = [(x + 10.16, y0), (x + 10.16, y0 + J), (COL_T - 1.76, y0 + J), (COL_T, y0 + 2.54)]

# ---- high-current power trunks (3 mm), drawn on one layer each:
#  +12V  F.Cu  J1.1 -> strip terminals (CIELO/TRAMONTO/ALBA/STELLE/CASETTE pin 1)
#  GND   B.Cu  J1.2 -> WS2811 GND pins and the three MOSFET source columns
YB = 197.5
power = {  # net -> (layer, list of polylines)
    "+12V": ("F", [[(28.0, 194.0), (28.0, YB), (198.0, YB), (198.0, 194.0)]] +
                  [[(x, YB), (x, 194.0)] for x in (108.0, 132.0, 156.0, 180.0)]),
    "GND": ("B", [[(33.08, 194.0), (33.08, YB), (203.08, YB), (203.08, 194.0)],
                  [(185.08, YB), (185.08, 194.0)],
                  [(47.08, YB), (47.08, 194.0)], [(70.08, YB), (70.08, 194.0)],      # OLED/START GND
                  [(83.08, YB), (83.08, 194.0)], [(96.08, YB), (96.08, 194.0)],      # NEXT/TEST GND
                  [(63.28, 135.0), (63.28, 172.0), (61.12, 174.16), (61.12, YB)],     # Q1/Q4/Q7 sources
                  [(91.28, 135.0), (91.28, 172.0), (87.04, 172.0), (87.04, YB)],      # Q2/Q5/Q8
                  [(119.28, 135.0), (119.28, 172.0), (127.6, 172.0), (127.6, YB)]]),  # Q3/Q6/Q9
}
# 1.5 mm neck-down stubs from each MOSFET source pin to its 3 mm riser (TO-220 pitch 2.54)
stubs = [[(qx + 5.08, qy), (qx + 7.08, qy)] for qx in (56.2, 84.2, 112.2) for qy in (135.0, 150.0, 165.0)]
power_ends = {"+12V": [(108.0, 194.0), (132.0, 194.0), (156.0, 194.0), (180.0, 194.0), (198.0, 194.0), (28.0, 194.0)],
              "GND": [(33.08, 194.0), (185.08, 194.0), (203.08, 194.0), (47.08, 194.0), (70.08, 194.0), (83.08, 194.0), (96.08, 194.0)] +
                     [(x, y) for x in (61.28, 89.28, 117.28) for y in (135.0, 150.0, 165.0)]}

# sanity: every path endpoint must sit on a pad of the same net
pads = {}
for fp in b.GetFootprints():
    for p in fp.Pads():
        pads.setdefault(p.GetNetname(), []).append((p.GetPosition().x / 1e6, p.GetPosition().y / 1e6))
for n, pts in paths.items():
    for end in (pts[0], pts[-1]):
        if not any(abs(end[0] - a) < 0.01 and abs(end[1] - c) < 0.01 for a, c in pads.get(n, [])):
            raise SystemExit(f"{n}: path end {end} is not on a {n} pad")
    if len(pads[n]) != 2: raise SystemExit(f"{n}: expected 2 pads, got {len(pads[n])}")

for n, ends in power_ends.items():
    for e in ends:
        if not any(abs(e[0] - a) < 0.01 and abs(e[1] - c) < 0.01 for a, c in pads.get(n, [])):
            raise SystemExit(f"{n}: trunk end {e} is not on a {n} pad")
for n, (lay, polys) in power.items():
    net = b.FindNet(n)
    for pts in polys:
        for a, c in zip(pts, pts[1:]):
            t = pcbnew.PCB_TRACK(b)
            t.SetStart(pcbnew.VECTOR2I(mm(a[0]), mm(a[1]))); t.SetEnd(pcbnew.VECTOR2I(mm(c[0]), mm(c[1])))
            t.SetWidth(mm(3.0)); t.SetLayer(pcbnew.F_Cu if lay == "F" else pcbnew.B_Cu)
            t.SetNet(net); t.SetLocked(True); b.Add(t)
for a, c in stubs:
    t = pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I(mm(a[0]), mm(a[1]))); t.SetEnd(pcbnew.VECTOR2I(mm(c[0]), mm(c[1])))
    t.SetWidth(mm(1.5)); t.SetLayer(pcbnew.B_Cu); t.SetNet(b.FindNet("GND")); t.SetLocked(True); b.Add(t)

geoms = []
for n, pts in paths.items():
    net = b.FindNet(n)
    for layer in (pcbnew.F_Cu, pcbnew.B_Cu):
        for a, c in zip(pts, pts[1:]):
            t = pcbnew.PCB_TRACK(b)
            t.SetStart(pcbnew.VECTOR2I(mm(a[0]), mm(a[1]))); t.SetEnd(pcbnew.VECTOR2I(mm(c[0]), mm(c[1])))
            t.SetWidth(mm(W)); t.SetLayer(layer); t.SetNet(net); t.SetLocked(True); b.Add(t)
    geoms.append(LineString(pts).buffer(W / 2))
pcbnew.SaveBoard(dst, b)
print("MAINS paths:", len(paths), "->", dst)

if keep:
    # 6 mm SELV keep-out around every MAINS track and pad (+0.1 mm margin)
    for fp in b.GetFootprints():
        for p in fp.Pads():
            if p.GetNetClassName() == "MAINS":
                geoms.append(Point(p.GetPosition().x / 1e6, p.GetPosition().y / 1e6).buffer(p.GetSize().x / 2e6))
    area = unary_union(geoms).buffer(6.1, resolution=8).simplify(0.05)
    polys = list(area.geoms) if hasattr(area, "geoms") else [area]
    # a keep-out must never swallow a SELV pad
    for fp in b.GetFootprints():
        for p in fp.Pads():
            if p.GetNetClassName() != "MAINS" and p.GetNetname():
                pt = Point(p.GetPosition().x / 1e6, p.GetPosition().y / 1e6)
                if any(Polygon(pg.exterior).distance(pt) < p.GetSize().x / 2e6 for pg in polys):
                    raise SystemExit(f"SELV pad {fp.GetReference()}.{p.GetNumber()} inside MAINS keep-out")
    for pg in polys:
        z = pcbnew.ZONE(b)
        z.SetIsRuleArea(True); z.SetDoNotAllowTracks(True); z.SetDoNotAllowVias(True)
        z.SetDoNotAllowCopperPour(True); z.SetDoNotAllowPads(False); z.SetDoNotAllowFootprints(False)
        ls = pcbnew.LSET(); ls.AddLayer(pcbnew.F_Cu); ls.AddLayer(pcbnew.B_Cu); z.SetLayerSet(ls)
        ol = z.Outline(); ol.NewOutline()
        for x, y in list(pg.exterior.coords)[:-1]:
            ol.Append(mm(x), mm(y))
        b.Add(z)
    pcbnew.SaveBoard(keep, b)
    print("keep-out areas:", len(polys), "->", keep)
