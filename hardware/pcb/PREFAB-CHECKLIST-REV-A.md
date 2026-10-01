# Rev A pre-fabrication physical-part checklist

These checks are mandatory before removing the DRAFT / NOT FOR FABRICATION status.

| Item | Current design assumption | Required verification |
|---|---|---|
| J1 12 V input terminal | 2-pole terminal, single board supply | Exact manufacturer/part number, pitch, wire-entry direction and continuous current rating above final board current |
| JR1..JR16 relay terminals | Phoenix-style 3-pole 5.08 mm candidate, COM/NO/NC | Exact purchased part, footprint dimensions, pin numbering, wire-entry side and voltage/current rating |
| RGB terminals | 4-pole perimeter terminal | Exact part, pitch, current rating per pole and outward wire-entry direction |
| WS2811 terminals | 3-pole perimeter terminal | Exact part, pitch/current rating and outward wire-entry direction |
| OLED/button terminals | low-current perimeter terminals | Exact part/pitch and outward wire-entry direction |
| K1..K16 | Omron G5Q-1 DC12 candidate | Exact ordered suffix and contact ratings for intended external loads |
| Q1..Q9 | IRLZ44N TO-220 | Exact manufacturer part, thermal characteristics and chosen heatsink dimensions/insulation |
| RV1 | B10K board potentiometer | Exact physical part and pin numbering must match GND / wiper A0 / +5 V |
| BZ1 | board buzzer on D6/GND | Exact active/passive type and operating current; add transistor driver if Arduino-pin current is not appropriate |
| C1 | 470 uF / 25 V electrolytic | Physical diameter/lead pitch and polarity marking |
| Arduino Mega | Mega 2560 R3-compatible board | Mechanical header alignment and VIN behavior of the exact board used |

## Electrical blockers

- Final WS2811 STELLE and CASETTE maximum currents are still required for the final 12 V budget.
- Final J1/wiring/PCB current target cannot be signed off until those currents are known.
- Mega regulator dissipation from a 12 V VIN source must be checked against actual 5 V load.
- Relay-contact PCB creepage/clearance must be reviewed for the real external voltage/environment.
- No production Gerbers until all items above that affect footprint, current or isolation are resolved.
