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
We are progressing, not routing-blocked. **Clean official baseline is K1-K16 + D25-D29 / 149 unconnected / zero critical geometry/electrical DRC**, proven by full KiCad Validation run `36880034688`. Workflow failure is only the intentional incomplete-connectivity gate.

D30/net25 redesign is active. Old alternating-layer family on the corrected D29 baseline produced 148 unconnected but 1 short (and later variants 3 crossings), so that family is abandoned. Current candidate is `08f5c5905378e17317c3b45fbb43ec9773f4a799`: simpler low-left route at y=83, preserving official PCB. Route Candidate run `36881645149` is still spending time in KiCad 9 installation; read its result before any promotion.

Important process: candidate success is necessary but not sufficient. After any D30 promotion, require full official KiCad Validation with **148 unconnected + zero critical geometry/electrical categories** before D31.

Operational bottleneck: GitHub-hosted runner repeatedly spends several minutes installing KiCad 9 for every candidate. Routing itself is advancing. After D30 is stabilized, improve CI runtime (cache/preinstalled-container strategy if safe) so D31+ iterations are faster; do not weaken DRC.

Final gate: zero real DRC + zero unconnected, then same-revision Gerber+Excellon ZIP + BOM CSV + CPL/centroid CSV.
