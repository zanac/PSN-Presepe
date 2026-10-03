# Firmware ↔ PCB pin map — Rev A

Source checked: `firmware/PSN-Presepe/PSN-Presepe.ino` on branch `dev`.

| Function | Mega pin | PCB net / destination |
|---|---:|---|
| CIELO R | D2 | D2_CIELO_R → RG1/Q1 |
| CIELO G | D3 | D3_CIELO_G → RG2/Q2 |
| CIELO B | D4 | D4_CIELO_B → RG3/Q3 |
| STELLE DATA | D5 | D5_STELLE_DATA → J_STELLE DATA |
| BUZZER | D6 | D6_BUZZER → BZ1 |
| TRAMONTO R | D7 | D7_TRAM_R → RG4/Q4 |
| CASETTE DATA | D8 | D8_CASETTE_DATA → J_CASETTE DATA |
| TRAMONTO G | D11 | D11_TRAM_G → RG5/Q5 |
| TRAMONTO B | D12 | D12_TRAM_B → RG6/Q6 |
| OLED SDA | D20 | D20_SDA → J_OLED |
| OLED SCL | D21 | D21_SCL → J_OLED |
| START | D22 | D22_START → J_START |
| AVANTI/NEXT | D23 | D23_NEXT → J_NEXT |
| TEST | D24 | D24_TEST → J_TEST |
| Relay 1..16 | D25..D40 | U1/U2 ULN2803 → K1..K16 |
| ALBA R | D44 | D44_ALBA_R → RG7/Q7 |
| ALBA G | D45 | D45_ALBA_G → RG8/Q8 |
| ALBA B | D46 | D46_ALBA_B → RG9/Q9 |
| B10K wiper | A0 | A0_POT → RV1 |
| OLED/B10K supply | 5V | +5V_MEGA |
| Logic/load return | GND | GND |
| Mega input supply | VIN | +12V |

## Relay polarity
Firmware currently defines:
`RELE_ACTIVE_LOW = false`

With the Rev A ULN2803 low-side coil driver:
- Mega output HIGH → ULN channel sinks current → relay coil energized;
- Mega output LOW → relay off.

This is therefore consistent with the intended onboard relay-driver architecture.

## WS2811
Rev A deliberately connects D5 and D8 directly to the external DATA terminals. No series DATA resistor or logic buffer is present in the approved Rev A design.

## Audit result
The firmware pin definitions checked on `dev` match the PCB Rev A named nets for RGB, WS2811, buzzer, buttons, potentiometer, OLED and all 16 relays.
