# PSN-Presepe PCB — schema elettrico Rev A

> Documento di progetto. **Non costituisce ancora uno schema approvato per costruzione a 230 V.** Serve come netlist funzionale per il successivo progetto KiCad.

## 1. Alimentazione

### J1 — 12 V DC
- J1.1 = +12V_IN
- J1.2 = GND

Catena prevista:
`J1 +12V -> F_MAIN -> protezione inversione -> +12V_BUS`

Da +12V_BUS derivano:
- +12V_RGB_CIELO
- +12V_RGB_TRAMONTO
- +12V_RGB_ALBA
- +12V_STELLE
- +12V_CASETTE
- +12V_RELAY

Arduino Mega resta alimentato separatamente via USB/5 V. GND Mega e GND 12 V sono comuni.

## 2. Arduino Mega — segnali

| Segnale | Mega |
|---|---:|
| CIELO_R/G/B | D2/D3/D4 |
| STELLE_DATA | D5 |
| BUZZER | D6 |
| TRAMONTO_R/G/B | D7/D11/D12 |
| CASETTE_DATA | D8 |
| OLED SDA/SCL | D20/D21 |
| START/NEXT/TEST | D22/D23/D24 |
| RELAY_01…16 | D25…D40 |
| ALBA_R/G/B | D44/D45/D46 |
| POT | A0 |

## 3. Canale MOSFET RGB — x9

Per ogni canale:
```
Mega PWM --- Rg 100R --- Gate Qx
                         |
                       Rpd 100k
                         |
                        GND

Qx Source -> GND
Qx Drain  -> ritorno LED R/G/B
LED +     -> +12V ramo
```

Qx: N-MOSFET logic-level, VDS >= 30 V, bassa RDS(on) specificata a VGS 4.5/5 V.
Footprint e codice definitivo da congelare prima del PCB.

Tre morsetti RGB:
- J_CIELO: +12V / R / G / B
- J_TRAMONTO: +12V / R / G / B
- J_ALBA: +12V / R / G / B

## 4. WS2811

### J_STELLE
- +12V_STELLE
- GND
- DATA, da D5 attraverso 390 ohm

### J_CASETTE
- +12V_CASETTE
- GND
- DATA, da D8 attraverso 390 ohm

Predisporre footprint TVS/ESD opzionale sulle due DATA.

## 5. Pulsanti

Tre morsetti a 2 poli:
- J_START: D22 / GND
- J_NEXT: D23 / GND
- J_TEST: D24 / GND

Il firmware usa INPUT_PULLUP; pulsanti esterni NO.

## 6. Potenziometro

RV1 = B10K lineare, montato sulla PCB:
- terminale 1 -> +5V_MEGA
- cursore -> A0
- terminale 3 -> GND

Aggiungere 100 nF A0-GND vicino all'ingresso ADC come footprint opzionale/DNP per filtraggio hardware, da validare sul prototipo.

## 7. OLED

J_OLED, 4 poli:
- +5V_MEGA
- GND
- SDA / D20
- SCL / D21

## 8. Buzzer

BZ1 piezo passivo, pilotato da D6. Se il buzzer scelto richiede corrente superiore a quella ammessa dal GPIO, usare piccolo driver NPN/NMOS. Rev A prevede footprint driver per non caricare direttamente il Mega.

## 9. Driver relè

U1, U2 = **ULN2803C**, 8 canali ciascuno.

Collegamenti U1:
- IN1…IN8 <- D25…D32
- OUT1…OUT8 -> bobina negativa K1…K8
- COM -> +12V_RELAY
- GND -> GND
- altra estremità bobine K1…K8 -> +12V_RELAY

U2:
- IN1…IN8 <- D33…D40
- OUT1…OUT8 -> bobina negativa K9…K16
- COM -> +12V_RELAY
- GND -> GND
- altra estremità bobine K9…K16 -> +12V_RELAY

Gli ULN2803C integrano i diodi clamp; COM va quindi collegato al positivo delle bobine.

Aggiungere:
- C_RELAY_BULK 470 uF / >=25 V vicino al banco relè
- 100 nF ceramico vicino a ciascun ULN2803C
- test point +12V_RELAY e GND

## 10. Relè K1…K16

Candidato: **Omron G5Q-1 DC12**, SPDT / 1 Form C.

Per ogni Kx:
- COIL+ -> +12V_RELAY
- COIL- -> ULN2803C OUTx
- COM -> morsetto JRx pin COM
- NO -> morsetto JRx pin NO
- NC -> morsetto JRx pin NC

Ogni JRx è un morsetto a 3 poli adatto a rete, con serigrafia:
`230V — COM | NO | NC`

Il firmware mantiene i relè OFF al boot secondo la logica esistente; il driver hardware deve inoltre evitare attivazioni spurie durante reset.

## 11. Dominio 230 V

La parte contatti di K1…K16 e J_R1…J_R16 è un dominio separato.

Regole preliminari:
- nessun GND, +5 V, +12 V o segnale sotto/attraverso la zona contatti;
- niente copper pour SELV nella barriera;
- mantenere una fascia di isolamento continua fra bobine/driver e piste dei contatti;
- slot di isolamento da valutare sotto/accanto ai relè;
- morsetti e footprint devono mantenere le distanze richieste dal progetto finale;
- routing 230 V esclusivamente nel settore dedicato.

Le clearance numeriche definitive NON vengono fissate in questo documento: vanno determinate prima del layout finale considerando IEC 60664-1 / standard applicabile, pollution degree, materiale PCB, categoria di sovratensione e costruzione dell'involucro.

## 12. Connettori/fusibili previsti

- F_MAIN: 12 V ingresso
- F_CIELO
- F_TRAMONTO
- F_ALBA
- F_STELLE
- F_CASETTE
- F_RELAY

Valori fusibili da definire dopo misura/stima delle correnti reali.

## 13. Distinta funzionale preliminare

- 1x carrier/header Arduino Mega 2560
- 9x N-MOSFET logic-level
- 9x 100 ohm gate resistor
- 9x 100 kohm gate pulldown
- 2x ULN2803C
- 16x Omron G5Q-1 DC12 (candidato)
- 16x morsetto 3 poli COM/NO/NC rete
- 3x morsetto 4 poli RGB
- 2x morsetto 3 poli WS2811
- 3x morsetto 2 poli pulsanti
- 1x morsetto 4 poli OLED
- 1x B10K PCB
- 1x buzzer + driver
- fusibili/protezioni 12 V
- condensatori bulk/decoupling
- test point principali

## 14. Verifiche prima del passaggio PCB

- verificare corrente bobina G5Q-1 DC12 e dissipazione contemporanea di 16 relè;
- verificare disponibilità e footprint esatto G5Q-1 DC12;
- scegliere morsetti rete con datasheet e footprint;
- scegliere MOSFET e morsetti 12 V;
- definire dimensioni PCB;
- decidere orientamento Mega (USB accessibile dal bordo);
- ERC completo;
- revisione manuale della separazione rete/SELV.
