# Simulation

Starter Wokwi hardware model for PSN-Presepe.

The simulated LEDs stand in for the real MOSFET/load channels:

- D2 RGB red
- D3 RGB green
- D4 RGB blue
- D5 stars
- D6 house lights
- D7 pump
- D8 mill
- D9 grotto/lamp posts

Buttons:
- D22 START/STOP
- D23 NEXT
- D24 TEST

Potentiometer:
- A0 cycle speed

The normal GitHub Action only compiles the firmware and does not require a Wokwi token.
The `wokwi.toml` and `diagram.json` are included so CI simulation can be enabled later.
