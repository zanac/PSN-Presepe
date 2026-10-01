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
Official PCB remains **K1-K16 + D25 + D26 / 152 unconnected**, independently verified by KiCad Validation run `36858485914`: only 66 footprint mismatches + 152 unconnected; **no critical geometry/electrical DRC**.

D27 best candidate remains `e154a246...`: 152->151, zero short/clearance, four known crossings. Right-side D27 and coordinated D26/D27 repack were worse. D28 isolated even-lane probe was also worse. The x=128.5 F.Cu / x=130.5 B.Cu wall pair plus D25/D26 now makes single-net additions inefficient.

Next: design D27-D32 as a coordinated fanout bus with staggered layer-change stations, using official D25/D26 as baseline. Prefer a multi-net candidate and promote atomically only if connectivity improves by the intended number and routing DRC is zero. Generator restored to best D27 at `a4e29afc4a56b875a72812e5a8a0b55bf0510c06`.

Keep +12V/GND, COM/NO, high-current copper and pours untouched.
