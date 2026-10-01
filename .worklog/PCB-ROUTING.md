# PCB routing worklog

This file is the persistent restart checkpoint for long PCB-routing sessions.

## Resume contract

1. Read this file first.
2. Fetch current `dev` and `wip/pcb-routing` HEADs before changing anything.
3. Experiments and partially validated routes stay on `wip/pcb-routing`.
4. Prefix intermediate save points with `WIP:`.
5. Update this file after every meaningful experiment with commit SHA, CI run, DRC result and next action.
6. Only routes proven by KiCad DRC and connectivity reduction may be promoted to `dev`.
7. Never force-update `dev`; fetch fresh files before every write.
8. The production/fabrication gate remains on `dev`.

## Checkpoint — 2026-10-01

- WIP branch created from dev SHA: `d364e63c1caabbaacaafa5bef12728aee291bc30`.
- PCB parser: OK under KiCad 9.
- Fabrication source has progressed beyond the original zero-track draft; current dev history reports a validated baseline around 169 unconnected items before the latest K2 experiment.
- K1 coil route was promoted after KiCad validation in commit `f73b14ec0d2dd4d86b28c541501978ca8525dc9`.
- Rotated relay pad-coordinate audit was corrected in commit `097a0a13692466858d6e51f11b53f1ddc64de986`.
- Latest CI run checked: `36821407171`, commit `d364e63c1caabbaacaafa5bef12728aee291bc30`, title “Test K2 coil-low route from corrected relay geometry”; conclusion: failure. This is the immediate investigation target.
- Earlier low-risk D22/D23/D24 candidate demonstrated the non-destructive candidate method but its first geometry had shorts/crossings; do not reuse that obsolete path blindly.
- Critical invariants remain: relay G5Q corrected pinout; all terminals on perimeter; MOSFET heatsink spacing; no unreviewed copper zones; explicit fabrication gate.

## Immediate next actions

1. Read CI logs/artifact for run 36821407171.
2. Determine whether K2 candidate failure is DRC geometry, connectivity, or workflow/gate-only failure.
3. Correct K2 only on this WIP branch and commit as `WIP: ...`.
4. Re-run/inspect KiCad validation.
5. If clean and it reduces unconnected count exactly as expected, record the successful SHA/run here.
6. Promote the proven change to `dev` as a clean commit, then advance/rebase this WIP branch from fresh dev.
7. Continue K3..K16 one small validated route group at a time.

## Durable design blockers before fabrication

- Exact J1 part/current rating.
- Exact terminal-block wire-entry direction and ratings.
- Final WS2811 current budget.
- Mega VIN regulator thermal check.
- PCB-level relay-contact creepage/clearance review for actual external voltage/environment.
- Footprint-library mismatch cleanup.

## Investigation: K2 candidate

Run `36821407171` was inspected in full. The K2 route itself is clean:
- baseline: 169 unconnected;
- candidate: 168 unconnected;
- reduction: exactly 1;
- candidate non-routing warnings: 66 library mismatches, same as baseline;
- critical/detail DRC blocks: 0;
- no shorts, clearance errors, crossings or mask bridges.

The workflow failed because `compare_unconnected.py` in `CANDIDATE_MODE=baseline` exits 1 when connectivity changes. That behavior is wrong for an experimental route whose purpose is to improve connectivity. **Do not change the K2 geometry; fix the comparator/gate semantics first.**

## Checkpoint protocol now active

The WIP branch has isolated CI enabled. Long routing work should be split into these durable stages:
1. `WIP: plan <net/group>` — record baseline and intended geometry;
2. `WIP: test <net/group>` — candidate generator/geometry only;
3. `WIP: validate <net/group>` — record exact KiCad run ID, DRC categories and connectivity delta;
4. `WIP: ready <net/group>` — only after zero new critical DRC categories;
5. promote the proven PCB change to fresh `dev`, then checkpoint the new dev SHA here.

A restart therefore needs only this file, the two branch HEADs and the most recent referenced CI run/artifact.

## READY: K2 coil-low

WIP CI run `36821692685` on SHA `287e144fcbafdfa45f7119e9d23096b7108b5a8e` revalidated the K2 candidate after comparator repair:
- source baseline: 169 unconnected;
- K2 candidate: 168 unconnected;
- connectivity reduction: 1;
- non-routing warnings: 66 baseline / 66 candidate;
- critical DRC categories: none;
- detail blocks: 0.

K2 geometry is therefore READY for clean promotion to fresh `dev`. Candidate path: U1.17 (145.16,64.54) -> (148,66.5) -> (173,66.5) -> (175.62,64) -> K2.5 (175.62,60), F.Cu 0.30 mm, net 37 RELAY2_COIL_LOW.

## Promoted baseline

K2 was promoted to `dev` in commit `d8761dd1bf4adc2f0b2304a1835ebe33a3bc4dd1`; sanity whitelist updated in `a728d711a275e50bf1e7d17cdb207a2b63e460ca`. Stable validation workflow run `36821946903` confirmed the official PCB at **168 unconnected items, 0 error-severity DRC violations, no critical geometry/electrical categories**. Stable and experimental CI were then separated (`ae11ce53...`, `727d91d4...`).

Next routing target: K3 / `RELAY3_COIL_LOW` from U1 output to K3 coil pad, using the corrected Y-down rotated relay geometry. Start from fresh dev HEAD, not from the old K2 candidate generator.
