# PSN-Presepe PCB Rev-C

Rev-C is the active PCB revision.

## Mandatory corrections inherited from Rev-B review

- G5Q-1 footprint must match component-side/top-view PCB geometry.
- ULN2803C DIP-18 row spacing: 7.62 mm.
- Relay contact mapping: pad 2 = COM, pad 3 = NO, pad 4 = NC.
- Relay contact nets must maintain the 6 mm internal PCB isolation target from SELV and from contact circuits belonging to **different relays**.
- The 6 mm PCB rule does **not** apply between COM, NO and NC of the **same relay**: those three nets form the same SPDT switched contact circuit and their spacing is constrained by the relay/terminal geometry. This is an intentional scope exclusion, not a DRC waiver.
- For each channel, the protected mains-capable path is `Kx pad 2/3/4 (COM/NO/NC) -> Rx_COM/Rx_NO/Rx_NC copper -> JRx pad 1/2/3`. The complete path must satisfy the 6 mm PCB rule against SELV and other relay channels.
- Component-internal insulation is assessed separately from PCB copper spacing. Omron's G5Q datasheet specifies 6.4 mm minimum creepage and 5.5 mm minimum clearance for the coil-contact insulation system; these manufacturer values must not be misrepresented as 6 mm PCB spacing between COM/NO/NC.
- Manufacturer reference: Omron G5Q datasheet J155-E1, product family G5Q-1 SPDT (1c), https://components.omron.com/eu-en/datasheet_pdf/J155-E1.pdf.
- CI must prove the 6 mm rule actually fires using a deliberate positive-control violation.
- Routing must satisfy the rule itself; post-DRC exclusions are not acceptable.
- Rev-C release is not fabrication-ready until final KiCad DRC/ERC, mechanical, footprint, Gerber/mask/drill, silkscreen and preview gates all pass.

## Status

Work in progress. **DO NOT FABRICATE** until this README explicitly records final release validation.
