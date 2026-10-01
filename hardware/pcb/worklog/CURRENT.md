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
Tooling review found a positive acceleration path: KiCad 9 Python exposes Specctra DSN export/import and Freerouting supports headless DSN->SES autorouting. Existing `.github/workflows/pcb-autoroute-candidate.yml` has been converted into an **artifact-only laboratory** (no automatic PCB push), updated to Freerouting 2.4.1, with baseline-vs-candidate connectivity/DRC comparison. Long 300-pass run `36881798109` is still autorouting; fast 50-pass run `36883023057` is starting. Evaluate artifacts before adopting anything.

Clean official PCB baseline remains **149 unconnected / zero critical geometry/electrical DRC** (run `36880034688`). Exact residual composition from the clean report: GND 37, +12V 27, +5V_MEGA 5 (69 shared-power records); 48 relay-contact records (COM/NO/NC); 9 relay-input signals D30-D40; remainder other logic/PWM/data/MOSFET-side signals. Progress estimates corrected: routing ~45-55%, overall PCB ~65-70%, manufacturing package ~60-65%.

D30 manual candidate `08f5c590...` rejected (1 clearance, 1 short, 3 crossings). Earlier family reached 148 with only one localized short; do not promote. Prioritize autoroute experiment outcome. If Freerouting produces a DRC-clean large reduction, inspect and selectively adopt candidate; protected relay contacts and power are stripped by the lab before DRC. If not useful, resume manual/batched routing and improve CI to evaluate multiple candidates per KiCad installation.

Final gate unchanged: zero real DRC + zero unconnected, then same-revision Gerber+Excellon ZIP + BOM CSV + CPL/centroid CSV.
