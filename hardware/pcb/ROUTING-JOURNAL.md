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

## K14 combined-reroute experiments — 2026-10-01

- Official PCB stayed unchanged at K1-K13 / **157 unconnected** throughout this series.
- Joint K11+K14 candidates `dfd7af45...`, `a8a32429...`, and `fa9e4053...` all preserved connectivity and produced **157 -> 156**; the best result was only two track crossings and no shorts.
- Moving K13 as well (`26902354...`) regressed DRC, so K13 should remain in its validated geometry.
- K14 layer-weave `32fda91e...` and alternate entry `ca57761c...` proved the two-crossing bottleneck is in the U2.13 local fanout, not the lower backbone.
- Next experiment should temporarily repack K11+K12 together while preserving K13, creating a dedicated B.Cu escape lane for K14. No official route should be replaced until the combined candidate has zero error-severity DRC and still reduces unconnected 157 -> 156.

## K14 exact-crossing reduction — 2026-10-01 11:17 CEST

- K11+K12+K14 repack `65b12f29...` regressed to 3 crossings; rejected.
- Right-side K14 escape `83235a25...` entered K9 contact geometry and produced shorts/clearance errors; reject this topology family.
- Inspecting the best K11+K14 artifact proved its two DRC crossings were both on the temporary K11 replacement, while K14 itself was clean.
- Local K11 layer-hop candidate `c2d97e60...` improved the combined route to **one single tracks_crossing**, still **157 -> 156**, with no shorts/clearance errors.
- The remaining crossing is between K11 F.Cu backbone ending at/near `(193.62,146)` and validated K12 F.Cu geometry reported from `(147,136)`; artifact `11150558819` is the cleanest evidence checkpoint.
- Extending the K11 B.Cu section (`5e358898...`, `db215b94...`) trades that one crossing for crossings against K13/K14, so do not use those variants.
- **Official PCB remains unchanged: K1-K13, 157 unconnected.** Best restart base is candidate `c2d97e60287361f5e377c04ce1d9b19ce04a474b`; solve only its final K11/K12 crossing while keeping K14 topology unchanged.

## K14 extended search / local optimum — 2026-10-01 11:36 CEST

Extended autonomous search confirmed the local optimum rather than promoting a marginal route:
- K11 endpoint-from-left `bbc99085...`: 157 -> 156, 1 crossing.
- K11 minimal B.Cu endpoint stub `5d70da72...`: 157 -> 156, 1 crossing.
- Shift endpoint vertical right `f7bf6f79...`: 157 -> 156, 1 crossing.
- Lower F.Cu backbone `2107f249...`: 157 -> 156, 1 crossing.
- Direct B.Cu U2.16 escape `afcc54a1...`: 157 -> 156, 1 crossing.
- Outer x=136 descent `8bb8ef6b...`: produced shorts/mask/clearance; rejected.
- K12+K14 `2ae0c50e...`: 3 crossings; rejected.
- K10+K14 `6e9c4195...`: shorts/mask + 4 crossings; rejected.

Conclusion: moving K10/K12/K13 or changing K11's endpoint/backbone does not beat the K11+K14 candidate `c2d97e60...`, which remains the best known geometry at **one tracks_crossing, zero shorts/clearance, 157 -> 156**. Generator was deliberately restored to that exact candidate in commit `7d5c70de...`. Official PCB remains K1-K13 / 157 unconnected.

Next useful step is to inspect the exact DRC item text/coordinates for artifact `11150558819` and modify only the segment pair named by KiCad. Do not resume broad geometric guessing.

## K14 promoted; K15 started — 2026-10-01 11:55 CEST

- Exact artifact inspection of `11150558819` identified the last K14-blocking violation precisely: K12 F.Cu horizontal at y=136 crossing K11 F.Cu vertical x=193.62.
- Candidate `5a6f8a361b15faae3c396026fbd24d9db01cb418` inserted only a local K11 B.Cu bridge from y=138 to y=134. Route Candidate run `36844515326` **SUCCESS**: 157 -> 156, zero routing DRC errors.
- Promoted K11 replacement + K14/net49 atomically to official PCB in `285ee46f592a7a2ee4197c7c06fb1f488ee47f00`.
- Sanity allow-list updated for net49 in `81a3c3e064615797c101b76999cfe74ef5cfe764`.
- Official KiCad validation after promotion: **156 unconnected**, no critical geometry/electrical categories; fabrication gate fails only because board is intentionally incomplete.

