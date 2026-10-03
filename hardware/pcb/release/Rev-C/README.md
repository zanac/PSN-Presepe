# PSN-Presepe PCB Rev-C

Rev-C is the active PCB revision.

## Mandatory corrections inherited from Rev-B review

- G5Q-1 footprint must match component-side/top-view PCB geometry.
- ULN2803C DIP-18 row spacing: 7.62 mm.
- Relay contact mapping: pad 2 = COM, pad 3 = NO, pad 4 = NC.
- Relay contact nets must maintain the 6 mm internal isolation target from SELV and from contacts belonging to other relays.
- CI must prove the 6 mm rule actually fires using a deliberate positive-control violation.
- Routing must satisfy the rule itself; post-DRC exclusions are not acceptable.
- Rev-C release is not fabrication-ready until final KiCad DRC/ERC, mechanical, footprint, Gerber/mask/drill, silkscreen and preview gates all pass.

## Status

Work in progress. **DO NOT FABRICATE** until this README explicitly records final release validation.
