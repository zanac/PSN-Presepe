# PCB CAD status — Rev A

`PSN-Presepe-Mega.kicad_pcb` is the current physical board source.

## Current mechanical state
- outline: **280 x 170 mm** (working coordinates 20..300 x 20..190 mm);
- FR-4 1.6 mm, 2 layers;
- Arduino Mega 2560 carrier/shield architecture;
- 16 Omron G5Q-1 relay footprints in two rows with increased wiring space;
- 16 relay COM/NO/NC terminal blocks on the PCB perimeter;
- all low-voltage terminal blocks on the PCB perimeter with outward wire-entry intent;
- 9 IRLZ44N with a dedicated heatsink/airflow area;
- B10K potentiometer and buzzer onboard;
- terminal-function silkscreen labels included.

## Electrical/netlist state
- 119 named nets;
- 77 electrical/component footprints plus 6 M3 NPTH mounting-hole footprints;
- relay contact mapping verified as G5Q: pins 1/5 coil, 3 COM, 2 NC, 4 NO;
- each JR1..JR16 is independent COM/NO/NC; no mains L/N bus exists on the PCB;
- Mega firmware pin mapping is preserved.

## Routing state
**Routing is intentionally reset to zero.**

A geometric audit of the earlier text-generated draft routing found same-layer crossings between different nets. Those segments were removed rather than presenting an unsafe or unroutable board as complete.

Final routing must be performed/checked in KiCad with real interactive routing and DRC. In particular:
- SELV and relay-contact routing must remain physically separated;
- no SELV GND plane is allowed under the relay-contact routing area;
- mains-capable contact creepage/clearance must be configured and checked;
- board-edge, pad, via and track clearances must pass DRC.

## Silkscreen
Small connection labels are present near every terminal group:
- power: 12V / GND;
- OLED: 5V / GND / SDA / SCL;
- START, AVANTI, TEST + GND;
- CIELO, TRAMONTO, ALBA: 12V / R / G / B;
- STELLE, CASETTE: 12V / GND / DATA;
- R1..R16: COM / NO / NC.

The final KiCad review must confirm that every label follows the actual terminal wire-entry orientation and does not overlap pads/courtyards.

## Mechanical mounting
Six 3.2 mm NPTH mounting holes are present:
- four near the board corners;
- two intermediate supports near x=135 mm on the top/bottom edges.

Final enclosure/standoff fit still requires physical/mechanical review.

## Netlist audit
- exactly 119 global net declarations;
- 119 unique net IDs and names;
- no duplicate, orphan or unused nets;
- no one-pad electrical nets;
- all firmware-required Mega pins are assigned;
- 46 unassigned Mega pads are intentionally unused headers/functions.

## Fabrication status
**DRAFT — NOT FOR FABRICATION.**

No ERC/DRC has been run in a real KiCad environment and no Gerber/Excellon set from this revision is approved for manufacture.
