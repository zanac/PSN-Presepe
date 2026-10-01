# PCB work checkpoint

This file is the short restart point for long autonomous PCB sessions.

## Current baseline
- Branch: `dev`.
- Official board: `hardware/pcb/kicad/PSN-Presepe-Mega.kicad_pcb`.
- Official board contains K1-K12 coil-low routing; K12 added six track segments plus one via after K11 baseline.
- Routing is being promoted only after a temporary candidate passes real KiCad DRC.
- K1-K13 relay coil-low routes are promoted and sanity-approved. K14 is in candidate validation.
- Gerber fabrication gate remains blocked until DRC has no real errors and connectivity is complete.

## Restart procedure
1. Fetch HEAD versions of this file, `make_route_candidate.py`, `pcb_sanity.py`, PCB and workflow.
2. Inspect the newest `pcb-kicad.yml` Actions run and its logs/artifacts.
3. Never assume a candidate was promoted merely from its script: confirm the official PCB segment count and sanity allow-list.
4. If candidate DRC is clean and reduces connectivity, promote only that verified route in a dedicated commit.
5. Update this checkpoint after each meaningful routing milestone.
6. Keep experimental generated boards out of the official PCB; CI build paths are disposable.

## Commit discipline
Use small commits with one purpose:
- `WIP candidate: <net>` for experiment infrastructure or route candidate;
- `Promote KiCad-validated <net> route` only after clean candidate DRC;
- `Checkpoint PCB routing state` for this restart log;
- documentation/tooling changes separately from electrical PCB changes.

## Safety invariants
- Do not blind-route relay contact/mains-capable nets.
- No unreviewed copper zones.
- Preserve perimeter terminal placement and MOSFET heatsink spacing.
- Keep the explicit fabrication gate; never generate production Gerbers from an incomplete board.
- Fetch HEAD immediately before every PCB/tool/workflow update to avoid overwriting concurrent work.

## Next action
Official PCB: **K1-K16 + D25-D28 / 150 unconnected / zero critical geometry/electrical DRC**. D28 candidate 61fcb1d6... run 36865837527 SUCCESS; promoted 095233fc...; sanity dc2b5e92.... Official validation observed in run 36866316897: only 66 footprint mismatches + 150 unconnected.

D28 established a reusable wall-crossing concept: F.Cu crosses D24_TEST(B), via before D22_START(F), B.Cu crosses START, via between START/NEXT, F.Cu crosses D23_NEXT(B). Its analog-row corridor is x=110.55 between A11/A12 and wall-crossing y=92.

D29 first clone c4d7cec6... is rejected despite 150->149: it touches D30, crosses D28, touches U2.1/D33, and crosses D28 right ascent. Next D29 should use a distinct escape (prefer right/vertical or coordinated D29+D30) while retaining the validated alternating-layer wall-crossing principle. Do not modify official D28 unless an atomic replacement is fully DRC-clean.

Final gate: zero real DRC + zero unconnected, then same-revision **Gerber+Excellon ZIP + BOM + CPL/centroid**, with reference/revision cross-check.

Keep +12V/GND distribution, relay COM/NO, high-current copper and pours untouched until dedicated reviewed phase.