K15/net50:
- Initial B.Cu candidate `81777e02...`: 156 -> 155, exactly one crossing (K15 initial fanout vs K14 vertical).
- Right-side/local-bridge candidate `70fab4b4a9e86a9c205d61f840278a23a06451c5`: 156 -> 155, exactly one crossing, zero shorts/clearance. Artifact `11153127344` identifies it as K15 initial B.Cu segment crossing K12 B.Cu vertical x=147.
- Attempts `d62b78e2...` and `a2d19887...` to bridge near U2 introduce a short; rejected.
- Generator restored to best K15 candidate in `41ef0da662f07cabb78bdffc8f552df953100fd1`.

Next: solve only K15's initial pad escape across K12 x=147, but keep layer changes farther from U2 pads/vias. Official board stays K1-K14 / 156 unconnected until K15 candidate is zero-error.

## K15 extended escape search — 2026-10-01 12:07 CEST

Official remains K1-K14 / 156 unconnected and clean except intentional incompleteness.

K15 experiments from best `70fab4b4...` (156 -> 155, one crossing, zero shorts/clearance):
- `33354716...`: move layer bridge below U2; 2 shorts + 2 mask bridges + 2 crossings. Reject.
- `abafd372...`: separate pad escape/crossing; 3 shorts + 4 mask bridges + hole errors. Reject.
- `75a2ff22...`: long F.Cu escape to x=152; no shorts but 6 crossings. Reject.
- `9c2821ef...`: attempted candidate-only local K12 bridge; generator produced malformed candidate (KiCad failed to load). **No electrical conclusion; this topology still needs a correct test.**
- `3f9d0036...`: B.Cu detour around K12 lower endpoint; 2 shorts + 3 mask bridges. Reject.

Conclusion: do not add vias close to U2 and do not route K15 long-distance on F.Cu. Best known K15 candidate remains `70fab4b4a9e86a9c205d61f840278a23a06451c5`, artifact `11153127344`, with only K15 initial B.Cu escape crossing K12 B.Cu vertical x=147. Generator restored to that exact candidate in `5225dca9ee6584600b84fb2d18bfaad6556e9662`.

Next experiment: correctly construct a candidate that keeps K15 exactly as best-known and replaces only K12's B.Cu x=147 segment with a local F.Cu bridge around the K15 crossing, with vias placed sufficiently far from U2. Validate syntax before DRC.

## K15 promoted; K16 started — 2026-10-01 12:38 CEST

### K15/net50 completion
- Corrected the malformed K12-bridge generator and obtained a valid topology test in `88fe9b7b...`: 156 -> 155, crossings eliminated but two shorts; artifact `11154558418` proved both shorts were K12 bridge vias vs K9 F.Cu vertical x=147.5.
- Repacked K9/net44 away from those vias while keeping the proven K12 bridge and K15 geometry. Candidate `435f8b0439c3839422fc9aa41ebd0fbd59e951f0`, Route Candidate run `36849600656`: **SUCCESS**, 156 -> 155, zero routing DRC errors. Evidence artifact `11154489961`.
- Promoted K9 + K12 repack and K15/net50 atomically to official PCB in `bec89822bcfcb3f2f0540362171a7f785e18f947`; sanity allow-list net50 in `7638b267b49036cdf2a1bbe0fabd7a69d004d471`.
- Official KiCad validation: **155 unconnected**, error-severity DRC violations none, critical geometry/electrical categories none. Fabrication gate fails only because connectivity is intentionally incomplete.

### K16/net51 search
- Initial lower-backbone candidate `60009a8e344c969e03e2cf42ff5496f14314ae5d`: **155 -> 154**, zero shorts/clearance, exactly one crossing. Artifact `11154883351` identifies exact crossing: K16 initial B.Cu escape from U2.11 vs K14 B.Cu vertical x=143.5 (K14 segment 106->142).
- `220fc49f...`: bridge K14 locally onto F.Cu around K16 crossing. Crossing removed, but two shorts; artifact `11155515916` shows both K14 vias collide with K13 F.Cu vertical x=143.0 (segment starting 143,103.5).
- `8fdcf5b2...`: K16 right-side/lower escape; regressed to 2 shorts + 3 crossings. Reject.
- Conclusion: K13 F.Cu x=143 and K14 B.Cu x=143.5 form the two-layer bottleneck. Next solve via coordinated local K13/K14 repack around y~108-114, leaving K16 best geometry unchanged.
- Generator restored to exact best K16 candidate in `993086ce6a043618672e8388f5d7e208f15a1eba`.

