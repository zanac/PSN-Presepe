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
Official PCB: **K1-K14 / 156 unconnected**, zero critical routing DRC errors. K15/net50 best candidate remains `70fab4b4a9e86a9c205d61f840278a23a06451c5`: **156 -> 155**, zero shorts/clearance, one crossing; artifact `11153127344`. Generator restored to this exact candidate at `5225dca9ee6584600b84fb2d18bfaad6556e9662`.

Extended escape search proves vias near U2 and long F.Cu routes regress badly. The only promising untested topology is a **candidate-only local reroute of K12**, bridging its B.Cu vertical x=147 onto F.Cu around the K15 crossing while leaving K15 exactly unchanged. Previous attempt `9c2821ef...` was syntactically malformed and therefore gave no DRC conclusion. Rebuild that test cleanly, validate candidate syntax, then run DRC. Promote coordinated K12 adjustment + K15 only if zero-error.
