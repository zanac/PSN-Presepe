# PSN-Presepe PCB — specifica Rev A

> Stato: **progettazione, NON pronta per produzione**. La sezione 230 V richiede verifica finale di schema, footprint, distanze di isolamento, DRC e revisione indipendente prima della fabbricazione.

## Obiettivo

Scheda unica tipo carrier/shield per Arduino Mega 2560, coerente con il firmware del branch `dev`, con morsetti per tutti i carichi e comandi del presepe.

## Interfaccia Arduino Mega 2560

- D2 / D3 / D4 — CIELO RGB R/G/B
- D5 — DATA STELLE WS2811
- D6 — buzzer
- D7 / D11 / D12 — TRAMONTO RGB R/G/B
- D8 — DATA CASETTE WS2811
- D22 / D23 / D24 — START/STOP, AVANTI, TEST
- D25…D40 — relè 1…16
- D44 / D45 / D46 — ALBA RGB R/G/B
- D20 / D21 — OLED SDA/SCL
- A0 — potenziometro B10K

## Alimentazione e domini

### SELV / bassa tensione
- ingresso 12 V DC per carichi, bobine relè e WS2811;
- GND 12 V comune con GND Arduino per PWM e DATA;
- Arduino Mega alimentato separatamente a 5 V/USB, come nel progetto attuale;
- nessun collegamento galvanico intenzionale tra rete 230 V e SELV eccetto l'isolamento interno dei relè.

### Rete
La zona contatti relè è da considerare **230 V AC**. Deve essere fisicamente segregata dalla zona SELV, con keep-out di rame e distanze di isolamento definite in fase di layout in base allo standard/applicazione finale. Prevedere slot di isolamento dove utili. Nessuna pista SELV deve attraversare la zona contatti.

## 9 canali MOSFET RGB

Tre gruppi indipendenti:
- CIELO: R/G/B
- TRAMONTO: R/G/B
- ALBA: R/G/B

Requisiti:
- low-side switching per strisce analogiche 12 V a positivo comune;
- MOSFET N-channel logic-level compatibili con comando 5 V del Mega;
- gate resistor e gate pulldown per ogni canale;
- morsetto a 4 poli per ogni striscia: +12V, R, G, B;
- piste di potenza dimensionate dopo definizione della corrente massima per striscia;
- PWM firmware 8 bit + gamma, senza dithering.

## WS2811

Due morsetti a 3 poli:
- STELLE: +12V / GND / DATA (D5)
- CASETTE: +12V / GND / DATA (D8)

Per ciascuna DATA:
- resistenza serie 330–470 ohm vicino al Mega/driver;
- predisposizione opzionale per protezione ESD sul connettore;
- GND comune.

## Comandi e interfaccia

- 3 morsetti a 2 poli: START/STOP, AVANTI, TEST; contatto NO verso GND, firmware INPUT_PULLUP.
- potenziometro lineare B10K montato direttamente sulla PCB, collegato 5V/A0/GND.
- morsetto OLED 4 poli: 5V / GND / SDA(D20) / SCL(D21).
- buzzer piezo passivo onboard oppure footprint + connettore opzionale.

## 16 relè

Architettura:
- 16 relè SPDT (1 Form C), bobina 12 V DC;
- ogni uscita espone COM / NO / NC su morsetto 3 poli;
- pilotaggio delle bobine tramite driver low-side dedicati, non direttamente dai pin Mega;
- diodo flyback per ogni bobina (o array driver con clamp adeguato);
- stato di default OFF durante reset/boot.

### Candidato Rev A
**Omron G5Q-1 DC12**, famiglia G5Q SPDT, attualmente in produzione. La famiglia prevede bobina 12 V e contatti per rete fino a 250 VAC; la portata effettiva dipende da NO/NC, tipo di carico e variante. Il progetto non assume 10 A su tutti i contatti: i carichi PSN previsti sono di pochi watt.

Il codice ordine/footprint definitivo va verificato sul datasheet corrente prima del layout finale.

## Separazione fisica proposta

Layout a due macro-zone:

```
+-------------------------------------------------------------+
| SELV 5/12 V                         |  ZONA 230 V            |
|                                     |                        |
| Mega 2560                           | [R1] COM NO NC         |
| OLED / tasti / B10K                 | [R2] COM NO NC         |
| WS2811                              | ...                    |
| 9 MOSFET + morsetti RGB             | [R16] COM NO NC        |
| driver bobine relè -> bobine        |                        |
|                                     | morsetti rete          |
+------------------ barriera isolamento -----------------------+
```

I pin bobina dei relè restano lato SELV; i pin COM/NO/NC e le relative piste/morsetti restano lato rete. Nessun piano di massa sotto la barriera o nella zona di isolamento.

## Protezioni e connettori

Da prevedere nella Rev B:
- ingresso 12 V con protezione inversione polarità;
- fusibile principale 12 V e/o fusibili per rami CIELO/ALBA/TRAMONTO/STELLE/CASETTE;
- TVS 12 V se utile;
- morsetti 12 V dimensionati per corrente reale;
- morsetti lato rete certificati per almeno 250 VAC e passo adeguato;
- serigrafia molto evidente: **230 VAC**, COM/NO/NC, separazione SELV;
- fori di fissaggio e distanza meccanica dal Mega/USB/connettore alimentazione.

## Vincoli prima dei Gerber

1. Congelare codice esatto dei relè e relativo footprint.
2. Congelare modello dei morsetti 230 V.
3. Definire corrente massima reale delle tre strisce RGB e dei due rami WS2811.
4. Scegliere MOSFET definitivi e verificarne dissipazione.
5. Definire dimensioni massime PCB e posizione desiderata dei morsetti.
6. Eseguire ERC dello schematico.
7. Applicare regole di clearance/creepage coerenti con 230 V e ambiente d'uso.
8. Eseguire DRC completo.
9. Ispezione visiva Gerber + drill.
10. Revisione indipendente della sezione 230 V prima della fabbricazione.

## Nota firmware

La PCB deve adattarsi al pinout del firmware esistente; la Rev A non richiede modifiche alla logica scenografica.
