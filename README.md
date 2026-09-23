# PSN-Presepe

Controller basato su Arduino Mega 2560 per la gestione modulare di un presepe a 12 V.

**Italiano** | [English](README_EN.md)

## Mockup della centralina

![Mockup centralina PSN-Presepe](docs/a_high_resolution_infographic_wiring_diagram_photo.png)

> Mockup concettuale della disposizione della centralina. Per i collegamenti elettrici fare riferimento agli schemi vettoriali presenti nella cartella `docs/`.

## Schema elettrico

![Schema elettrico PSN-Presepe Fase 1 + Fase 2](docs/schema-fase1-fase2-pulito.png)

> Questo è lo **schema di riferimento aggiornato** per il cablaggio. La striscia RGB 12 V è a positivo comune: il +12 V è diretto, mentre R, G e B vengono commutati sul lato negativo dai MOSFET.

## Mappatura hardware attuale

I pin di Arduino **non alimentano direttamente i carichi a 12 V**. Ogni uscita del Mega pilota l'ingresso `PWM` del relativo canale MOSFET. I normali carichi a due fili possono utilizzare la coppia `OUT+` / `OUT-`; la striscia RGB a positivo comune viene invece collegata come indicato qui sotto.

### MOSFET #1 — Cielo RGB

| Arduino Mega | Ingresso MOSFET | Uscita MOSFET | Carico 12 V | Controllo |
|---:|---|---|---|---|
| D2 | PWM1 | OUT1- | Striscia RGB — ritorno R | PWM / dimmerabile |
| D3 | PWM2 | OUT2- | Striscia RGB — ritorno G | PWM / dimmerabile |
| D4 | PWM3 | OUT3- | Striscia RGB — ritorno B | PWM / dimmerabile |
| — | PWM4 | OUT4+ / OUT4- | **Libero** | — |

La striscia RGB è un carico **12 V a positivo comune (anodo comune)**. Il suo unico filo `+12V` viene collegato direttamente alla distribuzione +12 V protetta/WAGO e rimane sempre alimentato. I tre canali MOSFET commutano invece i ritorni R/G/B sul lato negativo:

```text
+12V alimentatore ──► fusibile/distribuzione ──► +12V comune RGB

RGB R ─────────────────────────────────────────► OUT1-
RGB G ─────────────────────────────────────────► OUT2-
RGB B ─────────────────────────────────────────► OUT3-

Mega D2 ───────────────────────────────────────► PWM1  (Rosso)
Mega D3 ───────────────────────────────────────► PWM2  (Verde)
Mega D4 ───────────────────────────────────────► PWM3  (Blu)

+12V alimentatore ─────────────────────────────► DC+ MOSFET
0V alimentatore ───────────────────────────────► DC- MOSFET
```

La striscia RGB **non deve essere cablata come tre carichi indipendenti a due fili**. In questa configurazione `OUT1+`, `OUT2+` e `OUT3+` non sono necessari per la striscia RGB.

### Stelle WS2811 indirizzabili

Le stelle sono ora una stringa **WS2811 12 V da 50 pixel individualmente indirizzabili**. Non passano dal MOSFET: D5 è il segnale DATA.

```text
+12V alimentatore ──► fusibile/distribuzione ──► WS2811 +12V
0V alimentatore ───────────────────────────────► WS2811 GND
Arduino GND ───────────────────────────────────► stesso 0V comune
Mega D5 ── resistenza 330–470 Ω ──────────────► WS2811 DATA / DIN
```

Con le WS2811 il **GND Arduino deve essere comune allo 0 V dell'alimentatore 12 V**, perché il segnale DATA necessita dello stesso riferimento elettrico. Il Mega continua comunque a essere alimentato a 5 V via USB: il +12 V non deve mai essere collegato ai pin 5V o I/O di Arduino.

Il firmware può comandare ogni stella separatamente, con luminosità e colore differenti, facendo comparire progressivamente stelle casuali durante il crepuscolo e spegnendole durante l'alba. Il canale 4 del MOSFET #1 rimane libero.

### MOSFET #2 — Scenografia e movimenti

| Arduino Mega | Ingresso MOSFET | Uscita MOSFET | Carico 12 V | Controllo previsto |
|---:|---|---|---|---|
| D6 | PWM1 | OUT1+ / OUT1- | Luci case | ON/OFF / PWM |
| D7 | PWM2 | OUT2+ / OUT2- | Pompa | ON/OFF |
| D8 | PWM3 | OUT3+ / OUT3- | Mulino | ON/OFF |
| D9 | PWM4 | OUT4+ / OUT4- | Grotta / lampioni | ON/OFF / PWM |

D6-D9 sono attualmente riservati alla Fase 2; il firmware attuale implementa la Fase 1 dedicata a cielo e stelle.

### Comandi

| Arduino Mega | Dispositivo | Collegamento |
|---:|---|---|
| D22 | Pulsante START/STOP | D22 ↔ pulsante ↔ GND logica |
| D23 | Pulsante AVANTI | D23 ↔ pulsante ↔ GND logica |
| D24 | Pulsante TEST | D24 ↔ pulsante ↔ GND logica |
| A0 | Potenziometro B10K velocità ciclo | 5V ↔ esterno, A0 ↔ cursore, GND ↔ esterno |

I pulsanti utilizzano `INPUT_PULLUP`, quindi non richiedono una resistenza di pull-up esterna. Il GND logico di Arduino viene distribuito tramite WAGO agli ingressi `GND1...GND4` dei MOSFET e ai comandi.

## Firmware

Aprire:

`firmware/PSN-Presepe/PSN-Presepe.ino`

con Arduino IDE standard e selezionare **Arduino Mega or Mega 2560**.

Il firmware attuale implementa la Fase 1 (cielo RGB + stelle + comandi). D6-D9 sono riservati nel sorgente al secondo modulo MOSFET della Fase 2.

## GitHub Actions

Il workflow `.github/workflows/build.yml` può essere avviato manualmente dalla pagina GitHub Actions e compila il firmware per:

`arduino:avr:mega`

I file HEX/ELF compilati vengono pubblicati come artifact della GitHub Action.

## Simulazione

`simulation/diagram.json` contiene un modello iniziale per Wokwi. I LED virtuali rappresentano i canali MOSFET reali e permettono di verificare la logica senza collegare l'hardware a 12 V.

La CI Wokwi rimane per ora opzionale: la normale compilazione GitHub Actions non richiede token o servizi esterni.

## Nota elettrica

Con l'introduzione delle stelle WS2811, **Arduino GND e lo 0 V dell'alimentatore 12 V sono collegati in comune** per fornire il riferimento al segnale DATA. Il Mega resta alimentato separatamente a 5 V via USB. Prima del cablaggio definitivo verificare con il multimetro la continuità tra `DC+` e gli eventuali `OUT+` utilizzati. Per pompa e mulino devono inoltre essere verificati corrente nominale, corrente di spunto e protezione dei carichi induttivi.

---

By **Vanni Brutto**
