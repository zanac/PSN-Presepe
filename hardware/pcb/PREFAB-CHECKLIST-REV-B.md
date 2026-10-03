# Rev B pre-fabrication checklist

This checklist supersedes the Rev-A checklist for PCB fabrication.
It distinguishes PCB-fabrication blockers from assembly/commissioning checks.

## PCB fabrication — machine verified

- [x] Final board routes with 0 unconnected pads.
- [x] KiCad final DRC has no unexpected violations.
- [x] Relay-contact to SELV and inter-relay isolation rules use the project 6 mm target and are active in final DRC.
- [x] Production copper-width gate passes: +12V/GND 3 mm target with explicitly controlled local neckdowns; RGB returns 1.5 mm; relay contacts 2 mm; +5V_MEGA 0.8 mm.
- [x] F.Mask and B.Mask contain pads and non-empty .gts/.gbs are generated.
- [x] External terminal silkscreen labels are present and visible after assembly.
- [x] All external wiring terminals are on the PCB perimeter with wiring/access side outward.
- [x] Arduino Mega R3 stackable/pass-through header geometry, pin mapping, USB and barrel-jack keepout checks pass.
- [x] High-resolution technical and manual/documentation PNG previews are generated with the manufacturing package.

## Assembly parts — must match footprints before ordering assembled boards

These are not bare-PCB Gerber blockers, but the exact purchased parts must be checked before PCBA/assembly ordering:

- [ ] J1 and J_* terminal blocks: exact manufacturer part, pitch, pin numbering, outward wire-entry and current/voltage rating.
- [ ] JR1..JR16: exact 5.08 mm 3-pole terminal part and rating for the intended external load.
- [ ] K1..K16: exact Omron G5Q-1 DC12 suffix (or footprint-compatible approved equivalent) and contact rating.
- [ ] Q1..Q9: exact IRLZ44N manufacturer variant and selected individual heatsink/insulation arrangement.
- [ ] RV1: exact B10K mechanical part and pin order.
- [ ] BZ1: exact passive piezo part and current. If its required drive exceeds the Mega D6 capability, use an external/next-revision driver; do not substitute an active/high-current buzzer silently.
- [ ] C1: exact 470 uF / 25 V body diameter, lead pitch and polarity.
- [ ] HDR-MEGA-STACK: complete Mega R3 stackable female/pass-through set with long lower tails; mandatory fitted item.

## System commissioning — not a bare-PCB fabrication blocker

- [ ] Record final STELLE and CASETTE WS2811 pixel counts and measured/worst-case current.
- [ ] Size the external 12 V supply, J1 wiring and upstream fuse from RGB + relays + Mega + both WS2811 strings + engineering margin.
- [ ] Verify Mega 5 V regulator temperature with the real OLED/peripheral load when powered from 12 V VIN.
- [ ] Verify ULN2803 package temperature with the maximum simultaneous relay-coil load.
- [ ] Verify MOSFET/heatsink temperature at the real RGB load.
- [ ] Confirm enclosure, pollution/installation conditions and external 230 V wiring practice before using relay contacts at mains voltage. The PCB DRC is not a safety certification.

## Schematic / ERC status

- [x] Rev-B has a real KiCad 10 electrical schematic with instantiated symbols, pins and named electrical nets.
- [x] KiCad 10 successfully opens the schematic and exports its electrical netlist.
- [x] The KiCad-exported schematic netlist covers the connected PCB references and named nets.
- [x] KiCad 10 schematic ERC passes in CI.
- [x] A legacy Eeschema .sch + cache library representation is generated from the same validated PCB connectivity map.
- [x] Modern and legacy schematics plus the ERC report are staged with the Rev-B release package.
