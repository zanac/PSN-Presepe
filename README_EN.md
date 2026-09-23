# PSN-Presepe

Arduino Mega 2560 controller for a modular 12V nativity scene.

## Controller mockup

![PSN-Presepe controller mockup](docs/a_high_resolution_infographic_wiring_diagram_photo.png)

> Conceptual mockup of the controller layout. For authoritative wiring, refer to the vector diagrams in the `docs/` directory.

## Wiring diagram

![PSN-Presepe Phase 1 + Phase 2 wiring diagram](docs/schema-fase1-fase2-pulito.png)

> This is the **current reference wiring diagram**. The 12 V RGB strip uses a common positive connection: +12 V is wired directly, while R, G and B are switched on the negative side by the MOSFET channels.

## Current hardware mapping

The Arduino pins **do not power the 12V loads directly**. Each Mega output drives the corresponding `PWM` input of a MOSFET channel. Two-wire loads can use the channel's `OUT+` / `OUT-` pair; the common-positive RGB strip is wired differently as shown below.

### MOSFET #1 — RGB sky

| Arduino Mega | MOSFET input | MOSFET output | 12V load | Control |
|---:|---|---|---|---|
| D2 | PWM1 | OUT1- | RGB strip — R return | PWM / dimmable |
| D3 | PWM2 | OUT2- | RGB strip — G return | PWM / dimmable |
| D4 | PWM3 | OUT3- | RGB strip — B return | PWM / dimmable |
| — | PWM4 | OUT4+ / OUT4- | **Free** | — |

The RGB strip is a **12V common-positive (common-anode)** load. Its single `+12V` wire is connected directly to the protected +12V distribution/WAGO and remains continuously supplied. The MOSFET channels switch the three R/G/B returns on the negative side:

```text
+12V PSU ──► fuse/distribution ──► RGB +12V common

RGB R ───────────────────────────► OUT1-
RGB G ───────────────────────────► OUT2-
RGB B ───────────────────────────► OUT3-

Mega D2 ─────────────────────────► PWM1  (Red)
Mega D3 ─────────────────────────► PWM2  (Green)
Mega D4 ─────────────────────────► PWM3  (Blue)

12V PSU + ───────────────────────► MOSFET DC+
12V PSU 0V ──────────────────────► MOSFET DC-
```

Do **not** wire the RGB strip as three independent two-wire loads. The `OUT1+`, `OUT2+` and `OUT3+` terminals are not needed for the RGB strip in this wiring scheme.

### Addressable WS2811 stars

The stars are now a **12 V WS2811 string with 50 individually addressable pixels**. They do not use a MOSFET channel; D5 carries the DATA signal.

```text
12V PSU + ──► fuse/distribution ──► WS2811 +12V
12V PSU 0V ───────────────────────► WS2811 GND
Arduino GND ──────────────────────► same common 0V
Mega D5 ── 330–470 ohm resistor ─► WS2811 DATA / DIN
```

With WS2811 pixels, **Arduino GND must share the 12 V PSU 0 V reference** so DATA has a valid electrical reference. The Mega remains powered from its separate 5 V USB supply; +12 V must never be connected to Arduino 5V or I/O pins.

Firmware can control each star independently with different brightness and color, progressively introducing random stars at twilight and fading them during dawn. MOSFET #1 channel 4 is now free.

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

With WS2811 stars, **Arduino GND and the 12 V PSU 0 V are intentionally common** to provide a reference for DATA. The Mega is still powered separately from its 5 V USB supply. Before final RGB wiring, verify with a multimeter whether DC+ is continuous with OUT1+/OUT2+/OUT3+/OUT4+ on the actual MOSFET board. Pump and mill require current/inrush and inductive-load protection checks before physical connection.

---

By **Vanni Brutto**
