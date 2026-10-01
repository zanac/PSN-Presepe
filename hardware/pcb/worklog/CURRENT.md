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
**Validated Freerouting logic batch is ready for promotion from artifact 11175292602 (run 36887424491).** The candidate passed protected-net stripping, routed-net preservation, KiCad DRC comparison and improved connectivity from **149 to 122 unconnected pads (-27)** with no critical DRC categories.

Promotion failed only because KiCad SES reformatting exposed an indentation assumption in `pcb_sanity.py`; the sanity parser has since been hardened and the exact validated routed-net ID set approved. Autoroute CI is now serialized with `concurrency/cancel-in-progress` and remains artifact-only; promotion is external/manual after validation.

After promotion, exactly **5 logic connections** remain: `D36_RELAY12`, `CIELO_G_NEG`, `TRAM_R_NEG`, `TRAM_G_NEG`, `ALBA_B_NEG`. The other **117** remaining unconnected reports are deliberate routing work: **48 relay contacts + 69 power**. Close the 5 logic stragglers with targeted candidates/DRC before relay-contact routing, then power buses/zones.

Official KiCad validation workflow was also fixed so `kicad-cli` may emit incomplete-board reports without aborting before `drc_gate.py`; the explicit fabrication gate remains authoritative. Final fabrication gate remains zero real DRC + zero unconnected -> same-revision Gerber+Excellon ZIP + BOM CSV + CPL/centroid CSV.

Progress checkpoint before artifact promotion: ~50% routing / ~68% overall PCB. Recalculate immediately after the 149->122 candidate is committed.