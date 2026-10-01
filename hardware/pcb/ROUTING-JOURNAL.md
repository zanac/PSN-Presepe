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
- Unconnected items: **161**
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
