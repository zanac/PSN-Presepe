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
Clean-baseline recovery in progress. D30/net25 is intentionally **removed** from the official PCB; current connectivity is **149 unconnected** (K1-K16 + D25-D29). Full DRC still had one clearance after commit `4a322caf...`.

Current official experiment commit: `deae8e0597c8823744d3c9f7c4dd5c17a4808d2d`. It changes only D29/net24 escape via from x=119.5 to x=120.5 at y=52.63 and its two adjoining segments. Full KiCad Validation run `36879585169` is pending/in progress. Do not infer success until its DRC summary is read.

If full DRC is clean: record 149-unconnected clean baseline, then redesign D30 from scratch and require both Route Candidate AND post-promotion full KiCad Validation to show zero critical geometry/electrical categories. If the one clearance remains: download the DRC artifact and identify exact object pair before another coordinate change; do not guess further.

After D30 full-DRC clean at 148, continue D31/D32. Final manufacturing gate: zero real DRC + zero unconnected, then same-revision Gerber+Excellon ZIP + machine-readable BOM CSV + CPL/centroid CSV.
