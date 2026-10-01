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
Official PCB: **K1-K16 + D25 + D26 + D27 / 151 unconnected**. D27 final candidate `fc0e3274...`, run `36861858225` SUCCESS; promoted `f2e4c50a...`, sanity `0a6bfe6f...`.

D28 best structural probe is `20a17bb0...`: 151->150, zero crossings, only one short + two mask bridges. The remaining obstacle is the physical Mega header itself: unused/no-net D42/D43 pads at y=69.14. Restart by routing D28 below the **entire** digital header rather than below D40, then return toward U1.4; preserve validated D25-D27.

Final delivery gate remains: zero real DRC + zero unconnected, then generate same-revision assembly package **Gerber+Excellon ZIP + BOM + CPL/centroid**, cross-check reference designators and revision consistency.

Keep +12V/GND distribution, relay COM/NO, high-current copper and pours untouched until their dedicated reviewed phase.
