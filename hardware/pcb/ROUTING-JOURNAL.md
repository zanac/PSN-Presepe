# PCB Routing Journal — Rev A

Persistent restart/checkpoint log for long autonomous routing sessions on branch `dev`.

## Rules

- Never route directly from an unverified idea into the production PCB.
- Build one small candidate net/group at a time in a temporary copy.
- Run KiCad 9 DRC on the candidate.
- Promote only candidates with zero error-severity DRC violations and a real reduction in unconnected items.
- After promotion, commit immediately and record the new baseline here.
- Keep relay-contact routing and high-current/pour work for dedicated reviewed phases.
- Gerber export remains blocked until the fabrication gate sees zero DRC errors and zero unconnected items.

## Current verified baseline

- Branch: `dev`
- Baseline HEAD when this checkpoint was written: `3f41e3e98e11786a8fc51d589adb8a157fd18042`
- KiCad: 9.0.9 in GitHub Actions
- Source PCB routed segments: at least 109
- Copper zones: 0
- Error-severity DRC violations: **0**
- Unconnected items: **160**
- Full-report non-routing warnings: 66 `lib_footprint_mismatch`
- Fabrication status: **BLOCKED / NOT FOR FABRICATION**

## Verified/promoted routing groups

The source sanity allow-list currently contains these routed net IDs:

- 14, 15: OLED SDA/SCL
- 16, 17, 18: START/NEXT/TEST
- 19: A0 potentiometer signal
- 36, 37, 38, 39, 40, 41, 42, 43, 44: relay coil-low K1/K2/K3/K4/K5/K6/K7/K8/K9
- 63..71: local MOSFET gate nodes

These nets are considered source-PCB routing checkpoints because they were promoted only after candidate DRC validation.

## Current experiment

Next candidate: `RELAY10_COIL_LOW`, net 45, U2 pad17 -> K10 pad5.

Generator:
`hardware/pcb/tools/make_route_candidate.py`

Important: re-read the production PCB and generator from fresh `dev` HEAD before editing. Concurrent commits have occurred during previous sessions.

## Restart procedure

1. Fetch `dev` HEAD.
2. Read this journal.
3. Check latest `pcb-kicad.yml` run.
4. Confirm production baseline with `pcb_sanity.py` and KiCad DRC.
5. Inspect the current candidate generator.
6. Run/inspect candidate DRC.
7. If clean and connectivity improves, promote only that candidate net.
8. Commit the promotion.
9. Update sanity approved-net allow-list.
10. Update this journal baseline and next candidate.

## Historical milestones

- Initial production board: 0 segments / 194 unconnected.
- First naive D22/D23/D24 candidate reduced connectivity but created shorts/crossings; it was rejected and never promoted.
- Candidate workflow was moved into the KiCad project directory so project footprint libraries are resolved correctly.
- Low-risk routing was then promoted incrementally rather than as one large text-generated route set.
- Current verified production baseline: 166 unconnected, zero error-severity DRC violations.

## Do not infer

A red GitHub Actions run does not automatically mean routing failed. While the board is incomplete, the final fabrication gate intentionally exits non-zero for remaining unconnected items. Always inspect the DRC counts and candidate-specific steps/logs.

## Checkpoint K5 — 2026-10-01

- K5 / `RELAY5_COIL_LOW` net 40 promoted in `9d1b02622b19cd3b372162aa1dcf989d9fa6d91c`.
- Sanity allow-list updated in `76e252d9f4eabce3c5dec292bf02dfb8ce4fabec`.
- Stable KiCad 9.0.9 run: `36824507731`.
- Official baseline: **165 unconnected items**.
- Error-severity DRC violations: **0**.
- Critical geometry/electrical categories: **none**.
- Next target: K6 / `RELAY6_COIL_LOW`, net 41, U1 pad13 -> K6 pad5.

## Checkpoint K6 — 2026-10-01

- K6 / `RELAY6_COIL_LOW` net 41 candidate passed dedicated route validation on run `36824635074`.
- K6 route promoted in `ca01fe1fb9f8d1e2e33b271d4be57d3ba8253dcc`.
- Sanity allow-list updated in `ca7565f4aed8d7d69ef1fb77e9e3324dc0286b88`.
- Candidate reduced connectivity from **165 → 164 unconnected items** with zero error-severity DRC violations.
- Next target: K7 / `RELAY7_COIL_LOW`, net 42, U1 pad12 -> K7 pad5.

## Checkpoint K7 — 2026-10-01

- K7 / `RELAY7_COIL_LOW` net 42 candidate passed dedicated route validation on run `36824895407` and Routing Lab `36824895370`.
- K7 route promoted in `6b68a10e4f4a674b6cefec46b93f88035723c038`.
- Sanity allow-list updated in `3f41e3e98e11786a8fc51d589adb8a157fd18042`.
- Candidate improved connectivity with zero error-severity DRC violations; official baseline is now **163 unconnected items**.
- Next target: K8 / `RELAY8_COIL_LOW`, net 43, U1 pad11 -> K8 pad5.

