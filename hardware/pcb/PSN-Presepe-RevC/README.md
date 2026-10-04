# PSN-Presepe PCB — Rev C (manufacturing package)

Rev C supersedes Rev B. It fixes the Rev B blocking defects, and every step of the
build is checked by KiCad DRC plus two independent checkers (one on the board file,
one on the Gerber/Excellon files the fab will actually use).

**Status: official Rev C source and manufacturing candidate.** The accepted design target is 6 mm MAINS-to-SELV, 5 mm between different relay contact circuits, and 2 mm within the same relay contact circuit. Final ordering remains gated by KiCad 10 CI plus the pre-order checklist below. That checklist
is a 1:1 paper fit test and confirming the exact part numbers.

## 1. What changed from Rev B

| # | Rev B defect | Rev C fix |
|---|---|---|
| 1 | **Omron G5Q-1 footprint was mirrored** (pads 4/5 on the wrong side). The relays could not be inserted. | Official KiCad footprint `Relay_THT:Relay_SPDT_Omron-G5Q-1` (top view). Verified against the KiCad library hole pattern. |
| 2 | **NO/NC swapped**: relay pad 3 was wired as NC and pad 4 as NO. The terminal marked "NO" was really NC. | G5Q-1 pad 3 = **NO**, pad 4 = **NC** (per the KiCad `Relay` symbol lib G5Q-1 and the G5Q-1A, which is the NO-only version that keeps pin 3). Terminals are still 1 = COM, 2 = NO, 3 = NC. |
| 3 | **ULN2803 footprint had 10.16 mm (400 mil) rows.** The DIP-18 package could not be inserted. | Standard `Package_DIP:DIP-18_W7.62mm` (300 mil). |
| 4 | **Relay isolation rule never ran.** The rules used `=~` regular expressions, which KiCad custom rules do not support, so they matched nothing. The CI also only counted the rule lines in the file. Measured contact copper was down to 0.20 mm from other relays, +12 V and logic. | New wildcard-based rules: **6 mm** between relay contacts and everything else, **5 mm** between different relays, **2 mm** between COM/NO/NC of the same relay, **3 mm** to the board edge, **6 mm** to non-MAINS holes. A positive control shows each rule is active: forcing each rule to an impossible value makes the DRC flag it (`reports/positive-control-summary.txt`). |
| 5 | **Relay contact traces up to 185 mm long**, bundled across the board between other circuits. | Relay section re-placed so **each relay sits directly behind its own terminal block**. Contact paths are 10–25 mm long, drawn on **both layers at 2 mm**, with no vias. |
| 6 | Buzzer driven directly from D6. A 16–42 Ω magnetic buzzer would overload the pin and the Mega 5 V regulator. | `RBZ1` 220 Ω added in series (net `BUZZER_DRV`). Safe with a piezo or a magnetic buzzer. |
| 7 | MOSFET block courtyards overlapped: resistor leads sat under the TO-220 bodies. | MOSFET block re-laid out as 3×3 cells (RG + RPD to the left of each TO-220). No courtyard overlaps. |
| 8 | Rev B `.kicad_sch`: every global label sat at the **vertically mirrored** pin position (library Y axis points up). The schematic netlist did not match the PCB (for example J1 +12V on pin 2). | Schematic regenerated from the PCB. A KiCad-exported netlist matches the PCB pin-for-pin: 315/315 pins, 0 mismatches. |

Unchanged:
- All 119 Rev B nets and the firmware pin map (D2–D8, D11/D12, D20–D46, A0, VIN). This is checked by parsing `PSN-Presepe.ino`.
- Board outline 300 × 180 mm, 2 layers.
- Low-voltage terminal positions.
- The Mega 2560 shield footprint and the MOSFET circuit.

## 2. Electrical design summary

| Net class | Width | Clearance | Notes |
|---|---|---|---|
| MAINS (R*_COM/NO/NC) | 2.0 mm on F.Cu **and** B.Cu | 6 mm to SELV, 5 mm between relays, 2 mm within a relay | No vias. Locked tracks. |
| POWER (+12V, GND) | **3 mm trunks**, 1 mm branches | 0.3 mm | Trunks: J1 to the strip terminals (CIELO/TRAMONTO/ALBA/STELLE/CASETTE), and the MOSFET sources back to J1, with 1.5 mm stubs into the TO-220 pins. Branches carry < 0.6 A: relay coils, ULN COM, Mega VIN, caps. |
| RGB (*_NEG) | 1.5 mm | 0.3 mm | MOSFET drain to the strip terminal, about 1.7 A per channel. |
| P5V (+5V_MEGA) | 0.8 mm | 0.25 mm | |
| COIL | 0.4 mm | 0.2 mm | 33 mA per coil. |
| Signals | 0.25 mm | 0.2 mm | |

Current capacity (IPC-2221, external layer, 10 °C rise, 1 oz):
- 3 mm trunk: about 5.3 A.
- 1.5 mm RGB: about 3.2 A.
- Relay contact (2 × 2 mm, both layers): about 7.9 A.

With **2 oz copper (recommended)** these roughly double. This gives margin over the 5.5 A board budget and lets the relay channels use more of their 10 A rating. The IRLZ44N dissipates about 0.1 W at 1.7 A, so no heatsink is needed.

The isolation distances are a conservative design target for 230 V AC, pollution degree 2, FR-4. They are **not a safety certification**. Use a closed enclosure, put fuses on the mains feed, use wire rated for the load, and keep mains wiring away from the low-voltage side.

## 3. Verification (all in `reports/`)

