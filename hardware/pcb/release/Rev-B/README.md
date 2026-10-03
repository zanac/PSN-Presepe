# PSN-Presepe PCB Manufacturing Release — Rev B

This directory is the validated manufacturing snapshot produced by the KiCad 10 / Freerouting CI pipeline.

Contents:
- final routed KiCad PCB and design rules
- final DRC report
- BOM.csv
- CPL.csv
- Gerber copper, silkscreen and board outline
- Excellon drill file and Gerber job file
- front/back solder-mask Gerbers (.gts/.gbs), generated from the final routed PCB
- high-resolution technical and manual/documentation PNG previews, plus vector silkscreen SVG

Validation gates include 0 unconnected pads, relay/contact 6 mm clearance rule, Mega mechanical/pin/stackable checks, terminal silkscreen checks, production copper-width checks (+12V/GND, +5V_MEGA, RGB loads and relay contacts), solder-mask pad audit, and manufacturing export checks.

Solder-mask Gerbers are mandatory: CI audits F.Mask/B.Mask pad membership on the final post-SES PCB and requires non-empty .gts/.gbs fabrication files.

Generated from GitHub Actions run associated with the parent source commit. Do not edit generated manufacturing files manually.
