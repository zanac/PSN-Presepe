# PSN-Presepe PCB — layout meccanico Rev A

## Outline corrente
- **280 x 170 mm**
- FR-4 1.6 mm
- 2 layer

La scheda è stata volutamente ingrandita per privilegiare cablaggio, isolamento, dissipazione e accesso con cacciavite ai morsetti.

## Architettura
La PCB è una carrier/shield estesa per Arduino Mega 2560. Il Mega resta sostituibile; USB, jack e RESET devono rimanere accessibili.

### Zona SELV
Comprende Mega, B10K, buzzer, 9 MOSFET IRLZ44N, due ULN2803C, alimentazione 12 V e terminali bassa tensione.

I 9 MOSFET hanno una zona dedicata con spazio per piccoli dissipatori TO-220 e circolazione d'aria. I dissipatori non devono potersi toccare fra loro: il tab dell'IRLZ44N è elettricamente collegato al drain.

### Terminali bassa tensione
Sono sul perimetro e con ingresso filo rivolto verso l'esterno:
- J1: 12V / GND
- J_OLED: 5V / GND / SDA / SCL
- J_START: START / GND
- J_NEXT: AVANTI / GND
- J_TEST: TEST / GND
- J_CIELO: 12V / R / G / B
- J_TRAMONTO: 12V / R / G / B
- J_ALBA: 12V / R / G / B
- J_STELLE: 12V / GND / DATA
- J_CASETTE: 12V / GND / DATA

La serigrafia PCB riporta in piccolo queste funzioni vicino ai morsetti.

### Relè
16 Omron G5Q-1, due file da 8, con passo aumentato per facilitare collegamento fili e manutenzione.

Pinout verificato:
- 1, 5: bobina
- 3: COM
- 2: NC
- 4: NO

JR1..JR16 espongono ciascuno:
`COM | NO | NC`

Tutti i morsetti relè sono sul perimetro e devono avere ingresso filo rivolto verso l'esterno. La serigrafia riporta `R1: COM NO NC` ... `R16: COM NO NC`.

## Contatti potenzialmente a 230 VAC
La PCB **non distribuisce fase o neutro**. I contatti sono puliti e indipendenti, ma possono essere cablati esternamente a 230 VAC.

Per il routing finale:
- nessun piano GND SELV sotto la zona contatti;
- nessuna pista SELV deve passare fra i percorsi COM/NO/NC;
- creepage/clearance devono essere impostati nel DRC in funzione dei requisiti reali;
- eventuali slot d'isolamento si decidono nel CAD dopo DRC e ispezione meccanica.

## Stato routing
Il routing testuale preliminare è stato rimosso dopo un audit geometrico che ha rilevato incroci sullo stesso layer fra net diverse.

Il placement/netlist/serigrafia sono la base corrente. Il routing definitivo richiede KiCad e DRC reale; non va ricostruito alla cieca con segmenti testuali.

## Vincolo termico
Mantenere spazio per dissipatori sui 9 IRLZ44N, ventilazione attorno agli ULN2803 e distanza degli elettrolitici dalle principali sorgenti di calore.

## Produzione
Nessun Gerber di questa revisione è approvato finché non sono completati routing reale, ERC/DRC, controllo orientamento morsetti, verifica footprint/datasheet e ispezione Gerber.
