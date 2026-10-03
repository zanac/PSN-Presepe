#!/usr/bin/env python3
import sys
import uuid
from pathlib import Path
import pcbnew

board = pcbnew.LoadBoard(sys.argv[1])
out = Path(sys.argv[2])

nets = sorted(
    {p.GetNetname() for fp in board.GetFootprints() for p in fp.Pads() if p.GetNetname()}
    | {t.GetNetname() for t in board.GetTracks() if t.GetNetname()}
)

def uid():
    return str(uuid.uuid4())

root = uid()
lines = [
    "(kicad_sch",
    "  (version 20250114)",
    '  (generator "eeschema")',
    '  (generator_version "10.0")',
    f"  (uuid {root})",
    '  (paper "A3")',
    "  (lib_symbols)",
]

y = 15.24
for i, name in enumerate(nets):
    x = 15.24 + (i // 45) * 70
    yy = y + (i % 45) * 5.08
    safe = name.replace('"', "'")
    lines += [
        f'  (text "{safe}" (exclude_from_sim no) (at {x:.2f} {yy:.2f} 0)',
        "    (effects (font (size 1.27 1.27)) (justify left bottom))",
        f"    (uuid {uid()}))",
    ]

lines += [
    '  (sheet_instances (path "/" (page "1")))',
    ")",
]

out.write_text("\n".join(lines) + "\n")
print("REV_B_SCHEMATIC_GENERATED nets=", len(nets), out)
if len(nets) < 50:
    raise SystemExit("Unexpectedly small PCB net inventory")
