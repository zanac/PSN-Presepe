# PSN-Presepe PCB — specifica Rev A

> Stato: progettazione, NON pronta per produzione. La PCB termina ai contatti puliti COM/NO/NC dei relè; l'eventuale cablaggio 230 V è esterno alla scheda.

## Architettura approvata
- Arduino Mega 2560 innestato direttamente come shield/carrier.
- Unico ingresso PCB: +12V / GND.
- Il 12 V alimenta carichi, bobine relè e il Mega attraverso il suo ingresso VIN/percorso di alimentazione previsto; non viene iniettato sul pin 5V.
- Il +5V per OLED, B10K e logica proviene dal Mega.
- 9 MOSFET onboard per CIELO, TRAMONTO e ALBA.
- 16 relè SPDT onboard.
- B10K e buzzer onboard.

## Pin firmware
D2/D3/D4 CIELO; D5 STELLE; D6 buzzer; D7/D11/D12 TRAMONTO; D8 CASETTE; D20/D21 OLED; D22/D23/D24 START/AVANTI/TEST; D25..D40 relè 1..16; D44/D45/D46 ALBA; A0 B10K.

## Morsetti esterni approvati
- J1 ALIMENTAZIONE: +12V / GND
- J_CIELO: +12V / R / G / B
- J_TRAMONTO: +12V / R / G / B
- J_ALBA: +12V / R / G / B
- J_STELLE: +12V / GND / DATA D5
- J_CASETTE: +12V / GND / DATA D8
- J_START: D22 / GND
- J_NEXT: D23 / GND
- J_TEST: D24 / GND
- J_OLED: +5V / GND / SDA D20 / SCL D21
- JR1..JR16: COM / NO / NC

STELLE e CASETTE non hanno resistenze, buffer o altri componenti sul DATA: il segnale va direttamente dal pin Mega al morsetto.

## Relè e rete
La PCB non distribuisce fase o neutro. Ogni relè termina esclusivamente sul proprio morsetto COM/NO/NC indipendente. I contatti e i morsetti sono comunque dimensionati e disposti considerando che l'utilizzatore potrà collegarvi esternamente 230 VAC; resta quindi necessaria la separazione fisica fra contatti e SELV.

## RGB
Ogni canale usa un N-MOSFET logic-level low-side con gate resistor e pulldown. Le tre strisce sono 12 V a positivo comune.

## Vincoli prima dei Gerber
Footprint esatto relè e morsetti, correnti reali 12 V, protezione ingresso, dimensioni PCB, ERC, regole isolamento, DRC e ispezione Gerber devono essere completati e verificati prima della produzione.
