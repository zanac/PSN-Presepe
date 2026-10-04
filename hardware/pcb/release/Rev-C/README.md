# Rev C legacy workspace — superseded

The official PSN-Presepe Rev C design, manufacturing package, reports and reproducible build are now in:

`hardware/pcb/PSN-Presepe-RevC/`

Do **not** fabricate from this legacy workspace or from the old `hardware/pcb/kicad/` experimental routing files.

The accepted Rev C isolation targets are:
- relay-contact copper to SELV: >= 6.0 mm;
- contact circuits of different relays: >= 5.0 mm;
- COM/NO/NC within the same relay contact circuit: >= 2.0 mm;
- relay-contact copper to board edge: >= 3.0 mm.

Final production approval is gated by the official Rev C reports, KiCad 10 CI, and the physical 1:1 component fit check.

Historical files under Rev-B and old routing workflows are retained only for traceability.
