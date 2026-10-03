# PSN-Presepe PCB Rev B — design notes

This document consolidates the still-relevant engineering notes from the superseded Rev-A documents. Rev-A files remain available in Git history.

## Architecture
- Arduino Mega 2560 R3 shield, stackable female/pass-through headers mandatory.
- Single external +12 V input. The Mega is supplied through VIN; never apply +12 V to the Mega +5 V rail.
- Mega-generated +5 V is used for low-power logic/peripherals such as OLED and potentiometer.
- Common low-voltage ground is used by Mega, MOSFET stages, ULN2803 drivers and 12 V loads.
- External wiring terminals are on the PCB perimeter with access facing outward.

## Loads and drivers
- Nine IRLZ44N-class MOSFET PWM channels are used for the RGB lighting outputs.
- Gate network: 100 ohm series resistor and 100 kohm pull-down per MOSFET.
- Two ULN2803C devices drive sixteen 12 V relay coils.
- Relay footprint target: Omron G5Q-1 DC12 or an explicitly verified footprint-compatible equivalent.
- Relay contacts are brought to individual COM/NO/NC edge terminals; there is no onboard mains distribution bus.
- WS2811 data outputs are direct logic connections; final pixel count/current is a commissioning input.
- BZ1 is intended for a passive piezo on Mega D6. Use an external/next-revision driver if the selected buzzer exceeds the MCU drive capability.

## Power and thermal notes
- The +12 V rail supplies Mega VIN, relay coils, RGB loads and the WS2811 strings.
- A G5Q-1 12 V coil is budgeted at about 33 mA / 0.4 W; sixteen energized coils are about 0.53 A / 6.4 W before other loads.
- Each ULN2803 can therefore see roughly 0.27 A with all eight assigned relay coils energized; verify package temperature during commissioning.
- Verify the Mega onboard regulator temperature with the actual 12 V VIN and peripheral load.
- IRLZ44N TO-220 tabs are drain-connected. Separate heatsinks must not electrically touch unless suitable insulation is used.
- Final 12 V supply, wiring and upstream fuse must be sized from measured/worst-case RGB + relay + Mega + WS2811 load with engineering margin.

## PCB electrical rules
- +12V/GND: 3 mm production target with only explicitly controlled local neckdowns.
- RGB load returns: 1.5 mm target.
- Relay-contact copper: 2 mm target.
- +5V_MEGA: 0.8 mm target.
- Relay-contact to SELV and inter-relay contact isolation use the project 6 mm target and are checked by final KiCad DRC.
- Same-relay COM/NO/NC terminal geometry is constrained by the selected 5.08 mm terminal pitch and is not represented as a 6 mm pairwise rule.

## Safety scope
The PCB DRC and internal 6 mm rules are engineering checks, not a declaration of regulatory or mains-safety certification. Final suitability depends on the exact relay/terminal parts, PCB material and copper, pollution degree, overvoltage category, altitude, enclosure, fusing/protection and installation practice.

## Source of truth
Rev-B fabrication source, Gerbers, drill files, masks, previews, schematics, ERC/DRC reports and release README are under `hardware/pcb/release/Rev-B/`. The pre-fabrication and commissioning status is tracked in `PREFAB-CHECKLIST-REV-B.md`.
