#!/usr/bin/env python3
"""PSN-Presepe Rev C - board generator (KiCad 7+ pcbnew API).

Builds the unrouted board from:
  * revb_netlist.json  - pad -> net map extracted from the Rev-B release PCB
  * revb_pads.json     - Rev-B absolute pad positions (kept-in-place parts)
  * the placement table below (relay section re-placed for Rev C)

Rev C changes vs Rev B (see README):
  * Omron G5Q-1 now uses the official KiCad footprint (Rev B footprint was mirrored)
  * G5Q-1 contact mapping fixed: pad 3 = NO, pad 4 = NC (Rev B had them swapped)
  * ULN2803 now uses the standard DIP-18 300 mil footprint (Rev B used 400 mil rows)
  * relay section re-placed: every relay sits directly behind its own terminal
  * series resistor RBZ1 (220R) added between D6 and the buzzer

Usage: python3 build_board.py <out_dir>
"""
import json, math, os, sys
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "out"))
os.makedirs(OUT, exist_ok=True)
KILIB = os.environ.get("KICAD_FOOTPRINT_DIR", "/usr/share/kicad/footprints")
LOCAL = os.path.join(ROOT, "lib", "PSN_RevC.pretty")
NAME = "PSN-Presepe-Mega-RevC"

NET = json.load(open(os.path.join(ROOT, "data", "revb_netlist.json")))
VAL = json.load(open(os.path.join(ROOT, "data", "revb_values.json")))
PADPOS = json.load(open(os.path.join(ROOT, "data", "revb_pads.json")))

mm = pcbnew.FromMM

# ---------------------------------------------------------------- netlist fixes
# 1) G5Q-1 contacts: pad 3 = NO, pad 4 = NC (KiCad Relay.lib G5Q-1 / G5Q-1A).
for i in range(1, 17):
    k = NET[f"K{i}"]
    assert k["3"] == f"R{i}_NC" and k["4"] == f"R{i}_NO", k
    k["3"], k["4"] = f"R{i}_NO", f"R{i}_NC"
# 2) buzzer series resistor
assert NET["BZ1"]["1"] == "D6_BUZZER"
NET["BZ1"]["1"] = "BUZZER_DRV"
NET["RBZ1"] = {"1": "D6_BUZZER", "2": "BUZZER_DRV"}
VAL["RBZ1"] = "220R"
VAL["U1"] = VAL["U2"] = "ULN2803A"
VAL["BZ1"] = "BUZZER_PASSIVE_RM7.6"

# ---------------------------------------------------------------- footprints
LIB = {
    "MCU1": (LOCAL, "Arduino_Mega2560_R3_Shield"),
    "U": (KILIB + "/Package_DIP.pretty", "DIP-18_W7.62mm"),
    "K": (KILIB + "/Relay_THT.pretty", "Relay_SPDT_Omron-G5Q-1"),
    "Q": (KILIB + "/Package_TO_SOT_THT.pretty", "TO-220-3_Vertical"),
    "R": (KILIB + "/Resistor_THT.pretty", "R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal"),
    "C1": (KILIB + "/Capacitor_THT.pretty", "C_Radial_D10.0mm_H12.5mm_P5.00mm"),
    "C": (KILIB + "/Capacitor_THT.pretty", "C_Disc_D5.0mm_W2.5mm_P5.00mm"),
    "BZ1": (KILIB + "/Buzzer_Beeper.pretty", "Buzzer_12x9.5RM7.6"),
    "RV1": (KILIB + "/Potentiometer_THT.pretty", "Potentiometer_Alps_RK09K_Single_Horizontal"),
    "H": (KILIB + "/MountingHole.pretty", "MountingHole_3.2mm_M3"),
}
def term(n):
    return (KILIB + "/TerminalBlock_Phoenix.pretty",
            f"TerminalBlock_Phoenix_MKDS-1,5-{n}-5.08_1x{n:02d}_P5.08mm_Horizontal")

def lib_for(ref):
    if ref in LIB: return LIB[ref]
    if ref.startswith("JR"): return term(3)
    if ref.startswith("J"): return term(len(NET[ref]))
    if ref.startswith(("RG", "RPD", "RBZ")): return LIB["R"]
    return LIB[ref.rstrip("0123456789")]

# ---------------------------------------------------------------- placement
# Relay section geometry (all mm). See README "Relay section".
P = 19.3            # relay / terminal pitch (both rows)
TOP_X0 = 140.2      # K1 pad-1 x
TOP_YC = 53.0       # top row coil-pad y
TOP_YT = 25.5       # top row terminal pad y   (wire entry towards y=20 edge)
COL_X0 = 289.0      # column relays pad-1 x
COL_Y0 = 45.0       # K9 pad-1 y
COL_T = 314.8       # column terminal pad x    (wire entry towards x=320 edge)

