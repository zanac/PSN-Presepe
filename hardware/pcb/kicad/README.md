# KiCad source — Rev A

This directory starts the CAD source for the PSN-Presepe Mega controller.

Files:
- `PSN-Presepe-Mega.kicad_pro`: KiCad project container.
- `PSN-Presepe-Mega.sch`: functional Eeschema source, intentionally kept in the legacy textual schematic format so it can be opened/migrated by KiCad without hand-forging KiCad's embedded symbol library structures.

## Why the schematic is not yet a fabricated-board source

The execution environment used to create this revision does not contain KiCad, therefore this commit deliberately does **not** claim ERC/DRC or format validation. Open `PSN-Presepe-Mega.sch` in a current KiCad release and save it to migrate it to `.kicad_sch`.

The electrical architecture is frozen in the companion documents in `hardware/pcb/`. Exact relay and terminal footprints, mains isolation rules, board outline and routing remain release blockers.

**Do not manufacture a 230 VAC PCB from this revision.**