## Checkpoint K8/K9 — 2026-10-01

- K8 / net 43 passed Route Candidate run `36825163253` and Routing Lab `36825163240`; promoted in `92b51d9ade2f77bdfbd14e6c32fc90ccd81dfb0e`, sanity-approved in `da995d58895f32e03e9aa645983017897bd52724`.
- K9 / net 44 passed Route Candidate run `36825298968` and Routing Lab `36825299003`; promoted in `eb7ac805b9a549f9871fbe4db3625000b6ec9203`, sanity-approved in `6cfd658603feee9aa6f601e6d1489f433ac8953b`.
- K1-K8 first coil-low bank is complete; second bank routing has started with K9.
- Official connectivity after K9 is **161 unconnected items**.
- Next target: K10 / `RELAY10_COIL_LOW`, net 45, U2 pad17 -> K10 pad5; candidate commit `f355ad399eab761c4f565e3a53219743873418e0`.

## K10 rejected candidate — 2026-10-01

- Candidate `f355ad399eab761c4f565e3a53219743873418e0` reduced connectivity **161 -> 160**, but was correctly rejected by Route Candidate run `36825569934`.
- DRC found K10 trace crossing K9 coil trace and touching K9 contact pads (`R9_NC`, `R9_COM`): 1 tracks_crossing, 2 shorting_items, 3 solder_mask_bridge.
- Nothing from this failed candidate was promoted to the production PCB.
- Revised K10 candidate `838e61b3dc6f0e53eba087d159820d8b42295f62` routes around the left/bottom of K9 and must pass the full candidate gate before promotion.

## Checkpoint K10 — 2026-10-01

- Revised K10 candidate `838e61b3dc6f0e53eba087d159820d8b42295f62` passed Route Candidate run `36825827075` with all gate steps successful.
- K10 / net 45 promoted in `f3bcda32516b89d19843643708845e0119bd251b` and sanity-approved in `2ea98eb2c71bd09bed03ded318b039c09c0754bc`.
- Official connectivity after K10: **160 unconnected items**.
- K11 / net 46 candidate prepared in `0c90ef05d92acda60cadc32e994b2534617a294a` using a lower corridor below K10.

## K11 rejected candidate — 2026-10-01

- Candidate `0c90ef05d92acda60cadc32e994b2534617a294a` reduced **160 -> 159** but was rejected by run `36825931693` for one `tracks_crossing` only.
- Exact crossing: K11 first segment from U2.16 intersects K10 vertical segment at `(142.0,96.5..118.0)`; no shorts were reported.
- Revised K11 candidate `68718816b2a38c29f8d96a4ba7934758ab69114c` exits U2 to the right and uses y=122 lower corridor.

## K11 second rejected candidate — 2026-10-01

- Candidate `68718816b2a38c29f8d96a4ba7934758ab69114c` again reduced **160 -> 159**, but run `36826094970` rejected it for exactly one `tracks_crossing`.
- Existing K9/K10 F.Cu corridors constrain a clean same-layer escape from U2.16.
- Third candidate `3022cabc0e84f851c72c524990f2827ac1d8dc3d` uses a controlled B.Cu crossover with two vias, returning to F.Cu near K11. It must pass full DRC before promotion.

## K11 third rejected candidate — 2026-10-01

- B.Cu candidate `3022cabc0e84f851c72c524990f2827ac1d8dc3d` reduced **160 -> 159** but run `36826462548` rejected it.
- Exact errors from candidate artifact: F.Cu escape crossed K9 coil route; B.Cu diagonal crossed K10 COM pad `(168.0,104.84)`, causing one short and one solder-mask bridge.
- DRC artifact also confirms actual lower relay coordinates K11..K16; no further coordinate extrapolation is needed.
- Fourth candidate `ffd9058b0c0dce627d6f4b7ceda41f36553ee566` drops to B.Cu beside U2 and uses y=124 below the relay row before returning beside K11 coil pad.

## K11 fourth rejected candidate — 2026-10-01

- Candidate `ffd9058b0c0dce627d6f4b7ceda41f36553ee566` reduced **160 -> 159**, but its B.Cu vertical at x=145.8 ran alongside/through U2 output-side PTH apertures, including +12V pad10, producing mask bridges and one short.
- Root cause is now explicit: do not descend beside U2 output pad column on B.Cu.
- Fifth candidate `1b3deb535c66716031a2bf19b6e43e25ecf7b356` escapes left on B.Cu, descends at x=132 outside U2 pad columns, crosses below relay row at y=130, then rises at K11.
