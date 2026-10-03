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
