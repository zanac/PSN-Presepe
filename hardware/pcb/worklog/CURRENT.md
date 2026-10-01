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
Official board promotion completed on `dev` at commit `cf84acada8c95eb92ad755395199ef8dcfbbcb3d`: the second validated Freerouting delta reduced connectivity from **122 to 120 unconnected pads (-2)** with no new critical DRC categories.

The two newly solved logic connections are:
- `D36_RELAY12`: MCU1 D36 -> U2 pad 4.
- `CIELO_G_NEG`: Q2 pad 2 -> J_CIELO pad 3.

Exactly **3 logic connections remain**:
- `TRAM_R_NEG`
- `TRAM_G_NEG`
- `ALBA_B_NEG`

The remaining 117 non-logic unconnected reports are still the planned **48 relay-contact + 69 power** routing workload. Close these 3 logic stragglers with targeted candidates and real KiCad DRC before relay-contact routing, then power buses/zones.

Validated artifact for the 122->120 delta: run `36898305562`, artifact `11180751893`; promotion run `36900932623` completed successfully. Keep autoroute artifact-only and protected power/contact nets stripped.

Final fabrication gate remains zero real DRC + zero unconnected -> same-revision Gerber+Excellon ZIP + BOM CSV + CPL/centroid CSV.

Progress checkpoint after 122->120 promotion: ~66% routing / ~76% overall PCB.