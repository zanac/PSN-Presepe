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
Clean official baseline restored: **K1-K16 + D25-D29 / 149 unconnected / zero critical geometry/electrical DRC**. Full KiCad Validation run `36880034688` on commit `40500c6a...`: categories only `lib_footprint_mismatch:66` + `unconnected_items:149`; critical categories none. D29 clearance was fixed by moving its first via right to x=120.5.

D30/net25 was removed from official PCB and sanity approval revoked after discovering full-DRC clearance regressions. Redesign D30 from the clean 149 baseline. Candidate success alone is insufficient: after promotion require official full KiCad Validation with zero critical geometry/electrical categories and 148 unconnected before D31.

Continue D30 using the prior alternating-layer concept but keep transition vias safely spaced; avoid the compressed x=129.5/131.25 transition that produced clearance errors. Then D31/D32.

Final gate: zero real DRC + zero unconnected, then same-revision Gerber+Excellon ZIP + BOM CSV + CPL/centroid CSV.
