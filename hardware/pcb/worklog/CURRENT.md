# PCB work checkpoint

This file is the short restart point for long autonomous PCB sessions.

## Current baseline
- Branch: `dev`.
- Official board: `hardware/pcb/kicad/PSN-Presepe-Mega.kicad_pcb`.
- Official board currently contains **113 routed segments**.
- Routing is being promoted only after a temporary candidate passes real KiCad DRC.
- K1-K10 relay coil-low routes are promoted and sanity-approved. K11 is in candidate validation.
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
Official baseline remains **160 unconnected**, K1-K10 promoted. K11 candidates 1-6 were rejected and never promoted; every one still proved connectivity reduction 160->159. Candidate 6 showed direct B.Cu lateral escape from U2.16 crosses the ULN THT row. Validate candidate 7 `9cbb0a9ad6a4ae42da3628c2dc245dc33c16bc01` (Route Candidate `36827640339`): short F.Cu escape to remote via at (150,98.5), then external B.Cu corridor x=130/y=132 into K11.5. If green promote net46 and continue K12.
