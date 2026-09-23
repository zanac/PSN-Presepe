# PSN-Presepe

Arduino Mega 2560 controller for a modular 12V nativity scene.

## Controller mockup

![PSN-Presepe controller mockup](docs/a_high_resolution_infographic_wiring_diagram_photo.png)

> Conceptual mockup of the controller layout. For authoritative wiring, refer to the vector diagrams in the `docs/` directory.

## Current hardware mapping

The Arduino pins **do not power the 12V loads directly**. Each Mega output drives the corresponding `PWM` input of a MOSFET channel; the real load is connected to that channel's `OUT+` and `OUT-` terminals.

### MOSFET #1 — Sky and stars

| Arduino Mega | MOSFET input | MOSFET output | 12V load | Control |
|---:|---|---|---|---|
| D2 | PWM1 | OUT1+ / OUT1- | RGB strip — Red | PWM / dimmable |
| D3 | PWM2 | OUT2+ / OUT2- | RGB strip — Green | PWM / dimmable |
| D4 | PWM3 | OUT3+ / OUT3- | RGB strip — Blue | PWM / dimmable |
| D5 | PWM4 | OUT4+ / OUT4- | Stars | PWM / dimmable |

Example for the stars:

```text
Mega D5 ───────► PWM4

12V PSU ───────► DC+ / DC-     MOSFET #1

                 OUT4+ ───────► + Stars
                 OUT4- ───────► - Stars
```

### MOSFET #2 — Scenery and movements

| Arduino Mega | MOSFET input | MOSFET output | 12V load | Planned control |
|---:|---|---|---|---|
| D6 | PWM1 | OUT1+ / OUT1- | House lights | ON/OFF / PWM |
| D7 | PWM2 | OUT2+ / OUT2- | Pump | ON/OFF |
| D8 | PWM3 | OUT3+ / OUT3- | Mill | ON/OFF |
| D9 | PWM4 | OUT4+ / OUT4- | Grotto / lamp posts | ON/OFF / PWM |

D6-D9 are currently reserved for Phase 2; the present firmware implements the Phase 1 sky/stars sequence.

### Controls

| Arduino Mega | Device | Wiring |
|---:|---|---|
| D22 | START/STOP button | D22 ↔ button ↔ logic GND |
| D23 | NEXT button | D23 ↔ button ↔ logic GND |
| D24 | TEST button | D24 ↔ button ↔ logic GND |
| A0 | B10K cycle-speed potentiometer | 5V ↔ outer pin, A0 ↔ wiper, GND ↔ outer pin |

The buttons use `INPUT_PULLUP`, so no external pull-up resistor is required. Arduino logic GND is distributed to the MOSFET `GND1...GND4` inputs and controls through the logic-ground WAGO.

## Firmware

Open:

`firmware/PSN-Presepe/PSN-Presepe.ino`

with the standard Arduino IDE and select **Arduino Mega or Mega 2560**.

The current firmware implements Phase 1 (RGB sky + stars + controls). D6-D9 are reserved in the source for the Phase 2 second MOSFET and will be activated as the sequence is developed.

## GitHub Actions

`.github/workflows/build.yml` can be started manually from the GitHub Actions page and compiles for:

`arduino:avr:mega`

The compiled HEX/ELF files are uploaded as a GitHub Actions artifact.

## Simulation

`simulation/diagram.json` contains a starter Wokwi model. LEDs represent the real MOSFET channels, so the control logic can be tested without connecting 12V hardware.

The repository deliberately keeps Wokwi CI optional at this stage: the normal build works without any external secret/token.

## Electrical note

The Arduino 5V logic side and 12V power side are kept separate in the current design. Before final RGB wiring, verify with a multimeter whether DC+ is continuous with OUT1+/OUT2+/OUT3+/OUT4+ on the actual MOSFET board. Pump and mill require current/inrush and inductive-load protection checks before physical connection.

---

By **Vanni Brutto**
