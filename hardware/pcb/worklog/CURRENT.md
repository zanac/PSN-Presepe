# PCB work checkpoint

This file is the short restart point for long autonomous PCB sessions.

## Current baseline
- Branch: `dev`.
- Official board: `hardware/pcb/kicad/PSN-Presepe-Mega.kicad_pcb`.
- Official board currently contains **105 routed segments**.
- Routing is being promoted only after a temporary candidate passes real KiCad DRC.
- K1-K8 relay coil-low routes are promoted and sanity-approved. The current temporary candidate targets K9 (`RELAY9_COIL_LOW`, net 44, U2.18 -> K9.5); always fetch it fresh because concurrent commits may advance it.
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
K8 (`RELAY8_COIL_LOW`, net 43) passed Route Candidate run `36825163253` and Routing Lab run `36825163240`; it was promoted in commit `92b51d9ade2f77bdfbd14e6c32fc90ccd81dfb0e` and sanity-approved in `da995d58895f32e03e9aa645983017897bd52724`. Validate the K9 candidate in commit `6424899cb5dd446a89f35f9b0216fc53cb99c796`; promote it only if candidate DRC is clean and connectivity improves.
