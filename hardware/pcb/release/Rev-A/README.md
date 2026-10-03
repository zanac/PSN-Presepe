# ⚠️ REVOKED — DO NOT MANUFACTURE

**Rev A is NOT production-ready and MUST NOT be sent to fabrication.**

Post-release audit found blocking routing/manufacturing defects:
- all routed copper segments are 0.20 mm, including power and relay-contact nets;
- required power/current track classes were not preserved by the autorouter;
- relay-contact/SELV and inter-relay 6 mm isolation must be revalidated geometrically after rerouting;
- solder-mask Gerbers F.Mask/B.Mask are missing even though PCB pads use *.Mask;
- previous final DRC gate is therefore not sufficient evidence for production approval.

This directory is retained only as an audit/debug snapshot. A later validated revision must replace it before fabrication.

# PSN-Presepe PCB Manufacturing Release — Rev A

This directory is the validated manufacturing snapshot produced by the KiCad 10 / Freerouting CI pipeline.

Contents:
- final routed KiCad PCB and design rules
- final DRC report
- BOM.csv
- CPL.csv
- Gerber copper, silkscreen and board outline
- Excellon drill file and Gerber job file

Validation gates include 0 unconnected pads, relay/contact 6 mm clearance rule, Mega mechanical/pin/stackable checks, terminal silkscreen checks, and manufacturing export checks.

F.Mask/B.Mask are accepted by KiCad but contain no plottable content on this design, so KiCad omits empty .gts/.gbs files rather than generating synthetic empty masks.

Generated from GitHub Actions run associated with the parent source commit. Do not edit generated manufacturing files manually.