## K16 bottleneck search II — 2026-10-01 13:00 CEST

Official PCB unchanged: K1-K15 / 155 unconnected / zero error-severity routing DRC. Best K16 remains `60009a8e...`: 155 -> 154, zero shorts/clearance, one crossing K16 B.Cu escape vs K14 B.Cu x=143.5.

Experiments:
- `566b3c6e...`: move K13 F.Cu vertical to x=140 + K14 F.Cu bridge. 1 short + 3 crossings. Reject.
- `a5122023...`: interleaved K13 B.Cu bridge / K14 F.Cu bridge. 4 shorts + 1 clearance + 1 crossing. Reject.
- `07d8caea...`: short K16 F.Cu escape right. 3 shorts + 1 mask bridge + 2 crossings. Reject.
- `f8a53546...`: K16 F.Cu escape left with remote via at (141,120). No shorts/clearance, but 2 crossings. Interesting but worse than baseline.
- K14 same-layer sidestep family: `1fd13ff9...`, `78bc73c0...`, `9171f3a8...`, `4feb36b5...`, `e8b973a2...`, `52dcbd65...`. All maintain 155 -> 154 with **zero shorts/clearance and exactly one crossing**. Moving K14 left does free the original K16/K14 crossing, but one K14 raccordo then crosses another B.Cu route. This family is geometrically promising but needs exact residual-pair inspection before another coordinate change.

Generator restored to exact best original K16 in `ed4133fbc21dc006f5b7495b5ae489fb1ab66aa2`.
Next: inspect residual crossing from artifact `11155458843` (direct K14 pad escape-left variant) and compare with original artifact `11154883351`; design K14 sidestep endpoints around the actual conflicting B.Cu segment rather than guessing coordinates. Do not disturb proven K16 lower backbone y=158.

## K16 promoted — second relay coil-low bank complete — 2026-10-01 13:22 CEST

- Exact residual sidestep crossing from artifact `11155458843`: K16 B.Cu vertical x=141 (start 141,112, length 46) vs K14 B.Cu horizontal re-entry at y=124 from x=139.5 to x=143.5.
- K14 F.Cu bridge experiment `1b698c15...` proved the only new conflict was K11 F.Cu x=140 vs K14 bridge/via at x=139.5,y=124 (artifact `11156733356`).
- Local K11/net46 F.Cu sidestep x=137 between y=120..130 freed the K14 bridge without disturbing its validated endpoints.
- Final candidate `4a546032d55f9b2b6dfa7e99aa6693296c8b1ee8`, Route Candidate run `36854584445`: **SUCCESS**, 155 -> 154, zero error-severity routing DRC. Evidence artifact `11157941040`.
- Promoted K11 + K14 + K16 atomically to official PCB: `cb164a2313a735384a2130bd7465fa126bc67088`.
- Added net51 to source sanity allow-list: `809c4d85e9f84cf219d28b8c448208f1bbcb94de`.
- Official KiCad Validation run `36854767991`: DRC categories `{'lib_footprint_mismatch': 66, 'unconnected_items': 154}`; **critical geometry/electrical categories none**, error-severity DRC violations none. Gate failure is intentionally only incomplete connectivity; no Gerbers exported.
- Milestone: **all K1-K16 relay coil-low outputs are now routed and KiCad-validated**.

Next phase is not blind relay-contact routing. Inventory the 154 remaining connections and route low-risk logic/control nets first; power/high-current and relay-contact nets remain a separately reviewed phase. Keep Gerber gate closed until zero real DRC errors + zero unconnected.

## Relay-input fanout reconnaissance — 2026-10-01 13:36 CEST

Official board remains the validated K1-K16 milestone: 154 unconnected, zero critical routing DRC. No input candidate promoted.

Residual low-risk target block identified: nets 20..35 = D25_RELAY1..D40_RELAY16, MCU1 -> U1/U2 inputs. U1 inputs are x=135,y=62..79.78; U2 inputs x=135,y=92..109.78. MCU1 absolute relay pads alternate x=121.98/124.52 from y=46.28 through 66.60.

