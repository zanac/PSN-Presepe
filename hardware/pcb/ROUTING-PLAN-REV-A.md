# Rev A routing plan

Status: engineering plan for the intentionally unrouted Rev A PCB. Not fabrication approval.

## Order

1. Relay-contact nets (`R1..R16_COM/NO/NC`) first, kept entirely in the relay-contact region.
2. Relay coil +12 V and `RELAY*_COIL_LOW` paths.
3. Main +12 V / GND distribution, using wide traces or reviewed copper pours only in the SELV region.
4. RGB load returns (`*_NEG`) from terminals to MOSFET drains.
5. +5 V, OLED, buttons, potentiometer and buzzer.
6. PWM/data/control nets from Mega to gate resistors, ULN2803 and WS2811 terminals.
7. Final ground strategy only after relay-contact keepout review.

## Net classes

- `Default`: 0.30 mm logic.
- `SELV_POWER`: 0.80 mm preliminary low-current power.
- `RGB_LOAD`: 1.50 mm preliminary MOSFET-to-strip return paths.
- `HIGH_CURRENT_12V`: 3.00 mm preliminary +12 V/GND backbone; copper pours preferred where safe.
- `RELAY_CONTACT`: 1.00 mm track and 1.00 mm preliminary clearance.

All widths are routing constraints, not final current/standards certification.

## Relay-contact isolation

- Never route SELV nets between relay contact pads and their perimeter terminals.
- Never place GND/+12 V/+5 V copper pours under the relay-contact routing area.
- Contact nets remain independent; there is no PCB mains phase or neutral bus.
- Keep contact routing on a dedicated physical corridor wherever practical.
- Any via used on a relay-contact net must remain inside the contact region.
- Final creepage/clearance is installation/standard dependent and must be reviewed before fabrication.
- Omron G5Q-1 internal relay specification is not a substitute for PCB-level spacing validation.

## High-current distribution

Known RGB installation rating is about 60 W total at 12 V (about 5 A) before adding relay coils, WS2811 loads and Mega current. Therefore:
- J1 current rating must be verified against the exact purchased terminal block;
- +12 V and GND backbone should use broad copper where isolation permits;
- avoid neck-downs near J1 and RGB terminals;
- RGB drain paths use the dedicated `RGB_LOAD` class;
- final copper weight and temperature-rise calculation remains mandatory.

## Routing acceptance

A routing pass is accepted only when:
- KiCad reports zero shorts and zero electrical-clearance errors;
- all 194 current unconnected-item records are resolved;
- relay-contact and SELV regions have been visually reviewed;
- no unreviewed copper zone is present;
- the critical net invariants in `pcb_sanity.py` still pass;
- Gerbers are generated only by the CI after the DRC error gate succeeds.
