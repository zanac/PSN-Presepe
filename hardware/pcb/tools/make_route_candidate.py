#!/usr/bin/env python3
"""Pass-through candidate: validate promoted routing baseline."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") == 77, "Expected 77-segment baseline after K1 coil promotion"
dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(s,encoding="utf-8")
print("Baseline-only candidate: no additional routing")
