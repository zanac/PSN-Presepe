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
Official PCB is now **K1-K15 / 155 unconnected**. K15/net50 plus required K9/K12 local repack was promoted in `bec89822bcfcb3f2f0540362171a7f785e18f947`; sanity approval `7638b267b49036cdf2a1bbe0fabd7a69d004d471`. Official KiCad validation reports zero error-severity routing violations; fabrication gate remains blocked only by incomplete connectivity.

K16/net51 best candidate is `60009a8e344c969e03e2cf42ff5496f14314ae5d`: **155 -> 154**, zero shorts/clearance, exactly one crossing. Artifact `11154883351`: K16 initial B.Cu escape crosses K14 B.Cu vertical x=143.5. A direct K14 F.Cu bridge (`220fc49f...`) removes the crossing but its two vias short against K13 F.Cu x=143 (artifact `11155515916`). Right-side K16 escape regresses. Generator restored to best K16 in `993086ce6a043618672e8388f5d7e208f15a1eba`.

Next: coordinated **local K13/K14 repack around y≈108–114** to free one layer at the K16 escape, without changing the proven lower K16 backbone y=158. Promote K16 only after zero-error candidate DRC. After K16, stop coil-low routing and begin the separately reviewed relay-contact/high-current phase; no Gerbers until zero DRC + zero unconnected.
