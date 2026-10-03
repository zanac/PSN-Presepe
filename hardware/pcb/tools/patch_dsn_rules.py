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
targets={n for _,pred,_ in groups for n in names if pred(n)}

# Parse every existing (class ...) S-expression and remove production nets
# from it. This avoids duplicate membership (e.g. kicad_default + HIGH_CURRENT).
def sexpr_end(text,start):
    depth=0; quote=False; esc=False
    for i in range(start,len(text)):
        c=text[i]
        if quote:
            if esc: esc=False
            elif c=="\\": esc=True
            elif c=='"': quote=False
        else:
            if c=='"': quote=True
            elif c=="(": depth+=1
            elif c==")":
                depth-=1
                if depth==0: return i+1
    raise SystemExit("unterminated s-expression")

pos=0; out=[]
while True:
    st=s.find("(class ",pos)
    if st<0: out.append(s[pos:]); break
    en=sexpr_end(s,st); block=s[st:en]
    # Only rewrite pre-existing classes; production classes do not exist yet.
    header_end=block.find("\n")
    header=block[:header_end if header_end>=0 else len(block)]
    for n in sorted(targets,key=len,reverse=True):
        header=re.sub(r'(?<![^\s"])("?'+re.escape(n)+r'"?)(?=\s|$)',"",header)
    header=re.sub(r"[ \t]+"," ",header).replace(" )",")")
    block=header+(block[header_end:] if header_end>=0 else "")
    out.append(s[pos:st]); out.append(block); pos=en
s="".join(out)

rules=[]
for label,pred,width in groups:
    ns=sorted(n for n in names if pred(n))
    if not ns: raise SystemExit(f"{label}: no matching nets in DSN")
    quoted=" ".join(f'"{n}"' for n in ns)
    rules.append(f'    (class "{label}" {quoted}\n      (rule (width {width}))\n    )')
    print(label,"width",width,"nets",len(ns))

idx=s.rfind("(network")
if idx<0: raise SystemExit("network section not found")
end=sexpr_end(s,idx)-1
s=s[:end]+"\n"+"\n".join(rules)+"\n"+s[end:]

# Hard validation: every production net must occur in exactly one class header.
class_headers=re.findall(r'^\s*\(class\s+[^\n]+',s,re.M)
for n in sorted(targets):
    hits=[h for h in class_headers if re.search(r'(?<![^\s"])("?'+re.escape(n)+r'"?)(?=\s|$)',h)]
    if len(hits)!=1:
        raise SystemExit(f"DSN_CLASS_MEMBERSHIP_FAIL {n} count={len(hits)} headers={hits}")
print("DSN_CLASS_MEMBERSHIP_PASS nets",len(targets))
# Inject the deliberate 3 mm GND spine directly into Specctra wiring.
fixed=[
 ((52000,176000),(122000,176000),"B.Cu"),
 ((122000,176000),(122000,128000),"B.Cu"),
]
widx=s.rfind("(wiring")
if widx < 0:
    dend=len(s.rstrip())-1
    wiring="  (wiring\\n"
    for a,b,layer in fixed:
        wiring+=f'    (wire (path {layer} 3000 {a[0]} {a[1]} {b[0]} {b[1]}) (net "GND") (type fix))\\n'
    wiring+="  )\\n"
    s=s[:dend]+wiring+s[dend:]
else:
    wend=sexpr_end(s,widx)-1
    wires=""
    for a,b,layer in fixed:
        wires+=f'    (wire (path {layer} 3000 {a[0]} {a[1]} {b[0]} {b[1]}) (net "GND") (type fix))\\n'
    s=s[:wend]+wires+s[wend:]
print("DSN_FIXED_GND_SPINE_PASS segments",len(fixed),"width",3000)

p.write_text(s)
print("DSN_RULE_PATCH_PASS")
