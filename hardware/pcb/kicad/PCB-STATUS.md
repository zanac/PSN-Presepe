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

Preliminary net classes are now stored in the KiCad project:
- Default signal: 0.30 mm track / 0.25 mm clearance;
- SELV_POWER: 1.00 mm track / 0.30 mm clearance;
- RELAY_CONTACT: 1.00 mm track / **1.00 mm preliminary clearance**.

The 1.00 mm relay-contact clearance is only a routing placeholder, **not a declaration of 230 V safety compliance**. Final creepage/clearance must be chosen and verified for the actual installation, pollution degree, material and applicable standard.

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
Six 3.2 mm NPTH mounting holes are present. Their positions were mechanically rechecked after placement; the simplified center-distance audit reports no other footprint center within 10 mm. Final courtyard/enclosure fit still requires KiCad/physical review.

Final enclosure/standoff fit still requires physical/mechanical review.

## Netlist audit
- exactly 119 global net declarations;
- 119 unique net IDs and names;
- no duplicate, orphan or unused nets;
- no one-pad electrical nets;
- all firmware-required Mega pins are assigned;
- 46 unassigned Mega pads are intentionally unused headers/functions.

## Project portability
The project-local `PSN_Presep_Custom.pretty` library now contains every footprint referenced with the `PSN_Presep_Custom:` prefix in the PCB, including ULN2803 and all dedicated terminal blocks.

A project-local `fp-lib-table` registers that library through `${KIPRJMOD}`, so opening the project does not depend on a separately installed custom footprint library.

Audit result:
- 14 custom footprint names used by the PCB;
- 14 corresponding library footprint files present;
- no board-specific net assignments retained in the extracted library footprints.

## Fabrication status
**DRAFT — NOT FOR FABRICATION.**

No ERC/DRC has been run in a real KiCad environment and no Gerber/Excellon set from this revision is approved for manufacture.


## KiCad 9 real validation checkpoint — 2026-09-30
The board is now successfully parsed by **KiCad 9.0.9** in GitHub Actions (`FULL_LOAD_OK`).

The first real DRC exposed malformed legacy board syntax and placement/footprint defects. Corrected items include:
- KiCad 9 canonical board layer IDs;
- malformed pad/net syntax;
- corrupted Mega VIN/embedded-net block;
- U1/U2 collision with Mega headers;
- C2/C3 collision with ULN2803 pads;
- H2 collision with JR9;
- **Omron G5Q-1 SPDT footprint geometry corrected from the official PCB mounting-hole drawing**.

After these corrections, the latest checked DRC report contains **no remaining shorting-items, electrical clearance, hole-clearance or solder-mask-bridge violations**.

Remaining categories are expected/unresolved work:
- 194 unconnected items because routing is intentionally still absent;
- footprint-library parity/configuration warnings;
- silkscreen text-height/overlap/copper warnings;
- one legacy non-mirrored back-layer text item in the Mega footprint.

This is a major validation checkpoint but **not fabrication approval**. Routing, final isolation strategy, silkscreen cleanup, library parity, final DRC and Gerber inspection are still required.

## KiCad 9 parser validation
- KiCad 9.0.9 now loads the complete PCB successfully (`FULL_LOAD_OK`).
- Board layer IDs were corrected to KiCad 9 canonical IDs.
- DRC is now executed in GitHub Actions; reports must be interpreted against the exact HEAD commit because placement evolved during parser repair.
