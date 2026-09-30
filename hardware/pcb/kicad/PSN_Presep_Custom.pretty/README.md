# Custom KiCad footprints — Rev A

## Relay_Omron_G5Q-1_SPDT.kicad_mod
Custom through-hole footprint for the **5-pin Omron G5Q-1 SPDT family**.

Rev A pin mapping used by the PCB:
- pins 1 and 5: coil
- pin 2: NC
- pin 3: COM
- pin 4: NO

The footprint uses 1.3 mm drills and the mounting geometry transcribed from the Omron PCB drawing. The exact relay part ordered for assembly must still be checked against the manufacturer datasheet before fabrication.

## TerminalBlock_Phoenix_MKDS-1.5-3-5.08.kicad_mod
Three-pole, 5.08 mm pitch terminal footprint intended for Phoenix Contact MKDS 1,5/3-5,08 / 1715734 geometry.

Before fabrication verify:
- exact purchased terminal family;
- drill and pin dimensions;
- body/courtyard dimensions;
- **wire-entry direction relative to footprint rotation**.

The PCB requirement is binding: every external terminal must have its wire-entry side facing outward from the PCB perimeter.

## Arduino_Mega2560_R3_Shield.kicad_mod
The Mega footprint currently used by Rev A came from the public `Alarm-Siren/arduino-kicad-library` resource and was adapted/checked for this project.

It is **not described as an official Arduino footprint**.

Before fabrication it must be cross-checked against the mechanical dimensions/header locations of the exact Arduino Mega 2560 R3-compatible board that will be plugged into the carrier, including:
- non-standard Arduino header spacing;
- mounting-hole positions;
- USB/jack/reset mechanical clearance;
- VIN, 5V and GND header positions.

## Fabrication rule
These custom footprints are design inputs, not proof of manufacturability. Final approval requires footprint/datasheet review plus KiCad DRC and physical Gerber inspection.
