# KiCad source — Rev A

Current PCB source: `PSN-Presepe-Mega.kicad_pcb`.

## Current board
- working outline: **280 x 170 mm**
- 2 layers / 1.6 mm
- 77 referenced footprints
- 119 named nets
- all external terminal groups placed on the board perimeter
- connection-function silkscreen labels included
- 9 MOSFET thermal/heatsink area reserved
- 16 independent relay COM/NO/NC outputs

## Important routing status
The PCB is currently **unrouted on purpose**.

An audit of the earlier automatically generated textual tracks found same-layer crossings between different nets. All draft segments were therefore removed. This is safer than retaining routing that has not passed KiCad DRC.

Final routing must be done in a real KiCad environment using the interactive router and DRC. Do not add blind text-generated routing as a substitute for DRC.

## Relay/mains-capable contact area
Relay contacts are dry contacts. There is no phase or neutral distribution on this PCB. External wiring may nevertheless place 230 VAC on COM/NO/NC.

Requirements for final CAD:
- no SELV ground plane under contact routing;
- maintain physical separation between SELV and contact copper;
- configure and pass appropriate clearance/creepage rules;
- inspect board-edge and terminal clearances;
- verify terminal wire-entry orientation from the actual terminal footprint/datasheet.

## Schematic
`PSN-Presepe-Mega.sch` is a functional/legacy textual source and is not a substitute for a migrated, ERC-checked KiCad schematic.

## Fabrication
**DRAFT — NOT FOR FABRICATION.**

No production Gerber/Excellon set should be generated or ordered until KiCad ERC/DRC and final visual inspection pass.
