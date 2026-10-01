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
Official PCB: **K1-K16 + D25-D29 / 149 unconnected**. D29 candidate `fdeb1ecd...`, Route Candidate `36873633369` SUCCESS (150->149, zero routing DRC); promoted `b6ba98a8...`; sanity net24 `ff67854d...`.

D29 reusable pattern: B.Cu escape through midpoint between adjacent Mega pads, via after pad column; F.Cu down an analog inter-column corridor; at an inter-row midpoint use F across TEST(B), via x127, B across START(F), via x129.5, F across NEXT(B), then approach U1. For D29 the clean inter-row Y is 80.57.

D30 current candidate `cd71514a7a079843dc92f24f6da86afe8916eea7`, run `36874130419`, uses complementary y=78.03 path and extra B.Cu final approach to cross D29. CI was still installing KiCad at checkpoint. Inspect result/artifact first; promote only if 149->148 and zero routing DRC.

Then continue D31/D32 using staggered inter-row corridors. Preserve D25-D29 unless an atomic repack is fully clean.

Final gate: zero real DRC + zero unconnected, then same-revision Gerber+Excellon ZIP + machine-readable BOM CSV + CPL/centroid CSV with reference/revision cross-check.

Keep +12V/GND distribution, relay COM/NO, high-current copper and pours untouched until dedicated reviewed phase.
