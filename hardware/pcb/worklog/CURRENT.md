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
**Freerouting CLI acceleration confirmed as the primary logic-routing strategy.** KiCad 9 -> Specctra DSN -> Freerouting 2.4.1 -> SES -> KiCad DRC works headlessly. Workflow is artifact-only; it never auto-promotes.

Direct inspection of autoroute artifact `11174895147` proves: official clean baseline report = **149 unconnected pads**; stripped autoroute candidate = **122 unconnected pads** and `Found 0 DRC violations` (non-connectivity). Thus **27 connections were solved in one pass**. Those 27 include D30,D31,D32,D33,D34,D35,D37,D38,D39,D40 plus D2/D3/D4 sky RGB, D5 stars, D6 buzzer, D7/D11/D12 sunset, D8 houses, D44/D45/D46 dawn and associated negative nodes. Power and relay COM/NO/NC were deliberately stripped/protected.

Workflow comparison bugs found/fixed: KiCad says 'unconnected pads', and error report legitimately contains unconnected_items. Commits `e1d62763...`, `ae4f884c...`, `f5c7d26f...` harden parser/gate. Current confirmation run `36885710850` is autorouting.

If confirmation matches 149->122 + no critical DRC: before promotion, add/check protected-net preservation and compare routed-net set; then promote the complete candidate only through full official KiCad Validation. Do not hand-route D30-D40 unless autoroute integration fails. After logic promotion, handle remaining logic stragglers, then dedicated relay-contact routing and power buses/zones.

Revised progress remains ~45-55% routing / ~65-70% overall PCB before autoroute promotion; a validated 27-connection promotion will materially improve both. Final gate remains zero real DRC + zero unconnected -> Gerber+Excellon ZIP + BOM CSV + CPL/centroid CSV.