| Check | Tool | Result |
|---|---|---|
| DRC with project rules + `.kicad_dru` | KiCad 7.0.11 pcbnew | **0 violations, 0 unconnected** |
| Each isolation rule actually active | KiCad DRC, one rule forced impossible per run | selv / inter / intra / edge all fire |
| Board geometry: shorts, clearances by class, connectivity, holes, edge, widths, pinout, footprint patterns, netlist parity with Rev B + listed changes, firmware pins, Mega keep-out | `build/verify.py` (shapely, no KiCad) | **ALL CHECKS PASSED** |
| Manufacturing files: Gerber copper islands vs X2 net attributes, clearances incl. MAINS, annular rings, NPTH, mask openings, tented vias, outline | `build/verify_gerbers.py` (gerbonara, no KiCad) | **ALL GERBER CHECKS PASSED** |
| Schematic ↔ PCB | `kicad-cli sch export netlist` + `check_sch_parity.py` | 315/315 pins match |

Project decision (2026-10-04): the 5 mm inter-relay target is accepted for Rev C; the measured 5.23 mm is therefore compliant and is not a waiver. The 6 mm target remains mandatory between relay-contact copper and SELV.

Measured minimum distances:

| Pair | Measured | Required |
|---|---|---|
| MAINS ↔ SELV | 6.30 mm | 6 |
| MAINS between relays | 5.23 mm | 5 |
| MAINS within a relay | 2.15 mm | 2 |
| MAINS ↔ mounting holes | 11.7 mm | — |

Not done here:
- **ERC**, because `kicad-cli` 7 has no `sch erc`. Run it in KiCad 8/9/10. The schematic is pure net labels, so the only expected messages are annotation notes about the `J_*` references, which have no trailing number.
- The build used **KiCad 7.0.11**, because this environment could not download KiCad 10. KiCad 10 opens these files and converts them on save. Re-running the DRC in KiCad 10 before ordering is a good final cross-check.

## 4. Ordering (e.g. JLCPCB / PCBWay / Aisler)

Upload `manufacturing/PSN-Presepe-Mega-RevC-gerbers.zip` (Gerber X2 + Excellon PTH/NPTH, Protel extensions) with these settings:

- 2 layers, 300 × 180 mm, FR-4 1.6 mm.
- **2 oz outer copper (recommended; 1 oz acceptable).**
- HASL or ENIG finish, any mask colour, white silkscreen.
- Minimum track/space 0.25/0.2 mm. Minimum drill 0.3 mm (vias), no castellations.

The board is all through-hole, so assembly is by hand. `CPL.csv` is included only for completeness.

## 5. Pre-order checklist

1. **Print `manufacturing/PSN-Presepe-Mega-RevC-1to1-A3-top.pdf` at 100 % on A3.** Check the scale with a ruler (300 mm outline). Push a real G5Q-1, a ULN2803 (or its socket), a 3-way MKDS terminal, an IRLZ44N, the RK09K potentiometer and the buzzer through the paper.
2. Confirm the exact order codes:
   - G5Q-1 **DC12** suffix (the standard G5Q-1 has the 10 A contact).
   - The terminal block series, with 5.08 mm pitch and wire entry towards the board edge.
   - The buzzer pitch (7.6 mm).
3. Wire entry: all terminals face outward (top row up, right column right, bottom row down). This was verified against the KiCad 3D model of the MKDS 1,5 horizontal terminal.
4. Put a strip of Kapton tape on the Mega USB-B shell. There are no vias above it, but the bottom-side tracks are only covered by solder mask.

## 6. Firmware notes (no change required)

- Relay outputs are unchanged (D25–D40, active HIGH through the ULN2803).
- The terminal labelled **NO** is now really normally-open. Rev B boards would have behaved inverted.
- `POT_RAW_MAX = 680` was measured on the breadboard. On this PCB, RV1 runs from GND to +5 V, so the ADC reaches about 1023. The code still works because readings are clamped, but the three speed zones sit in the lower two thirds of the rotation. Set `POT_RAW_MAX = 1023` if you want them evenly spread.

## 7. Package contents

```
manufacturing/   gerbers zip, BOM, CPL, 1:1 A3 print, drill maps
kicad/           PSN-Presepe-Mega-RevC.kicad_pro / .kicad_pcb / .kicad_dru / .kicad_sch (+ schematic PDF), lib/
reports/         KiCad DRC, positive controls, independent board + Gerber checks, schematic parity
previews/        top, bottom, copper, assembly renders
build/           complete, portable build scripts + input data (see below)
```

## 8. Rebuilding (portable, command-line paths)

Requirements:
- KiCad ≥ 7 with the Python `pcbnew` module, `kicad-cli` and the standard footprint libraries.
- Python 3 with `shapely`, `sexpdata`, `numpy`, `pillow` and `gerbonara`.
- Only to re-run the autorouter: Java 25 and Freerouting 2.2.4.

```sh
# reproduce the released board exactly from the stored routing session
SES_IN=build/data/routing.ses build/scripts/pipeline.sh /tmp/revc
# or re-route from scratch (results vary run to run; DRC + completion router handle leftovers)
PASSES=60 build/scripts/pipeline.sh /tmp/revc /path/freerouting-2.2.4.jar /path/java25/bin/java
# export the manufacturing package and run every verification
KICAD_FOOTPRINT_DIR=/usr/share/kicad/footprints \
  build/scripts/make_release.sh /tmp/revc/final.kicad_pcb /tmp/revc-release /path/PSN-Presepe.ino
```

Pipeline steps:
1. `build_board.py`: placement and netlist, including the Rev C fixes.
2. `make_rules.py`: net classes and isolation rules.
3. `route_mains.py`: deterministic relay-contact and power-trunk routing, plus 6 mm keep-outs for the router.
4. Freerouting for the SELV nets.
5. `import_ses.py`.
6. `complete_routes.py`: a rule-aware grid router for any leftover connection.
7. DRC.
