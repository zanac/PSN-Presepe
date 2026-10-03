# PSN-Presepe PCB — BOM Rev A

| Ref | Q.tà | Componente | Rev A |
|---|---:|---|---|
| MCU1 | 1 | Arduino Mega 2560 R3 | modulo innestabile come shield/carrier |
| Q1-Q9 | 9 | MOSFET N logic-level | IRLZ44N, TO-220 |
| U1-U2 | 2 | driver relè | ULN2803C, 8 canali |
| K1-K16 | 16 | relè SPDT bobina 12 V | Omron G5Q-1 DC12 |
| JR1-JR16 | 16 | morsetti relè | 3 poli COM/NO/NC, passo 5.08 mm, footprint candidato Phoenix MKDS 1,5/3-5,08 |
| J_CIELO | 1 | morsetto RGB | 4 poli 12V/R/G/B |
| J_TRAMONTO | 1 | morsetto RGB | 4 poli 12V/R/G/B |
| J_ALBA | 1 | morsetto RGB | 4 poli 12V/R/G/B |
| J_STELLE | 1 | morsetto WS2811 | 3 poli 12V/GND/DATA |
| J_CASETTE | 1 | morsetto WS2811 | 3 poli 12V/GND/DATA |
| J_START | 1 | morsetto pulsante | 2 poli START/GND |
| J_NEXT | 1 | morsetto pulsante | 2 poli AVANTI/GND |
| J_TEST | 1 | morsetto pulsante | 2 poli TEST/GND |
| J_OLED | 1 | morsetto OLED | 4 poli 5V/GND/SDA/SCL |
| J1 | 1 | alimentazione | 2 poli 12V/GND |
| RV1 | 1 | potenziometro | B10K onboard |
| BZ1 | 1 | buzzer | piezo passivo onboard |
| RG1-RG9 | 9 | resistenza gate | 100 ohm |
| RPD1-RPD9 | 9 | pulldown gate | 100 kohm |
| C1 | 1 | bulk alimentazione relè | 470 uF / 25 V |
| C2-C3 | 2 | decoupling locale | 100 nF |

## Note termiche
- lasciare spazio per piccoli dissipatori individuali sui 9 IRLZ44N;
- il tab TO-220 dell'IRLZ44N è collegato al drain: dissipatori metallici di canali diversi non devono toccarsi;
- mantenere C1 distante dalle principali sorgenti di calore;
- lasciare ventilazione attorno a U1/U2.

## Non presenti nella Rev A corrente
- nessuna resistenza DATA su STELLE/CASETTE;
- nessun buffer DATA;
- nessuna TVS;
- nessun bus fase/neutro 230 V;
- nessun fusibile/protezione ingresso è attualmente presente nel PCB: un'eventuale protezione aggiuntiva richiede una revisione esplicita.

L'unico ingresso di alimentazione PCB è 12 V. Il Mega viene alimentato attraverso VIN; non applicare 12 V al pin 5V.
