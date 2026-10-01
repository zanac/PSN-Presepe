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
Official PCB: **K1-K16 + D25 + D26 complete / 152 unconnected / zero critical routing DRC on promoted routes**. D25 clean candidate `c38f647f...` promoted `927f3d8c...`; D26 clean candidate `02ed5d90...` promoted `d3f6b0a3...`; sanity through net21 at `0ad9e773...`.

Fanout topology established: MCU->U1 crosses F.Cu wall net16 on B.Cu, changes layer in x≈129.5 channel, then crosses B.Cu wall net17 on F.Cu. D27 current candidate `e154a246...` reduces 152->151 with no short/clearance but 4 known crossings (artifact `11160176400`): D22_START F at (130.5,54), D26 B y=50.09, D26 F x=131.5, D26 F horizontal y=64.54. Redesign D27 around these exact obstacles, preferably comb-style; preserve validated D25/D26 unless an atomic repack is DRC-clean.

Continue D27..D32 low-risk input fanout. Keep +12V/GND, COM/NO, high-current copper and pours untouched.
