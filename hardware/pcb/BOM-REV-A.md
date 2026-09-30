# PSN-Presepe PCB — componenti congelati Rev A

## Componenti principali

| Ref | Q.tà | Componente | Scelta Rev A | Footprint previsto |
|---|---:|---|---|---|
| MCU1 | 1 | Arduino Mega 2560 | modulo originale innestabile | header Mega shield |
| Q1-Q9 | 9 | N-MOSFET RGB | IRLZ44N, TO-220 | TO-220-3 vertical |
| U1-U2 | 2 | driver relè | TI ULN2803C | SOIC-20 wide |
| K1-K16 | 16 | relè SPDT 12 V | Omron G5Q-1 DC12, candidato da verificare contro CAD ufficiale | custom/datasheet |
| JR1-JR16 | 16 | morsetto COM/NO/NC | Phoenix Contact MKDS 1,5/3-5,08 (1715734) | 1x03 P5.08 mm, drill 1.3 mm |
| JC/JT/JA | 3 | morsetto RGB | famiglia Phoenix 5.08 mm, 4 poli | 1x04 P5.08 mm |
| JS/JK | 2 | morsetto WS2811 | famiglia Phoenix 5.08 mm, 3 poli | 1x03 P5.08 mm |
| JBTN1-3 | 3 | morsetto pulsanti | 5.08 mm, 2 poli | 1x02 P5.08 mm |
| JOLED | 1 | OLED | morsetto/header 4 poli | 1x04 |
| RV1 | 1 | B10K | potenziometro THT pannello/PCB | da scegliere meccanicamente |
| BZ1 | 1 | piezo passivo | THT | da scegliere |
| F* | 7 | fusibili 12 V | portafusibile THT | da scegliere |

## Passivi

- R_GATE1-9 = 100 ohm
- R_PULL1-9 = 100 kohm
- R_DATA_STELLE = 390 ohm
- R_DATA_CASETTE = 390 ohm
- C_U1/C_U2 = 100 nF
- C_RELAY_BULK = 470 uF / 25 V minimo
- C_POT = 100 nF DNP iniziale

## Note di scelta

### IRLZ44N
Scelto per prototipo Rev A perché through-hole, robusto e con RDS(on) specificata dal costruttore anche a VGS=4 V/5 V. Per le correnti previste dalle strisce PSN offre ampio margine. Prima della produzione verificare disponibilità del codice esatto e sorgente affidabile.

### ULN2803C
Due array da 8 canali pilotano le 16 bobine. COM dei clamp a +12V_RELAY. La Rev A usa package SOIC-20; è possibile passare a un equivalente THT solo se si desidera assemblaggio completamente manuale.

### Morsetti 230 V
Phoenix Contact MKDS 1,5/3-5,08, codice 1715734:
- 3 poli indipendenti;
- pitch 5.08 mm;
- 17.5 A nominali;
- 250 V (III/3), 400 V (III/2);
- foro PCB indicato 1.3 mm.

### Relè
G5Q-1 DC12 resta candidato. Il footprint non verrà disegnato per supposizione: deve essere derivato dal disegno meccanico ufficiale della variante esatta.

## Filosofia assemblaggio

Rev A privilegia componenti THT nei blocchi di potenza e connettori, per rendere riparazioni e sostituzioni semplici. I due ULN2803C possono essere SMD perché sono componenti standard e non soggetti a usura meccanica.
