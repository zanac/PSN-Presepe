# Rev A current budget

This is a design budget, not a final certification calculation.

| Load | Known / preliminary current at 12 V |
|---|---:|
| RGB strips, total installed 5 m / 60 W rating | ~5.00 A max theoretical |
| 16 x Omron G5Q-1 DC12 coils | ~0.533 A |
| Arduino Mega through VIN | TBD / operating dependent |
| WS2811 STELLE string | TBD |
| WS2811 CASETTE string | TBD |
| Margin / transients | TBD |
| **Known subtotal before Mega + WS2811** | **~5.53 A** |

## Relay calculation

Omron specifies approximately 33.3 mA rated current and 400 mW coil consumption for the 12 V G5Q-1 class. Sixteen simultaneously energized coils therefore require about 0.533 A and 6.4 W.

## Consequences

- The exact J1 two-pole terminal part must be verified for continuous current above the final design current.
- The +12 V source, wiring and PCB distribution must be sized from the final total, not from the RGB load alone.
- Main +12 V/GND routing uses the preliminary `HIGH_CURRENT_12V` class and should use wide copper pours where the relay-contact isolation area permits.
- RGB switched returns use `RGB_LOAD`.
- Mega VIN regulator dissipation must be checked separately because 12 V input is linearly reduced onboard.
- WS2811 STELLE and CASETTE current must be added once final pixel counts/current assumptions are fixed.
- No production Gerber approval until connector current rating, copper weight/temperature rise and final total current are checked.
