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
K11/net46 is now validated and officially promoted. Candidate run `36829048742` proved **160 -> 159** with zero error-severity DRC; board commit `22d3f2b4cc33837f3d7836bc771c1eba14583a2e`, sanity approval `0e0a16ba399b72449ab47a3430c59bbf27abba4e`. Official baseline should now be **159 unconnected** (confirm from next candidate logs). Exact K12-K16 pad5 endpoints verified from official board: x=211.62/229.62/247.62/265.62/283.62, y=115. Validate K12/net47 candidate `cb24da98b496a8ded0bc87c96a1290f5913806c6`, Route Candidate `36829369985`; if green promote and continue K13.
