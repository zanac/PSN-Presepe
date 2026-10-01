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
**Methodology pivot: Freerouting CLI is viable and now preferred for congested logic.** KiCad 9 headless exports Specctra DSN via pcbnew; Freerouting 2.4.1 routes headlessly to SES; KiCad imports SES and remains final DRC authority. Workflow `.github/workflows/pcb-autoroute-candidate.yml` was made artifact-only (no automatic push) in `83052a17...`, then KiCad 9 parser fixed in `e1d62763...`.

First completed autoroute lab run `36881798109`, artifact `11172341324`: after stripping deliberately protected power and relay-contact routing, candidate report shows **122 unconnected pads vs clean official baseline 149 = 27 connections eliminated in one autoroute pass**, with **zero non-connectivity/error DRC violations** in the KiCad report. The workflow itself failed only because its comparison parser incorrectly looked for 'unconnected items'; KiCad 9 says 'unconnected pads'. Parser now fixed. Do NOT promote first artifact automatically; it is evidence/lab output.

Corrected confirmation run: `36883481213` (Freerouting 2.4.1) currently autorouting. If it confirms the reduction and clean DRC, stop hand-routing D30 as primary strategy. Next build/select best logic autoroute candidate, review diff/net classes, then promote only through full official KiCad DRC. Power (+12V/GND/+5V) and relay COM/NO/NC remain protected for dedicated width/clearance routing.

Progress accounting remains: clean official baseline 149 unconnected; routing ~45-55%, overall PCB ~65-70%, manufacturing readiness ~60-65%. A clean autoroute promotion of ~27 logic connections would materially raise these.

Final gate: zero real DRC + zero unconnected, then same-revision Gerber+Excellon ZIP + BOM CSV + CPL/centroid CSV.