PLACE = {}  # ref -> (x, y, rot)
for i in range(8):
    x0 = TOP_X0 + P * i
    PLACE[f"K{i+1}"] = (x0, TOP_YC, 90)
    PLACE[f"JR{i+1}"] = (x0 + 2.54, TOP_YT, 180)
for j in range(8):
    y0 = COL_Y0 + P * j
    PLACE[f"K{j+9}"] = (COL_X0, y0, 0)
    PLACE[f"JR{j+9}"] = (COL_T, y0 + 2.54, 90)
PLACE.update({
    "U1": (133.0, 62.0, 0), "U2": (133.0, 92.0, 0),
    "C2": (133.3, 86.0, 0), "C3": (133.3, 116.5, 0), "C1": (122.0, 121.0, 0),
    "H1": (26.0, 26.0, 0), "H2": (118.0, 26.0, 0), "H3": (100.0, 182.0, 0),
    "H4": (250.0, 192.0, 0), "H5": (210.0, 120.0, 0), "H6": (135.0, 170.0, 0),
    # user parts moved to the free left area (shaft of RV1 points to the x=20 edge)
    "RV1": (32.0, 138.0, 0), "BZ1": (26.0, 160.0, 0), "RBZ1": (25.0, 172.0, 0),
})
NEW_PARTS = {}
# MOSFET block: 3 x 3 cells, each = RG (top) + RPD (bottom) left of the TO-220
for n in range(9):
    c, rw = n % 3, n // 3
    qx, qy = 56.2 + 28 * c, 135.0 + 15 * rw
    PLACE[f"Q{n+1}"] = (qx, qy, 0)
    PLACE[f"RG{n+1}"] = (qx - 14.2, qy - 1.6, 0)
    PLACE[f"RPD{n+1}"] = (qx - 14.2, qy + 1.6, 0)

def load(ref):
    lp, name = lib_for(ref)
    fp = pcbnew.FootprintLoad(lp, name)
    if fp is None: raise SystemExit(f"cannot load {lp}:{name} for {ref}")
    return fp

def pad_local(fp):
    return {p.GetNumber(): (p.GetPosition().x / 1e6, p.GetPosition().y / 1e6)
            for p in fp.Pads() if p.GetNumber()}

def fit_to_revb(fp, ref):
    """Rotate/translate a library footprint so its numbered pads land on the
    Rev-B absolute pad positions (parts that are not moved in Rev C)."""
    target = PADPOS[ref]
    best = None
    for rot in (0, 90, 180, 270):
        fp.SetOrientationDegrees(rot); fp.SetPosition(pcbnew.VECTOR2I(0, 0))
        loc = pad_local(fp)
        common = [n for n in target if n in loc]
        if not common: continue
        n0 = common[0]
        dx = target[n0][0] - loc[n0][0]; dy = target[n0][1] - loc[n0][1]
        err = max(math.hypot(loc[n][0] + dx - target[n][0], loc[n][1] + dy - target[n][1]) for n in common)
        if best is None or err < best[0]: best = (err, rot, dx, dy)
    err, rot, dx, dy = best
    fp.SetOrientationDegrees(rot); fp.SetPosition(pcbnew.VECTOR2I(mm(dx), mm(dy)))
    return err

board = pcbnew.BOARD()
board.SetCopperLayerCount(2)
nets = {}
def net(name):
    if name not in nets:
        ni = pcbnew.NETINFO_ITEM(board, name); board.Add(ni); nets[name] = ni
    return nets[name]

