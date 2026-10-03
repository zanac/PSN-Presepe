#!/usr/bin/env python3
from pathlib import Path
import re,sys
p=Path(sys.argv[1]); s=p.read_text()
names=set(re.findall(r'\(net\s+"?([^"\s()]+)"?',s))
groups=[
 ("HIGH_CURRENT_12V",lambda n:n in {"+12V","GND"},3000),
 ("RGB_LOAD",lambda n:n.endswith("_NEG"),1500),
 ("RELAY_CONTACT",lambda n:re.fullmatch(r"R[0-9]+_(COM|NO|NC)",n) is not None,2000),
 ("SELV_POWER",lambda n:n=="+5V_MEGA",800)]
rules=[]
for label,pred,width in groups:
 ns=sorted(n for n in names if pred(n))
 if not ns: raise SystemExit(f"{label}: no matching nets in DSN")
 quoted=" ".join(f'"{n}"' for n in ns)
 rules.append(f'    (class "{label}" {quoted}\n      (rule (width {width}))\n    )')
 print(label,"width",width,"nets",len(ns))
idx=s.rfind("(network")
if idx<0: raise SystemExit("network section not found")
depth=0; end=None
for i in range(idx,len(s)):
 if s[i]=="(": depth+=1
 elif s[i]==")":
  depth-=1
  if depth==0: end=i; break
if end is None: raise SystemExit("unterminated network")
p.write_text(s[:end]+"\n"+"\n".join(rules)+"\n"+s[end:])
print("DSN_RULE_PATCH_PASS")
