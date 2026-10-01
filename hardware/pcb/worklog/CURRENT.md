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
Official PCB: **K1-K16 + D25-D28 / 150 unconnected / zero critical geometry/electrical DRC**. D28 promoted and independently validated.

D29 current experiment: `079bd5cc73ac52e8cef2f64aa76cdc2271aa9e1e`, left/lower stagger preserving D28. GitHub runner is currently delayed in KiCad installation; do not infer result until Route Candidate run `36871461901` completes. Previous right-side D29 `067c6e51...` rejected: C2/C3 collisions at x127.5, D28 crossing, and U2/coil conflicts.

If `079bd5cc...` fails, inspect its artifact and refine only the exact collision pairs. Preserve validated D25-D28. Continue D29 then D30 using staggered wall-crossing lanes.

Final gate remains zero real DRC + zero unconnected, then produce same-revision assembly package **Gerber+Excellon ZIP + machine-readable BOM CSV + CPL/centroid CSV**. Existing `BOM-REV-A.md` is descriptive only and must be converted/cross-checked. Note assembly capability for THT/module parts separately from file completeness.

Keep +12V/GND distribution, relay COM/NO, high-current copper and pours untouched until dedicated reviewed phase.
