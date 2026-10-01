#!/usr/bin/env python3
"""Pass-through candidate used to validate the newly promoted routing baseline."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
assert s.count("(segment ") == 74, "Expected buttons + OLED + A0 + 9 local gate nodes"
dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s,encoding="utf-8")
print("Baseline-only candidate: no additional routing")
