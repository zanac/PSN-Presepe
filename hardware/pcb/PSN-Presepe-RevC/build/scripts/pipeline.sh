#!/bin/sh
# Full Rev C build: place -> pre-route MAINS + power trunks -> autoroute -> import -> DRC
# Usage: build/pipeline.sh <out_dir> [freerouting.jar] [java]
set -e
OUT=${1:-out}; FR=${2:-freerouting-2.2.4.jar}; JAVA=${3:-java}
B=$(dirname "$0"); N=PSN-Presepe-Mega-RevC
mkdir -p "$OUT"
python3 "$B/build_board.py" "$OUT"
for n in $N placed mains keep routed; do python3 "$B/make_rules.py" "$OUT" $n >/dev/null; done
cp "$OUT/$N.kicad_pcb" "$OUT/placed.kicad_pcb"
python3 "$B/route_mains.py" "$OUT/placed.kicad_pcb" "$OUT/mains.kicad_pcb" "$OUT/keep.kicad_pcb"
python3 -c "import pcbnew,sys; b=pcbnew.LoadBoard(sys.argv[1]); assert pcbnew.ExportSpecctraDSN(b,sys.argv[2])" "$OUT/keep.kicad_pcb" "$OUT/keep.dsn"
if [ -n "$SES_IN" ]; then   # reproduce the released routing without re-running the autorouter
  cp "$SES_IN" "$OUT/keep.ses"
else
  "$JAVA" -jar "$FR" --gui.enabled=false --usage_and_diagnostic_data.disable_analytics=true \
     -de "$OUT/keep.dsn" -do "$OUT/keep.ses" -mp ${PASSES:-100} > "$OUT/freerouting.log" 2>&1
fi
grep "Auto-router session completed" "$OUT/freerouting.log" 2>/dev/null || true
python3 "$B/import_ses.py" "$OUT/mains.kicad_pcb" "$OUT/keep.ses" "$OUT/routed.kicad_pcb"
python3 "$B/drc.py" "$OUT/routed.kicad_pcb" "$OUT/routed-drc.txt"
python3 "$B/make_rules.py" "$OUT" final >/dev/null
python3 "$B/complete_routes.py" "$OUT/routed.kicad_pcb" "$OUT/routed-drc.txt" "$OUT/final.kicad_pcb"
python3 "$B/drc.py" "$OUT/final.kicad_pcb" "$OUT/final-drc.txt"
grep -E "Found" "$OUT/final-drc.txt"
