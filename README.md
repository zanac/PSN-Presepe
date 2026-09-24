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

### MOSFET #3 e #4 — RGB laterali alba/tramonto

Per rendere alba e tramonto più dinamici vengono aggiunte **due strisce RGB analogiche 12 V da 1 m**, indipendenti dalla striscia principale:

| Posizione | Effetto | Mega R/G/B | Modulo |
|---|---|---|---|
| Sinistra | Tramonto | D10 / D11 / D12 | MOSFET #3, CH1–CH3 |
| Destra | Alba | D44 / D45 / D46 | MOSFET #4, CH1–CH3 |

Ogni striscia ha il proprio +12 V comune collegato alla distribuzione protetta. I ritorni R/G/B vanno ai tre OUT- del relativo modulo MOSFET. Il quarto canale di ciascun modulo resta libero. **D13 rimane PWM libero.**

Nel firmware la striscia sinistra cresce e cala gradualmente durante il TRAMONTO, con tonalità calde rosso/arancio. La striscia destra esegue un andamento analogo durante l'ALBA, con una tonalità più chiara. La striscia RGB principale continua contemporaneamente la transizione generale del cielo: la sovrapposizione crea uno spostamento laterale della luce.

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

## Funzionamento scenografico

Il ciclo automatico coordina la **striscia RGB principale**, le **due strisce RGB laterali da 1 m** dedicate ad alba e tramonto e le **50 stelle WS2811 individualmente indirizzabili**.

1. **Giorno:** stelle spente; la striscia RGB crea l'illuminazione diurna.
2. **Tramonto:** stelle spente; la striscia principale passa progressivamente ai colori caldi mentre la striscia laterale sinistra entra e poi cala gradualmente, creando movimento e direzionalità nella luce.
3. **Crepuscolo:** le stelle iniziano a comparire **una alla volta in ordine casuale**, mentre il cielo RGB diventa progressivamente più scuro.
4. Ogni stella ha una **luminosità massima diversa**, per evitare un cielo uniforme e artificiale.
5. Circa il **18% delle stelle** presenta un leggerissimo **scintillio morbido**, senza lampeggi netti.
6. **Notte:** il cielo stellato è completo ma non uniforme; le stelle mantengono intensità differenti.
7. **Alba:** le stelle scompaiono progressivamente mentre la striscia principale torna verso il giorno e la striscia laterale destra entra e poi cala gradualmente, simulando una sorgente luminosa direzionale.
8. A ogni nuova notte viene generata una **disposizione differente** delle stelle e delle relative intensità.
9. Il colore delle stelle è impostato su **bianco caldo**, evitando un effetto RGB multicolore.

## Manuale di montaggio filo per filo

Questa sezione è il riferimento pratico per il cablaggio. **Non lavorare mai sul circuito con l'alimentatore 230 V collegato.** Il Mega è alimentato separatamente via USB 5 V. Il +12 V alimenta soltanto carichi e moduli di potenza. Lo **0 V 12 V e GND Arduino devono essere in comune** per i segnali PWM e per DATA WS2811.

### 1. Distribuzione alimentazione 12 V

Portare il +12 V dell'alimentatore a un portafusibili/distributore. Da questo partire con rami separati verso RGB principale, stelle WS2811, RGB tramonto, RGB alba e gli altri carichi. Portare lo 0 V a una morsettiera/WAGO comune.

| Da | A | Nota |
|---|---|---|
| PSU +12 V | ingresso portafusibili +12 V | cavo dimensionato per la corrente totale |
| PSU 0 V | WAGO/morsettiera 0 V comune | ritorno comune |
| WAGO 0 V | Mega GND | riferimento logico comune |
| WAGO 0 V | DC- MOSFET #1 | alimentazione modulo |
| WAGO 0 V | DC- MOSFET #2 | alimentazione modulo |
| WAGO 0 V | DC- MOSFET #3 | alimentazione modulo |
| WAGO 0 V | DC- MOSFET #4 | alimentazione modulo |
| +12 V protetto | DC+ MOSFET #1 | modulo RGB principale |
| +12 V protetto | DC+ MOSFET #2 | scenografia |
| +12 V protetto | DC+ MOSFET #3 | RGB sinistra/tramonto |
| +12 V protetto | DC+ MOSFET #4 | RGB destra/alba |

### 2. MOSFET #1 — RGB principale

| Filo | Da | A |
|---|---|---|
| 1 | Mega D2 | MOSFET #1 PWM1 |
| 2 | Mega GND | MOSFET #1 GND1 |
| 3 | Mega D3 | MOSFET #1 PWM2 |
| 4 | Mega GND | MOSFET #1 GND2 |
| 5 | Mega D4 | MOSFET #1 PWM3 |
| 6 | Mega GND | MOSFET #1 GND3 |
| 7 | +12 V protetto | RGB principale +12V |
| 8 | RGB principale R | MOSFET #1 OUT1- |
| 9 | RGB principale G | MOSFET #1 OUT2- |
| 10 | RGB principale B | MOSFET #1 OUT3- |

PWM4/GND4 e OUT4 restano liberi. Prima del cablaggio definitivo verificare sul modulo reale la continuità tra DC+ e OUT+.

### 3. Stelle WS2811

| Filo | Da | A |
|---|---|---|
| 11 | +12 V protetto | WS2811 +12V |
| 12 | WAGO 0 V comune | WS2811 GND |
| 13 | Mega D5 | resistenza 330–470 Ω |
| 14 | uscita resistenza | WS2811 DATA/DIN |

Rispettare la freccia/direzione DATA della stringa. La resistenza va preferibilmente vicino all'ingresso della prima WS2811.

