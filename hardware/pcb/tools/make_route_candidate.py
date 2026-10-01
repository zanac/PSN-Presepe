#!/usr/bin/env python3
"""Temporary DRC candidate: replace K11/net46 and add K14/net49 as a pair."""
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text(encoding="utf-8")
baseline_segments=s.count("(segment ")
assert baseline_segments >= 93
assert not any("(net 49)" in ln for ln in s.splitlines() if "(segment " in ln)

# Remove the validated K11 route (net46) only in this temporary candidate.
lines=s.splitlines()
lines=[ln for ln in lines if not (("(segment " in ln or "(via " in ln) and "(net 46)" in ln)]
s="\n".join(lines)+"\n"

# K11 is moved to an outer F.Cu corridor; this frees its former B.Cu x=143.5 lane.
# K14 then uses that freed B.Cu lane from U2.13.
parts=[
# replacement K11/net46
'  (segment (start 145.16 97.08) (end 140.0 99.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 140.0 99.0) (end 140.0 144.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 140.0 144.0) (end 193.62 144.0) (width 0.3) (layer "F.Cu") (net 46))',
'  (segment (start 193.62 144.0) (end 193.62 115.0) (width 0.3) (layer "F.Cu") (net 46))',
# new K14/net49 on freed B.Cu corridor
'  (segment (start 145.16 104.70) (end 143.5 106.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 143.5 106.0) (end 143.5 142.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 143.5 142.0) (end 247.62 142.0) (width 0.3) (layer "B.Cu") (net 49))',
'  (segment (start 247.62 142.0) (end 247.62 115.0) (width 0.3) (layer "B.Cu") (net 49))',
]
edge=s.find("  (gr_rect "); assert edge>0
s=s[:edge]+"\n".join(parts)+"\n"+s[edge:]
dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s,encoding="utf-8")
print("Replaced K11/net46 and added K14/net49 candidate")
