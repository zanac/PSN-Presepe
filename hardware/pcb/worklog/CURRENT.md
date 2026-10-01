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
**Progress accounting corrected.** Clean official baseline is K1-K16 + D25-D29, **149 unconnected**, full KiCad Validation run `36880034688`: categories only footprint mismatch + unconnected; **zero critical geometry/electrical DRC**.

149 is not 149 equally difficult routes. Exact clean-report decomposition: **GND 37 + +12V 27 + +5V_MEGA 5 = 69 (46%)** are shared power connections suited to buses/zones; **48** are relay contact nets (COM/NO/NC, 3 x 16); **9** relay-input signals remain D30-D40; the remainder are PWM/data/buzzer/MOSFET-side signals. Therefore old ~94% estimate was too optimistic for manufacturing completion. Use current estimates: routing/connectivity ~45-55%, overall PCB ~65-70%, manufacturing-package readiness ~60-65%.

D30 restart candidate `69132e77...` reduced 149->148 but had exactly one short: D30 via at (131.5,78.03) against D29 F.Cu track at x=132. Variant moving via to 131.25 (`060d7da5...`) worsened to 1 short + 3 crossings; reject and do not promote. Official PCB remains clean 149 baseline.

Next routing strategy: do not remain blocked on D30. Define/review a dedicated relay-contact routing class (wider copper/appropriate clearance) and route contact groups with candidate + full DRC; these 48 repetitive connections can materially reduce unconnected count. Resume D30 in parallel from clean baseline when a collision-free wall bridge is found. Do not blindly bulk-route K9-K16 because terminal geometry can require long paths.

Final gate: zero real DRC + zero unconnected, then same-revision Gerber+Excellon ZIP + BOM CSV + CPL/centroid CSV.
