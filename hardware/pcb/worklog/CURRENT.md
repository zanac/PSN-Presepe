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
Official board promotion completed on `dev` at commit `cf84acada8c95eb92ad755395199ef8dcfbbcb3d`: the second validated Freerouting delta reduced connectivity from **122 to 120 unconnected pads (-2)** with no new critical DRC categories.

The two newly solved logic connections are:
- `D36_RELAY12`: MCU1 D36 -> U2 pad 4.
- `CIELO_G_NEG`: Q2 pad 2 -> J_CIELO pad 3.

Exactly **3 logic connections remain**:
- `TRAM_R_NEG`
- `TRAM_G_NEG`
- `ALBA_B_NEG`

The remaining 117 non-logic unconnected reports are still the planned **48 relay-contact + 69 power** routing workload. Close these 3 logic stragglers with targeted candidates and real KiCad DRC before relay-contact routing, then power buses/zones.

Validated artifact for the 122->120 delta: run `36898305562`, artifact `11180751893`; promotion run `36900932623` completed successfully. Keep autoroute artifact-only and protected power/contact nets stripped.

Final fabrication gate remains zero real DRC + zero unconnected -> same-revision Gerber+Excellon ZIP + BOM CSV + CPL/centroid CSV.

Progress checkpoint after 122->120 promotion: ~66% routing / ~76% overall PCB.

## ALBA_B targeted routing investigation (2026-10-01)
Official board remains at **118 unconnected**; no experimental candidate has been promoted.

Target net: `ALBA_B_NEG` (net 61), Q9.2 `(112.54,165)` -> J_ALBA.4 `(171.24,184)`.

A dedicated KiCad 9 container workflow now batches candidate routes and runs real DRC without repeated APT installation:
`.github/workflows/pcb-targeted-alba-b.yml`.

Every tested route electrically closes ALBA_B and reaches **117 unconnected**, but all current geometries still create critical DRC collisions, so promotion is correctly blocked. Main geometric barriers observed around the Q9 escape/destination corridor include `D22_START`, `D24_TEST`, `CIELO_R_NEG`, `CIELO_G_NEG`, `CIELO_B_NEG`, `TRAM_B_NEG`, `ALBA_R_NEG`, and `ALBA_G_NEG`.

Best diagnostic families so far reduced the error classes to `tracks_crossing` / `shorting_items` (some variants also introduce clearance/hole/solder-mask issues). Direct, lower-edge, upper, mixed-layer, fine sweep, and dogleg topologies have been tested. Do not promote any of them.

Next best practice: stop hand-picking polylines and make the targeted router obstacle-aware from the actual PCB copper/pads/vias, searching a clearance-inflated grid independently on F.Cu/B.Cu with via transitions. Require 117 unconnected and no new critical DRC before promotion.


## ALBA_B closed on official board (2026-10-01)
Milestone reached on `dev`: official board is now **117 unconnected** with **no critical geometry/electrical DRC categories** and **no error-severity DRC violations**.

Final ALBA_B route is net 61. The only post-promotion clearance issue was between the ALBA_B via at `(127.5,172.75)` and `ALBA_G_NEG`: RGB_LOAD requires 0.300 mm clearance. Keeping the validated route geometry and changing that via from 0.8/0.4 mm to **0.6/0.3 mm** removes the violation. Official electrical board commit: `8dba41f28c25e780997ea7a1cd376aa72ea8b58f`.

Official KiCad validation reports:
- 117 unconnected items
- critical geometry/electrical categories: none
- error-severity DRC violations: none
- remaining non-critical/incomplete-board categories include planned unconnected items, footprint-library mismatch, existing hole-to-hole notices and a dangling-via notice.

The fabrication workflow remains intentionally red until **zero unconnected**; do not weaken that gate.

Remaining connectivity workload is now exactly the planned non-logic work:
- **48 relay-contact connections**
- **69 power connections**
- **0 logic connections**

Next stage: route relay contacts parametrically/in reviewed batches with mains-capable clearance/isolation rules; do not use blind generic autorouting. Power buses/zones remain last.


## Relay-contact milestone (2026-10-02)
Official board on `dev` has advanced from the 117-unconnected logic-complete baseline to a promoted **75-unconnected relay checkpoint** (commits `2acb44b...` / `89188ab...`). This means 42 connectivity items have been removed since the 117 baseline. Current targeted work is the final relay-contact subset; power routing remains last. A corrected obstacle router now applies footprint rotation consistently to real pad geometry. Revalidate the official 75 baseline with the normal KiCad workflow before any further promotion; never replace it with an experimental candidate that has shorts/clearance errors.


## Validated relay batch checkpoint (2026-10-02)
Promoted exact artifact from relay run `36943389801` at commit `ce40b5714b637355b450c43f20231f18ec328107`: **76 unconnected** in candidate DRC, with no clearance/short/track-dangling error categories. This preserves the previously verified 93-unconnected clean baseline and adds 17 conservatively routed relay-contact nets. Expected remaining connectivity: **7 relay contacts + 69 power = 76**. Run normal official-board KiCad validation immediately after this checkpoint and treat that result as authoritative.
