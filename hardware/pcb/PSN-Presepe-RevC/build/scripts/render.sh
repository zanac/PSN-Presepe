#!/bin/sh
# render.sh <board.kicad_pcb> <out.png> [layers]
L=${3:-F.Cu,B.Cu,F.SilkS,Edge.Cuts,F.CrtYd}
kicad-cli pcb export svg --exclude-drawing-sheet --page-size-mode 2 -l "$L" -o /tmp/_r.svg "$1" >/dev/null && rsvg-convert -b white -w ${4:-2400} /tmp/_r.svg -o "$2"
