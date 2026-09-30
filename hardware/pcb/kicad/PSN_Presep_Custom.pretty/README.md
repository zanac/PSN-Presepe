# Custom KiCad footprints

## Relay_Omron_G5Q-1_SPDT.kicad_mod

Custom through-hole footprint for the **5-pin G5Q-1 SPDT family**, based on Omron's PCB mounting-hole drawing.

Important: the exact ordered relay must still be checked before fabrication. G5Q variants include 4-pin NO-only and 5-pin SPDT versions; PSN-Presepe requires the 5-pin SPDT version.

The manufacturer drawing specifies 1.3 mm PCB holes and the 7.62 / 10.16 / 2.54 / 5.08 mm mounting geometry. Pad numbering follows the manufacturer's bottom-view terminal numbering.

## Mega shield

The Mega header footprint is intentionally not recreated from memory. The Arduino Mega 2560 Rev3 is open-source hardware and Arduino publishes CAD/EAGLE/DXF resources. The final carrier footprint must be imported/derived from that official geometry so the non-standard Arduino header offset and mounting holes are exact.
