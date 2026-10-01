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
Official PCB: **K1-K15 / 155 unconnected**, zero error-severity routing DRC. K16/net51 best remains `60009a8e344c969e03e2cf42ff5496f14314ae5d`: **155 -> 154**, zero shorts/clearance, exactly one crossing (K16 B.Cu initial escape vs K14 B.Cu x=143.5). Generator restored to this exact candidate at `ed4133fbc21dc006f5b7495b5ae489fb1ab66aa2`.

Extensive K13/K14/K16 search completed. Layer-bridge approaches create shorts; K16 F.Cu escapes create >=2 crossings. The best alternative family is a **same-layer K14 sidestep left**: multiple variants keep zero shorts/clearance and one crossing while removing the original K16/K14 collision. Latest direct-pad variant `52dcbd651d32f25c427530a4616253fec0cb930a`, artifact `11155458843`. Next action: inspect that artifact's exact residual crossing pair and choose K14 sidestep endpoints around that specific B.Cu obstacle. Compare against original artifact `11154883351`; do not change K16 lower backbone y=158.

Promote K16 only after candidate reaches 154 unconnected with zero error-severity DRC. Then K1-K16 coil-low bank is complete and routing moves to a separately reviewed relay-contact/high-current phase; no Gerbers until zero DRC + zero unconnected.
