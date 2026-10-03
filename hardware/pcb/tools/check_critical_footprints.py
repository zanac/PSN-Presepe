from pathlib import Path
import re, sys

PCB = Path(sys.argv[1] if len(sys.argv) > 1 else "hardware/pcb/kicad/PSN-Presepe-Mega.kicad_pcb")
s = PCB.read_text()

def sexpr_blocks(text, token):
    out=[]; pos=0
    while True:
        st=text.find(token,pos)
        if st<0: break
        depth=0; quote=False; esc=False; end=None
        for i in range(st,len(text)):
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
                    if depth==0: end=i+1; break
        if end is None: raise SystemExit("Malformed PCB")
        out.append(text[st:end]); pos=end
    return out

fps=sexpr_blocks(s,'(footprint "')
refs={}
for b in fps:
    m=re.search(r'\(property "Reference" "([^"]+)"',b)
    if m: refs[m.group(1)]=b

def pad_at(block,n):
    m=re.search(r'\(pad "'+re.escape(str(n))+r'"[\s\S]*?\(at\s+([-0-9.]+)\s+([-0-9.]+)',block)
    if not m: raise SystemExit(f"missing pad {n}")
    return tuple(map(float,m.groups()))

def pad_net(block,n):
    m=re.search(r'\(pad "'+re.escape(str(n))+r'"[\s\S]*?\(net(?:\s+\d+)?\s+"([^"]+)"\)',block)
    if not m: raise SystemExit(f"missing net pad {n}")
    return m.group(1)

for ref in ("U1","U2"):
    b=refs[ref]
    if "ULN2803C_DIP18" not in b: raise SystemExit(f"{ref}: wrong footprint")
    xs={round(pad_at(b,n)[0],2) for n in range(1,19)}
    if xs != {0.0,7.62}: raise SystemExit(f"{ref}: DIP18 row spacing wrong: x={sorted(xs)}")
    if pad_net(b,9)!="GND" or pad_net(b,10)!="+12V": raise SystemExit(f"{ref}: ULN COM/GND mapping wrong")

for i in range(1,17):
    ref=f"K{i}"; b=refs[ref]
    if "Relay_Omron_G5Q-1_SPDT" not in b: raise SystemExit(f"{ref}: wrong footprint")
    expected={1:(0.0,0.0),2:(10.16,0.0),3:(17.78,0.0),4:(15.24,-7.62),5:(0.0,-7.62)}
    for n,xy in expected.items():
        got=tuple(round(v,2) for v in pad_at(b,n))
        if got!=xy: raise SystemExit(f"{ref} pad {n}: {got} != {xy}")
    if pad_net(b,2)!=f"R{i}_COM" or pad_net(b,3)!=f"R{i}_NO" or pad_net(b,4)!=f"R{i}_NC":
        raise SystemExit(f"{ref}: COM/NO/NC mapping wrong: {pad_net(b,2)}, {pad_net(b,3)}, {pad_net(b,4)}")
    if pad_net(b,1)!="+12V" or pad_net(b,5)!=f"RELAY{i}_COIL_LOW":
        raise SystemExit(f"{ref}: coil mapping wrong")

print("CRITICAL_FOOTPRINT_GATE_PASS relays=16 uln2803=2 relay_pad3=NO relay_pad4=NC dip18_rows=7.62mm")