### 4. MOSFET #3 — RGB sinistra / TRAMONTO

| Filo | Da | A |
|---|---|---|
| 15 | Mega D10 | MOSFET #3 PWM1 |
| 16 | Mega GND | MOSFET #3 GND1 |
| 17 | Mega D11 | MOSFET #3 PWM2 |
| 18 | Mega GND | MOSFET #3 GND2 |
| 19 | Mega D12 | MOSFET #3 PWM3 |
| 20 | Mega GND | MOSFET #3 GND3 |
| 21 | +12 V protetto | RGB sinistra +12V |
| 22 | RGB sinistra R | MOSFET #3 OUT1- |
| 23 | RGB sinistra G | MOSFET #3 OUT2- |
| 24 | RGB sinistra B | MOSFET #3 OUT3- |

PWM4/GND4 e OUT4 restano liberi.

### 5. MOSFET #4 — RGB destra / ALBA

| Filo | Da | A |
|---|---|---|
| 25 | Mega D44 | MOSFET #4 PWM1 |
| 26 | Mega GND | MOSFET #4 GND1 |
| 27 | Mega D45 | MOSFET #4 PWM2 |
| 28 | Mega GND | MOSFET #4 GND2 |
| 29 | Mega D46 | MOSFET #4 PWM3 |
| 30 | Mega GND | MOSFET #4 GND3 |
| 31 | +12 V protetto | RGB destra +12V |
| 32 | RGB destra R | MOSFET #4 OUT1- |
| 33 | RGB destra G | MOSFET #4 OUT2- |
| 34 | RGB destra B | MOSFET #4 OUT3- |

PWM4/GND4 e OUT4 restano liberi. D13 rimane disponibile come uscita PWM di riserva.

### 6. MOSFET #2 — scenografia

Questi collegamenti sono predisposti; prima di collegare fisicamente pompa e mulino verificare tensione, corrente di regime/spunto e protezione dei carichi induttivi.

| Filo | Da | A | Carico |
|---|---|---|---|
| 35 | Mega D6 | MOSFET #2 PWM1 | luci case |
| 36 | Mega GND | MOSFET #2 GND1 | riferimento |
| 37 | Mega D7 | MOSFET #2 PWM2 | pompa |
| 38 | Mega GND | MOSFET #2 GND2 | riferimento |
| 39 | Mega D8 | MOSFET #2 PWM3 | mulino |
| 40 | Mega GND | MOSFET #2 GND3 | riferimento |
| 41 | Mega D9 | MOSFET #2 PWM4 | grotta/lampioni |
| 42 | Mega GND | MOSFET #2 GND4 | riferimento |

Per un normale carico 12 V a due fili, collegare il carico alla coppia OUT+/OUT- del canale corrispondente, dopo aver verificato il comportamento del modulo reale. Se il mulino verrà spostato su un modulo relè, D8 verrà riassegnato e questa riga sarà aggiornata.

### 7. Pulsanti

I pulsanti sono momentanei NO. Grazie a INPUT_PULLUP non servono resistenze esterne.

| Filo | Da | A |
|---|---|---|
| 43 | Mega D22 | START/STOP NO |
| 44 | START/STOP COM | Mega GND |
| 45 | Mega D23 | AVANTI NO |
| 46 | AVANTI COM | Mega GND |
| 47 | Mega D24 | TEST NO |
| 48 | TEST COM | Mega GND |

Gli eventuali contatti NC dei pulsanti rimangono scollegati.

### 8. Potenziometro B10K

| Filo | Da | A |
|---|---|---|
| 49 | Mega +5 V | estremo B10K |
| 50 | Mega A0 | cursore/centrale B10K |
| 51 | Mega GND | altro estremo B10K |

Se il senso di rotazione risulta invertito rispetto a quello desiderato, scambiare semplicemente i due fili degli estremi; il cursore A0 resta invariato.

### 9. Controllo prima dell'accensione

1. Mega scollegato dalla USB e alimentatore 12 V scollegato dalla rete.
2. Verificare che **+12 V non arrivi mai a 5V, A0 o a un pin digitale del Mega**.
3. Verificare con multimetro polarità +12 V / 0 V.
4. Verificare la massa comune Mega GND ↔ PSU 0 V.
5. Verificare i tre +12 V comuni delle strisce RGB.
6. Verificare che R/G/B vadano agli OUT- corretti.
7. Verificare DATA WS2811 e relativa resistenza.
8. Accendere inizialmente senza i carichi di movimento e usare il pulsante TEST.
9. Collegare poi un gruppo di carichi alla volta.

### Riepilogo pin Mega

| Pin | Funzione |
|---:|---|
| D2 | RGB principale R |
| D3 | RGB principale G |
| D4 | RGB principale B |
| D5 | DATA WS2811 |
| D6 | luci case |
| D7 | pompa |
| D8 | mulino (provvisorio, finché non si decide il relè) |
| D9 | grotta/lampioni |
| D10 | RGB tramonto R |
| D11 | RGB tramonto G |
| D12 | RGB tramonto B |
| D13 | PWM libero |
| D22 | START/STOP |
| D23 | AVANTI |
| D24 | TEST |
| D44 | RGB alba R |
| D45 | RGB alba G |
| D46 | RGB alba B |
| A0 | potenziometro B10K |

## Firmware

Aprire:

`firmware/PSN-Presepe/PSN-Presepe.ino`

con Arduino IDE standard e selezionare **Arduino Mega or Mega 2560**.

Il firmware attuale implementa cielo RGB principale, due RGB laterali alba/tramonto, stelle WS2811 e comandi. D6-D9 sono riservati nel sorgente al secondo modulo MOSFET della Fase 2.

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
