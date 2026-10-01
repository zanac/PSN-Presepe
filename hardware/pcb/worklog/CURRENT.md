# PCB work checkpoint

This file is the short restart point for long autonomous PCB sessions.

## Current baseline
- Branch: `dev`.
- Official board: `hardware/pcb/kicad/PSN-Presepe-Mega.kicad_pcb`.
- Official board contains K1-K12 coil-low routing; K12 added six track segments plus one via after K11 baseline.
- Routing is being promoted only after a temporary candidate passes real KiCad DRC.
- K1-K12 relay coil-low routes are promoted and sanity-approved. K13 is in candidate validation.
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
K12/net47 is validated and officially promoted. Route Candidate `36830213836` proved **159 -> 158** with zero error-severity DRC; board commit `dd8bc4059f4ce6603bb334ec920307bdd859ca93`, sanity approval `60b5597450766b482d425369ccb97190e007f913`. Validate K13/net48 candidate `e7a2ac6f155dd92796aaf1ccfccd572ebb9ca45b`; if green promote exact geometry, approve net48, then continue K14.
