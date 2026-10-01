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
**Milestone reached: K1-K16 relay coil-low routing complete.** Final K16 candidate `4a546032d55f9b2b6dfa7e99aa6693296c8b1ee8` passed Route Candidate run `36854584445`: 155 -> 154 unconnected, zero routing DRC errors. Promoted K11/K14/K16 geometry in `cb164a2313a735384a2130bd7465fa126bc67088`; net51 sanity approval `809c4d85e9f84cf219d28b8c448208f1bbcb94de`.

Official KiCad Validation `36854767991`: **154 unconnected**, `lib_footprint_mismatch: 66`, **critical geometry/electrical categories: none**, error-severity DRC violations none. Fabrication gate intentionally remains closed; no Gerbers.

Next: inventory/classify the 154 residual connections. Continue autonomously with low-risk logic/control routing candidates first (Arduino relay input nets D25-D40 and other signal nets as geometry permits). Keep +12V/GND distribution, relay contacts COM/NO, high-current copper and pours out of blind routing; those require their dedicated reviewed phase.