refs = sorted(set(NET) | set(PADPOS) | set(PLACE) | set(NEW_PARTS))
report = []
for ref in refs:
    fp = load(ref)
    fp.SetReference(ref)
    fp.SetValue(VAL.get(ref, fp.GetValue()))
    board.Add(fp)
    if ref in PLACE:
        x, y, r = PLACE[ref]
        fp.SetOrientationDegrees(r); fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    elif ref in NEW_PARTS:
        x, y, r = NEW_PARTS[ref]
        fp.SetOrientationDegrees(r); fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    else:
        err = fit_to_revb(fp, ref)
        if err > 0.05:
            report.append(f"WARN {ref}: library pads differ from Rev-B by {err:.3f} mm")
    for p in fp.Pads():
        n = NET.get(ref, {}).get(p.GetNumber())
        if n: p.SetNet(net(n))
    # reference designators: terminals/holes use the generated labels instead
    if ref.startswith(("H", "J")):
        fp.Reference().SetLayer(pcbnew.F_Fab)
    elif ref.startswith(("RG", "RPD", "RBZ", "C2", "C3")):
        ps = [p.GetPosition() for p in fp.Pads()]
        fp.Reference().SetPosition(pcbnew.VECTOR2I((ps[0].x + ps[1].x) // 2, (ps[0].y + ps[1].y) // 2))
        fp.Reference().SetTextSize(pcbnew.VECTOR2I(mm(0.8), mm(0.8))); fp.Reference().SetTextThickness(mm(0.12))
        fp.Reference().SetTextAngleDegrees(0)

# verify every netlist entry landed on a pad
for ref, pads in NET.items():
    fp = board.FindFootprintByReference(ref)
    have = {p.GetNumber() for p in fp.Pads()}
    miss = [n for n in pads if n not in have]
    if miss: raise SystemExit(f"{ref}: netlist pads {miss} not in footprint")

# ---------------------------------------------------------------- outline
def seg(layer, a, b, w=0.15):
    s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(pcbnew.VECTOR2I(mm(a[0]), mm(a[1]))); s.SetEnd(pcbnew.VECTOR2I(mm(b[0]), mm(b[1])))
    s.SetLayer(layer); s.SetWidth(mm(w)); board.Add(s); return s
X0, Y0, X1, Y1 = 20, 20, 320, 200
for a, b in (((X0, Y0), (X1, Y0)), ((X1, Y0), (X1, Y1)), ((X1, Y1), (X0, Y1)), ((X0, Y1), (X0, Y0))):
    seg(pcbnew.Edge_Cuts, a, b, 0.1)

# ---------------------------------------------------------------- silkscreen
def text(s, x, y, size=1.0, rot=0, layer=pcbnew.F_SilkS, thick=None):
    t = pcbnew.PCB_TEXT(board); t.SetText(s)
    t.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y))); t.SetLayer(layer)
    t.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size)))
    t.SetTextThickness(mm(thick if thick else max(0.12, size * 0.15)))
    t.SetTextAngleDegrees(rot); board.Add(t); return t

def padpos(ref, num):
    fp = board.FindFootprintByReference(ref)
    for p in fp.Pads():
        if p.GetNumber() == num: return p.GetPosition().x / 1e6, p.GetPosition().y / 1e6

LABELS = {
    "J1": ["12V", "GND"], "J_OLED": ["5V", "GND", "SDA", "SCL"],
    "J_START": ["START", "GND"], "J_NEXT": ["NEXT", "GND"], "J_TEST": ["TEST", "GND"],
    "J_CIELO": ["12V", "R", "G", "B"], "J_TRAMONTO": ["12V", "R", "G", "B"],
    "J_ALBA": ["12V", "R", "G", "B"], "J_STELLE": ["12V", "GND", "DATA"],
    "J_CASETTE": ["12V", "GND", "DATA"],
}
TITLE = {"J1": "POWER 12V", "J_OLED": "OLED", "J_START": "START", "J_NEXT": "NEXT",
         "J_TEST": "TEST", "J_CIELO": "CIELO", "J_TRAMONTO": "TRAMONTO", "J_ALBA": "ALBA",
         "J_STELLE": "STELLE", "J_CASETTE": "CASETTE"}
for ref, labs in LABELS.items():
    for k, s in enumerate(labs, 1):
        x, y = padpos(ref, str(k)); text(s, x, y - 7.3, 0.9)
    x1, y1 = padpos(ref, "1"); xn, _ = padpos(ref, str(len(labs)))
    text(TITLE[ref], (x1 + xn) / 2, y1 - 9.0, 1.0)
for i in range(1, 17):
    ref = f"JR{i}"
    if i <= 8:
        for num, s_ in (("1", "COM"), ("2", "NO"), ("3", "NC")):
            x, y = padpos(ref, num); text(s_, x, y + 6.5, 0.8)
        x, y = padpos(ref, "3"); text(f"R{i}", x - 3.6, y + 6.5, 0.9)
    else:
        x, y = padpos(ref, "1")
        text(f"R{i}: NC/NO/COM", 314.6, y + 4.6, 0.8)
    for num, s_ in (("1", "COM"), ("2", "NO"), ("3", "NC")):   # back-side labels behind each pad
        x, y = padpos(ref, num)
        t = text(s_, x, y + (3.2 if i <= 8 else 0), 0.8, layer=pcbnew.B_SilkS, rot=0 if i <= 8 else 90)
        if i > 8: t.SetPosition(pcbnew.VECTOR2I(mm(x - 2.8), mm(y)))
        t.SetMirrored(True)
text("!  RELAY CONTACTS MAY CARRY 230 V AC  -  SELV KEEP-OUT 6 mm  !", 222, 160, 1.2)
text("PSN-Presepe Rev C", 222, 145, 2.0)
text("MOSFET / HEATSINK AIRFLOW ZONE", 85.5, 127.6, 0.9)


# ---------------------------------------------------------------- save
out_pcb = os.path.join(OUT, NAME + ".kicad_pcb")
pcbnew.SaveBoard(out_pcb, board)
print("saved", out_pcb, "footprints", len(board.GetFootprints()), "nets", len(nets))
for r in report: print(r)
