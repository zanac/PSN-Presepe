# PCB assembly requirements

## Arduino Mega 2560 R3 stacking headers

The PSN-Presepe PCB is designed as a **stackable Arduino Mega 2560 R3 shield**.

The PCB assembly order must include the complete set of Arduino Mega R3 headers as **female stackable / pass-through headers**, soldered to the PSN-Presepe PCB.

Requirements:
- Arduino Mega 2560 R3 shield pin geometry, including the non-standard D7-D8 spacing.
- Female sockets accessible from the **top side** for a future additional shield.
- Long male tails on the **bottom side** to plug into the Arduino Mega 2560 R3.
- Through-hole soldered assembly.
- Do **not** substitute closed/non-stackable female headers.
- Keep the full Mega stacking envelope free of components; CI enforces this with `hardware/pcb/tools/check_mega_stackable.py`.

Assembly intent:

`future shield -> PSN-Presepe PCB -> Arduino Mega 2560 R3`

These headers are mandatory fitted components when ordering an assembled PCB, not DNI/DNP parts.
