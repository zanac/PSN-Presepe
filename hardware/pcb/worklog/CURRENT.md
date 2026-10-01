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
Official PCB is now **K1-K14 / 156 unconnected**. K14/net49 was promoted after zero-error candidate run `36844515326`; official board commit `285ee46f592a7a2ee4197c7c06fb1f488ee47f00`, sanity approval `81a3c3e064615797c101b76999cfe74ef5cfe764`. Official KiCad validation has no critical routing errors; fabrication remains blocked only by incomplete connectivity.

K15/net50 best candidate is `70fab4b4a9e86a9c205d61f840278a23a06451c5`: **156 -> 155**, zero shorts/clearance, exactly one crossing. Artifact `11153127344`: K15 initial B.Cu pad escape crosses K12 B.Cu vertical x=147. Generator restored to this best candidate in `41ef0da662f07cabb78bdffc8f552df953100fd1`. Next: redesign only K15's initial escape, placing any layer transition farther from U2; keep the proven x=148 descent, F.Cu bridge across K14 y=142, and lower B.Cu backbone. Promote only after zero-error DRC.