Probes:
- D25 F.Cu direct `b8adaee1...`: 154->153 but 1 short + 1 crossing + 1 solder-mask bridge.
- D25 same geometry B.Cu `3945740e...`: same violation pattern, proving corridor geometry rather than layer is the problem.
- D25 external-left B.Cu `7bb85a63...`: worse (clearance/short/mask/crossings); left edge around MCU is occupied.
- D40 lower direct `96b9ecd3...`: 154->153 but hole-clearance + short + mask + crossing near MCU corridor.

Conclusion: D25-D40 should be designed as coordinated 8-wire fanout banks, not independent point routes. Next action: map existing copper/through-hole obstacles around MCU x=118..136,y=44..112 and choose parallel fanout channels, then candidate a small 2-4 net bundle before promoting. Generator restored to D25 baseline in `8c099ae9a83cd995c3144e2a6d322096148466c2`; this is only a reproducible probe, not a promotion candidate.

## Relay-input fanout: D25/D26 promoted — 2026-10-01 13:55 CEST

- Copper map exposed two existing walls between MCU and ULN: net16/D22_START on F.Cu around x=128.5 and net17/D23_NEXT on B.Cu around x=130.5. Correct fanout topology is B.Cu from MCU across the F.Cu wall, via in the narrow inter-wall channel, then F.Cu across the B.Cu wall.
- D25/net20: first cross-layer candidate `5029ffc8...` had only C2 GND collision (F.Cu x=132.5). Bypass C2 right produced clean candidate `c38f647f09050b5915d6ec04d9d82ce5786b3b6f`, run `36857389224`: 154->153, zero routing DRC. Promoted official `927f3d8c9e16484040cb668d39c13c5091dda538`, sanity `f3f9c3ed69bae9054c121c1bc906fa3a7ca9ad80`.
- D26/net21: initial probe crossed D27 pad and D25. Final route uses B.Cu lane between MCU pad rows, via (129.5,50.09), F.Cu x=131.5 left of C2/D25, then horizontal into U1.2. Clean candidate `02ed5d909c3eda6c1582b5165e66c792c7ad92cd`, run `36858026986`: 153->152, zero routing DRC. Promoted official `d3f6b0a3d65586243c27053727199f439ad5e85a`, sanity `0ad9e773077e304f013aa442f453ca1791a9fdc0`.
- Official board is now **152 unconnected** with D25+D26 added to the previously clean K1-K16 milestone.
- D27/net22 candidate `e154a246...` reduces 152->151 with no shorts/clearance, but 4 crossings. Exact pairs from artifact `11160176400`: (1) D27 F start at 129.5,54.5 vs D22_START F track at 130.5,54; (2) D27 B pad escape vs D26 B horizontal y=50.09; (3) D27 F start vs D26 F vertical x=131.5; (4) D27 F vertical x=133 vs D26 F horizontal y=64.54. Next: redesign D27 as a comb lane around those four known segments; do not disturb validated D25/D26 unless coordinated candidate proves clean.

## D27/D28 fanout search — 2026-10-01 14:04 CEST

Official D25/D26 board independently revalidated by PCB KiCad Validation run `36858485914`: categories `{'lib_footprint_mismatch': 66, 'unconnected_items': 152}`; critical geometry/electrical categories none. Gate failure only incomplete connectivity; Gerbers skipped.

D27 experiments after checkpoint:
- right-side fanout `63ffe450...`: worse (1 short, 2 mask bridges, 3 crossings), reject.
- coordinated D26 repack + D27 `d67059cf...`: 1 short + 1 clearance + 3 crossings, reject; preserve clean official D26.
- best remains `e154a246...`: 152->151, **zero shorts/clearance**, four crossings, all previously identified.
D28 even-lane probe `d56c5145...`: 152->151 but 4 shorts + 2 mask + 2 crossings, confirming the narrow x=128.5..130.5 inter-wall channel cannot simply host additional independent vias/traces after D25/D26.

Conclusion: next progress requires a coordinated fanout-bus repack, not more isolated routes. Preserve official D25/D26 as baseline; model D27-D32 together, likely with staggered layer-change stations at different Y and/or one atomic repack of D25-D32. Generator restored to best D27 in `a4e29afc4a56b875a72812e5a8a0b55bf0510c06` for reproducible baseline.
