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

## K11 fifth rejected candidate — 2026-10-01

- Candidate `1b3deb535c66716031a2bf19b6e43e25ecf7b356` reduced **160 -> 159** but failed with via-related hole/mask/short violations.
- Key simplification: U2.16 and K11.5 are both through-hole pads, so no layer-change vias are required to use B.Cu.
- Sixth candidate `788b41860645d9cdb9d12693b080ed1e41a214e9` routes net46 entirely on B.Cu: directly from U2.16 left to x=132, below relay row at y=130, then directly into K11.5.

## K11 sixth rejected candidate — 2026-10-01

- Via-free B.Cu candidate `788b41860645d9cdb9d12693b080ed1e41a214e9` again reduced **160 -> 159** but failed: lateral B.Cu escape from U2.16 crosses other plated-through pads in the U2 row.
- Seventh candidate `9cbb0a9ad6a4ae42da3628c2dc245dc33c16bc01` uses a short F.Cu escape to a remote via `(150,98.5)`, then B.Cu outside U2 at x=130 and below relays at y=132, ending directly at K11.5 THT.

## K11 seventh rejected candidate — 2026-10-01

- Candidate `9cbb0a9ad6a4ae42da3628c2dc245dc33c16bc01` reduced **160 -> 159** but produced multiple crossings/shorts.
- Inspection of the official board exposed existing long backbones in the attempted left corridor: net16 on F.Cu around x=128.5 and net17 on B.Cu around x=130.5. The candidate crossed these repeatedly.
- Eighth candidate `14f2a1e058754b0f325a62f690047cc134942b10` avoids the left corridor: short F.Cu escape to the right, via at `(152,99)`, B.Cu descent at x=152, then y=132 below relay row into K11.5.

## K11 eighth rejected candidate — 2026-10-01

- Candidate `14f2a1e058754b0f325a62f690047cc134942b10` reduced **160 -> 159** and substantially reduced geometry conflicts, but still had one track crossing plus two shorts/mask bridges around the transition area.
- Ninth candidate `143b7d8e3745eb45d9df65d70cd7192bf4111c19` moves the F.Cu-to-B.Cu transition beyond K9 to `(162,99.5)` and lowers the B.Cu backbone to y=134 before entering K11.5.

## K11 ninth rejected candidate — 2026-10-01

- Candidate `143b7d8e3745eb45d9df65d70cd7192bf4111c19` reduced **160 -> 159** and narrowed failures to exactly 3 violations.
- DRC evidence: initial F.Cu escape crossed K9 net44 vertical at x=147.5; the long F.Cu segment also crossed K9 pad4 `R9_NO` at `(157.62,99.76)`, causing one short and one solder-mask bridge.
- Tenth candidate `0249f572798492a72d3edee492a3f8f4dcbbec3d` avoids both: short F.Cu escape left to via `(143.5,99)`, then B.Cu x=143.5 to y=134 and across to K11.5.

## K11 validated and promoted / K12 start — 2026-10-01

- K11 candidate 10 `0249f572798492a72d3edee492a3f8f4dcbbec3d`, Route Candidate `36829048742`: **160 -> 159**, zero error-severity DRC violations.
- Promoted exact validated net46 geometry in official board: `22d3f2b4cc33837f3d7836bc771c1eba14583a2e`.
- Sanity gate now approves net46: `0e0a16ba399b72449ab47a3430c59bbf27abba4e`.
- Verified official K12-K16 footprints directly: pad5 endpoints are (211.62,115), (229.62,115), (247.62,115), (265.62,115), (283.62,115).
- K12/net47 candidate `cb24da98b496a8ded0bc87c96a1290f5913806c6` uses a staggered variant of the validated K11 topology: via (143,101.5), B.Cu x=143, lower corridor y=136, K12.5.

## K12 validated and promoted / K13 start — 2026-10-01

- K12 candidates iteratively isolated K11/K10 conflicts; final candidate `d4b72695d6b28b4b8ef0bdb7f43e9477bc797e03`, Route Candidate `36830213836`: **159 -> 158**, zero error-severity DRC violations.
- Promoted exact validated net47 geometry: `dd8bc4059f4ce6603bb334ec920307bdd859ca93`; sanity approval: `60b5597450766b482d425369ccb97190e007f913`.
- K13/net48 candidate `e7a2ac6f155dd92796aaf1ccfccd572ebb9ca45b` starts a staggered mixed-layer corridor; validate before promotion.

## K13 validated and promoted / K14 start — 2026-10-01

- K13 required a controlled multi-layer weave around the dense U2/K9-K12 corridor. Final candidate `e8c343cec4e64c4b1aeb9493270f28f7e2edad7e`, Route Candidate `36830926095`: **158 -> 157**, zero error-severity DRC violations.
- Promoted exact net48 geometry: `ed6538741ede7c8c13bf49c5a07d07e912edf69f`; sanity approval: `7cd69e3a957f27bcba06e4c1a9304fca573e77bf`.
- K14/net49 candidate `6d4f840eca798715aee363e8a9ace09ffbfd599f` started with staggered coordinates; DRC remains authoritative.

## K14 first rejected candidate — 2026-10-01

- Candidate `6d4f840eca798715aee363e8a9ace09ffbfd599f`, Route Candidate `36831044922`, reduced **157 -> 156** but had five track crossings with validated K10/K12/K13 geometry.
- No promotion occurred. Revised candidate `72818bf4bff0f99182f49c627206f51aa03493df` uses a right-side fanout and controlled layer weave; validate it next.

## K14 fanout constraint discovered — 2026-10-01

- Multiple K14/net49 candidates consistently reduce connectivity **157 -> 156**, proving endpoint/net correctness, but none is promotable yet.
- DRC evidence shows the U2.13 escape is boxed by validated routes: K10/K13 on F.Cu, K11/K12 on B.Cu, plus U2.12/U2.11/U2.10 pads and K9 contact/coil pads.
- Best outer-corridor attempt `ff03eec08cb81aab1dc6231e00134e116e4a03dc` left only K11-vs-K14 local conflicts; moving the via left (`4c51bf5fc6e2b27ed5a6c2927e023908c842bb78`) moved the remaining conflicts to the short F.Cu escape against K10/K13.
- Immediate-via attempt `9936fc0a28abaa4dd6564a554f6cee3d8fd327a9` confirmed that simply dropping to B.Cu alongside U2 collides with pads 12/11/10 and K11.
- **No K14 candidate was promoted. Official PCB remains K1-K13, 157 unconnected.**
- Next safe strategy: test a combined temporary reroute that removes/repositions K11/net46 to open an escape lane for K14, then run full KiCad DRC and require no regression before changing the official PCB.
