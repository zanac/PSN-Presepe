# PCB autonomous work history

Concise durable milestones for restarting long routing sessions.

## 2026-10-01 — checkpoint system introduced
- Stable branch: `dev`.
- Restart summary: `worklog/CURRENT.md`.
- Official PCB SHA at checkpoint: `0ef369ad11c01e8dfbe0f1b5c71bfe0acbc25dce`.
- Official routed copper: 77 segments across 18 nets.
- Real KiCad 9.0.9 DRC: 0 error-severity violations, 167 unconnected items.
- Baseline before routing work was 194 unconnected items; verified progress = 27 fewer.
- Routed nets present: D22_START, D23_NEXT, D24_TEST, D20_SDA, D21_SCL, A0_POT, GATE_Q1..Q9, RELAY1_COIL_LOW, RELAY2_COIL_LOW, RELAY3_COIL_LOW.
- K1/K2/K3 coil routes were promoted only after candidate validation.
- Added isolated `PCB Routing Lab` workflow on `dev` so candidate experiments no longer depend on the stable fabrication workflow.
- Current experiment: RELAY4_COIL_LOW / K4.
