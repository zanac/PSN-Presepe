# PSN-Presepe

Arduino Mega 2560 controller for a modular 12V nativity scene.

## Controller mockup

![PSN-Presepe controller mockup](docs/a_high_resolution_infographic_wiring_diagram_photo.png)

> Conceptual mockup of the controller layout. For authoritative wiring, refer to the vector diagrams in the `docs/` directory.

## Current hardware mapping

| Module | Input | Mega pin | Function |
|---|---|---:|---|
| MOSFET #1 | PWM1 | D2 | RGB red |
| MOSFET #1 | PWM2 | D3 | RGB green |
| MOSFET #1 | PWM3 | D4 | RGB blue |
| MOSFET #1 | PWM4 | D5 | Stars |
| MOSFET #2 | PWM1 | D6 | House lights |
| MOSFET #2 | PWM2 | D7 | Pump |
| MOSFET #2 | PWM3 | D8 | Mill |
| MOSFET #2 | PWM4 | D9 | Grotto / lamp posts |

Controls: D22 START/STOP, D23 NEXT, D24 TEST, A0 B10K cycle-speed potentiometer.

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
