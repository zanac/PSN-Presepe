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
Official PCB has advanced to **K1-K16 + D25-D30 / 148 unconnected**. D30 clean Route Candidate was run `36875416537` at `d179b53b...` and its validated geometry is now present in the official PCB. Latest official validation is still running; inspect it before treating the 148 baseline as independently revalidated.

D30 final geometry uses complementary y=78.03 alternating-layer bridge and B.Cu final approach. Continue with D31/net26, using the proven D29/D30 staggered inter-row strategy; preserve D25-D30 unless an atomic repack is fully DRC-clean.

Final gate: zero real DRC + zero unconnected, then same-revision **Gerber+Excellon ZIP + BOM CSV + CPL/centroid CSV**, cross-checked by reference/revision. Keep +12V/GND distribution, relay COM/NO, high-current copper and pours untouched until dedicated reviewed phase.
