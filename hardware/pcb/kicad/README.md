# KiCad PCB — Rev A (routed and validated)

## Production status
The Rev A PCB is routed and validated by the KiCad 10 / Freerouting CI pipeline.

Validated run: **GitHub Actions #65**  
Validated source commit: `4f67314c46dd59c536ec106bf252f43676114665`

Final automated gates:
- board outline: **280 x 170 mm**
- 2 copper layers
- **0 unconnected pads**
- no unexpected DRC categories
- allowed DRC category: `lib_footprint_issues` only
- relay/contact custom clearance gate: **6 mm**
- Mega stackable expansion envelope: PASS
- Mega physical pin mapping: PASS
- Mega mechanical geometry / mandatory assembly BOM: PASS
- external terminal silkscreen labels: PASS
- production Gerber/drill export: PASS
- BOM/CPL export: PASS

## Manufacturing package
The CI artifact `pcb-manufacturing-complete` contains:
- final routed `PSN-Presepe-Mega-FREEROUTED.kicad_pcb`
- `PSN-Presepe-Mega-FREEROUTED.kicad_dru`
- `freerouted-k10.drc.txt`
- `BOM.csv`
- `CPL.csv`
- F.Cu / B.Cu Gerbers
- F.Silkscreen / B.Silkscreen Gerbers
- Edge.Cuts Gerber
- Excellon drill file
- Gerber job file

KiCad accepts `F.Mask` and `B.Mask`, but this board currently has no plottable solder-mask content on those layers, so KiCad omits empty .gts/.gbs files. Empty mask files are not fabricated or synthesized by the workflow.

## Important electrical safety note
The 16 relay COM/NO/NC groups are dry contacts and may be wired externally to mains voltage. The PCB does not distribute phase or neutral. The validated custom rule enforces the designed separation between relay contact routing and SELV circuitry. Final assembly and mains wiring must still use appropriately rated relays, terminals, wire, enclosure, fusing and workmanship.

## Source files
The editable KiCad sources remain in this directory. The manufacturing output is generated deterministically by:
`.github/workflows/pcb-freerouting-k10.yml`.

Do not manufacture from older draft routing artifacts or from the original unrouted PCB alone; use the validated routed manufacturing package produced by the CI pipeline.
