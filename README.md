# PSN-Presepe

## Demo online Wokwi

▶️ [Apri la simulazione interattiva PSN-Presepe su Wokwi](https://wokwi.com/projects/476035349322038273)

La demo permette di provare direttamente dal browser il ciclo giorno/notte, le strisce RGB, il cielo stellato, OLED e comandi senza hardware reale.


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

### Relè ON/OFF — 4 moduli, 16 uscite

Luci case, pompe, mulino e gli altri carichi che richiedono soltanto ON/OFF vengono gestiti dai **quattro moduli relè 12 V a 4 canali**. I MOSFET restano dedicati ai carichi che richiedono PWM/dimmer.

| Gruppo | Mega | Modulo / ingresso |
|---|---:|---|
| Grp_01_01–Grp_01_04 | D25–D28 | RELÈ #1 IN1–IN4 |
| Grp_02_01–Grp_02_04 | D29–D32 | RELÈ #2 IN1–IN4 |
| Grp_03_01–Grp_03_04 | D33–D36 | RELÈ #3 IN1–IN4 |
| Grp_04_01–Grp_04_04 | D37–D40 | RELÈ #4 IN1–IN4 |

Per ogni scheda: **+12 V protetto → DC+**, **0 V comune → DC-**. I morsetti COM/NO/NC restano disponibili per i futuri carichi. Per un carico normalmente spento si useranno normalmente COM + NO.

I jumper S1–S4 permettono di scegliere HIGH/LOW trigger. Il firmware gestisce già le 16 uscite nella modalità TEST; nel simulatore viene usata la logica HIGH=ON. Prima del collegamento definitivo dei moduli reali va verificata la posizione dei jumper e, se necessario, impostato `RELE_ACTIVE_LOW` nel firmware.

#### Schedulazione scenografica dei relè

Le accensioni e gli spegnimenti durante il ciclo sono definiti nel firmware dalla tabella `SCHEDULAZIONE_RELE[]`. Ogni evento contiene:

`{ NOME_FASE, NOME_RELE, ACCESO_SPENTO, PERCENTUALE_FASE }`

La percentuale è **relativa alla singola fase**, non all'intero ciclo. Per esempio:

```cpp
const EventoRele SCHEDULAZIONE_RELE[] = {
  { TRAMONTO, Grp_01_03, true,  30 },
  { NOTTE,    Grp_01_03, false, 50 }
};
```

Con questa configurazione `Grp_01_03` si accende al **30% della fase TRAMONTO**, resta acceso durante il resto del tramonto, il crepuscolo e la prima metà della notte, quindi si spegne al **50% della fase NOTTE**.

Lo stato dei relè viene ricostruito dalla posizione corrente del ciclo, quindi rimane coerente anche usando **AVANTI**, pausa/ripresa o modificando la durata con il potenziometro. All'inizio di un nuovo ciclo, prima che siano raggiunti nuovi eventi, i relè partono spenti. In futuro la scenografia ON/OFF può essere modificata semplicemente aggiungendo o cambiando le righe della tabella.

### Display OLED ELEGOO EL-SM-008

Display di stato OLED **0,96 pollici, 128×64, I²C**, alimentazione 3,3–5 V, indirizzo I²C a 7 bit **0x3C**.

| OLED | Arduino Mega 2560 |
|---|---|
| GND | GND |
| VCC | 5V |
| SDA | D20 / SDA |
| SCL | D21 / SCL |

Il display è **opzionale**: il firmware deve continuare a funzionare normalmente anche se l'OLED non è collegato. All'avvio il software verifica la presenza del display all'indirizzo 0x3C; se non risponde, prosegue senza OLED.

Il firmware usa il display come interfaccia di stato:
- schermata normale: **fase corrente**, percentuale di avanzamento della singola fase, barra grafica, RUN/PAUSA e durata totale del ciclo;
- START/STOP: mette in pausa o riprende il ciclo; in **PAUSA** l'OLED mostra stabilmente fase, percentuale della fase e i valori RGB correnti delle tre strisce; alla ripresa mostra brevemente **RIPRESA**;
- AVANTI: popup **AVANTI** con la nuova fase;
- TEST: feedback **TEST**;
- variazione significativa del B10K: popup **VELOCITA** con la durata effettiva del ciclo in minuti.

I popup durano circa 1,8 secondi e poi il display torna automaticamente alla schermata della fase. L'aggiornamento normale dell'OLED è non bloccante; l'assenza del display non impedisce l'avvio del controllore.

> Nota: sul Mega 2560 l'I²C hardware usa **D20=SDA** e **D21=SCL**. Eventuali esempi che indicano D21/D22 si riferiscono ad altre piattaforme, ad esempio ESP32.


Il display è opzionale: all'avvio il firmware verifica se risponde all'indirizzo 0x3C; se non viene trovato, il ciclo scenografico continua normalmente senza OLED.

Quando il ciclo viene messo in **PAUSA**, l'OLED mostra stabilmente la fase e la percentuale raggiunta, insieme ai valori RGB correnti delle tre strisce:

- `C R,G,B` = cielo RGB principale;
- `T R,G,B` = RGB laterale TRAMONTO;
- `A R,G,B` = RGB laterale ALBA.

I valori sono quelli logici 0–255 inviati al PWM e permettono di fermare la scena su una tonalità interessante, trascriverla e riutilizzarla successivamente per la taratura dei colori.

### Comandi

| Arduino Mega | Dispositivo | Collegamento |
|---:|---|---|
| D22 | Pulsante START/STOP | D22 ↔ pulsante ↔ GND logica |
| D23 | Pulsante AVANTI | D23 ↔ pulsante ↔ GND logica |
| D24 | Pulsante TEST | D24 ↔ pulsante ↔ GND logica |

> **Prova senza potenziometro:** se il potenziometro B10K su A0 viene scollegato, non lasciare A0 flottante: la lettura analogica potrebbe assumere valori casuali e far variare la durata del ciclo. Per una prova stabile, collegare temporaneamente **A0 direttamente a GND**. Il firmware leggerà A0=0, corrispondente alla durata minima del ciclo di **1 minuto**.
| A0 | Potenziometro B10K velocità ciclo | 5V ↔ esterno, A0 ↔ cursore, GND ↔ esterno |

I pulsanti utilizzano `INPUT_PULLUP`, quindi non richiedono una resistenza di pull-up esterna. Il GND logico di Arduino viene distribuito tramite WAGO agli ingressi `GND1...GND4` dei MOSFET e ai comandi.

## Sequenza di inizializzazione all'accensione

Prima di iniziare il normale ciclo scenografico, il firmware esegue un **autotest visivo di circa 8 secondi**. I relè restano spenti e le uscite vengono provate in sequenza:

1. **ALBA** — striscia RGB alba in bianco brillante per 2 secondi;
2. **CIELO** — striscia RGB principale in bianco brillante per 2 secondi;
3. **TRAMONTO** — striscia RGB tramonto in bianco brillante per 2 secondi;
4. **STELLE** — tutti i 50 pixel WS2811 in bianco brillante per 2 secondi.

Durante l'intera sequenza l'OLED mostra **Inizializzazione**, il nome dell'uscita in prova, la percentuale complessiva e una progress bar. Al termine tutte le uscite vengono spente, compare **PRONTO** per 900 ms e il timer del ciclo viene avviato da zero: il presepe entra quindi normalmente nella fase **GIORNO**.

Questa sequenza è visibile anche nella simulazione Wokwi e costituisce un rapido controllo all'accensione di strisce, stelle e relativi collegamenti.

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

> **Cosa significa “+12 V protetto” in questo manuale?**  
> Significa semplicemente che il filo **positivo +12 V è passato attraverso un fusibile prima di raggiungere il carico**. Il fusibile va quindi inserito **sul polo positivo (+12 V)** del ramo da proteggere, non sullo 0 V/negativo.
>
> Esempio: `alimentatore +12 V → fusibile → striscia LED +12 V`.
>
> Se un cavo o un utilizzatore va in cortocircuito, il fusibile di quel ramo interrompe il positivo e protegge soprattutto **cablaggio e connettori** dalla forte corrente che l'alimentatore potrebbe fornire. Quando nelle tabelle seguenti compare la dicitura **“+12 V protetto”**, bisogna quindi leggere: **“+12 V proveniente da un'uscita del portafusibili”**.

Portare il **+12 V** dell'alimentatore all'ingresso positivo del portafusibili/distributore. Ogni uscita del portafusibili avrà il proprio fusibile e alimenterà un singolo ramo: RGB principale, stelle WS2811, RGB tramonto, RGB alba e gli altri carichi. Lo **0 V (negativo)** non passa attraverso questi fusibili di ramo: viene portato alla barra negativa del distributore, se presente, oppure a una morsettiera/WAGO 0 V comune.

```text
ALIMENTATORE 12 V

 +12 V ──► ingresso + portafusibili
                │
                ├─► F1 CIELO ─────► +12 V RGB principale + DC+ MOSFET #1
                ├─► F2 ALBA ──────► +12 V RGB alba + DC+ MOSFET #4
                ├─► F3 TRAMONTO ──► +12 V RGB tramonto + DC+ MOSFET #3
                ├─► F4 STELLE ────► +12 V WS2811
                └─► ... futuri rami protetti (relè/carichi)

  0 V ────────────────────────────► barra negativa / WAGO 0 V comune
                                      ├─► GND/0 V carichi
                                      └─► GND Arduino (riferimento comune)
```

**Scelta progettuale:** CIELO, ALBA, TRAMONTO e STELLE hanno ciascuno un fusibile dedicato. Per le tre strisce RGB, l'uscita del relativo fusibile viene sdoppiata: alimenta sia il +12 V comune della striscia sia il `DC+` della scheda MOSFET che la pilota. Il `DC-` della scheda MOSFET torna allo 0 V comune. Non è previsto un ulteriore fusibile generico separato per le quattro schede MOSFET: la protezione segue il ramo/carico alimentato. Il MOSFET #2, al momento non assegnato a una delle tre RGB, verrà protetto insieme al futuro ramo che utilizzerà.

**Regola pratica per il montaggio:** ogni volta che nel manuale leggi `+12 V protetto`, **non collegare quel filo direttamente al +12 V dell'alimentatore**: collegalo a una delle uscite positive del portafusibili, dopo il relativo fusibile.

| Da | A | Nota |
|---|---|---|
| PSU +12 V | ingresso portafusibili +12 V | cavo dimensionato per la corrente totale |
| PSU 0 V | WAGO/morsettiera 0 V comune | ritorno comune |
| WAGO 0 V | Mega GND | riferimento logico comune |
| WAGO 0 V | DC- MOSFET #1 | ritorno comune modulo CIELO |
| WAGO 0 V | DC- MOSFET #2 | modulo disponibile per futuri carichi |
| WAGO 0 V | DC- MOSFET #3 | ritorno comune modulo TRAMONTO |
| WAGO 0 V | DC- MOSFET #4 | ritorno comune modulo ALBA |
| F1 — CIELO | RGB principale +12 V e DC+ MOSFET #1 | ramo protetto dedicato |
| F2 — ALBA | RGB alba +12 V e DC+ MOSFET #4 | ramo protetto dedicato |
| F3 — TRAMONTO | RGB tramonto +12 V e DC+ MOSFET #3 | ramo protetto dedicato |
| F4 — STELLE | WS2811 +12 V | ramo protetto dedicato |

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

### 6. Quattro moduli relè — 16 uscite ON/OFF

I quattro moduli vengono montati e collegati al Mega. Tutti i carichi che richiedono soltanto ON/OFF — casette, pompa, mulino, grotta, lampioni e altri effetti — devono essere assegnati a queste 16 uscite. D6–D9 non sono più riservati a questi carichi.

La nomenclatura standard è `Grp_GG_RR`: `GG` identifica il gruppo/scheda relè (01–04) e `RR` il relè del gruppo (01–04).

| Uscita | Mega | Modulo / ingresso |
|---|---:|---|
| Grp_01_01 | D25 | RELÈ #1 IN1 |
| Grp_01_02 | D26 | RELÈ #1 IN2 |
| Grp_01_03 | D27 | RELÈ #1 IN3 |
| Grp_01_04 | D28 | RELÈ #1 IN4 |
| Grp_02_01 | D29 | RELÈ #2 IN1 |
| Grp_02_02 | D30 | RELÈ #2 IN2 |
| Grp_02_03 | D31 | RELÈ #2 IN3 |
| Grp_02_04 | D32 | RELÈ #2 IN4 |
| Grp_03_01 | D33 | RELÈ #3 IN1 |
| Grp_03_02 | D34 | RELÈ #3 IN2 |
| Grp_03_03 | D35 | RELÈ #3 IN3 |
| Grp_03_04 | D36 | RELÈ #3 IN4 |
| Grp_04_01 | D37 | RELÈ #4 IN1 |
| Grp_04_02 | D38 | RELÈ #4 IN2 |
| Grp_04_03 | D39 | RELÈ #4 IN3 |
| Grp_04_04 | D40 | RELÈ #4 IN4 |

Per **ciascuno dei quattro moduli** collegare anche:

| Da | A |
|---|---|
| uscita +12 V del portafusibili | DC+ |
| 0 V comune | DC- |
| pin Mega indicato sopra | IN1 / IN2 / IN3 / IN4 |

Per ora i morsetti **COM/NO/NC possono rimanere senza carico**. Così tutta la parte di comando `Grp_01_01`–`Grp_04_04` è montata e pronta. In modalità TEST le 16 uscite vengono provate una alla volta, una pressione di TEST per ciascun relè. La sequenza completa comprende 30 test: CIELO R/G/B, TRAMONTO R/G/B, ALBA R/G/B, STELLE R/G/B su tutti i 50 pixel, tutte le 50 stelle in bianco caldo, tutto insieme e infine i 16 relè individuali.

Quando assegneremo un carico 12 V normalmente spento, lo schema tipico sarà: **+12 V protetto → COM → NO → positivo carico**, mentre il negativo del carico torna allo **0 V comune**.

### 7. Display OLED EL-SM-008

Collegare i quattro fili:

| Filo | Da | A |
|---|---|---|
| OLED 1 | GND | Mega GND |
| OLED 2 | VCC | Mega 5V |
| OLED 3 | SCL | Mega D21 / SCL |
| OLED 4 | SDA | Mega D20 / SDA |

Indirizzo I²C firmware: **0x3C**. Il display è opzionale: se viene scollegato o dimenticato, il controllore del presepe deve continuare a funzionare.

### 8. Pulsanti

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
| D6–D9 | liberi / riserva |
| D10 | RGB tramonto R |
| D11 | RGB tramonto G |
| D12 | RGB tramonto B |
| D13 | PWM libero |
| D22 | START/STOP |
| D23 | AVANTI |
| D20 | SDA OLED EL-SM-008 (I²C, opzionale) |
| D21 | SCL OLED EL-SM-008 (I²C, opzionale) |
| D24 | TEST |
| D25–D40 | Grp_01_01–Grp_04_04, quattro moduli relè |
| D44 | RGB alba R |
| D45 | RGB alba G |
| D46 | RGB alba B |
| A0 | potenziometro B10K |

## Firmware

Aprire:

`firmware/PSN-Presepe/PSN-Presepe.ino`

con Arduino IDE standard e selezionare **Arduino Mega or Mega 2560**.

Il firmware attuale implementa cielo RGB principale, due RGB laterali alba/tramonto, stelle WS2811, comandi, OLED e modalità TEST. D6–D9 sono liberi/di riserva. I carichi ON/OFF vengono gestiti tramite i 16 relè D25–D40.

## GitHub Actions

Il workflow `.github/workflows/build.yml` può essere avviato manualmente dalla pagina GitHub Actions e parte automaticamente quando viene pubblicata una nuova GitHub Release associata a un tag. Compila il firmware per:

`arduino:avr:mega`

I file compilati vengono pubblicati come artifact della GitHub Action. Per le build avviate da una Release vengono inoltre allegati alla Release il firmware `PSN-Presepe.ino.hex` e il pacchetto `PSN-Presepe-Windows-Portable.zip`.

## Simulazione Wokwi

La simulazione Wokwi riproduce Mega 2560, OLED, pulsanti, potenziometro, 50 stelle indirizzabili, 16 uscite relè e le tre strisce RGB. Il file principale è `simulation/diagram.json`.

È disponibile anche `simulation/diagram-no-display.json`, variante dedicata ai test **senza OLED**: è mantenuta allineata a `diagram.json` per tutte le modifiche di cablaggio e componenti che non riguardano il display. Serve a verificare che il firmware continui ad avviarsi e funzionare normalmente quando l'OLED opzionale non è presente.

Per le strisce CIELO, TRAMONTO e ALBA vengono usati i componenti custom `rgb-strip.chip.json` + `rgb-strip.chip.c`: leggono i tre PWM R/G/B e visualizzano una barra del colore risultante. A differenza del normale LED RGB di Wokwi, una striscia a `(0,0,0)` viene mostrata **completamente nera**, quindi nero significa inequivocabilmente **SPENTO**. Il componente gestisce anche PWM 0 e 255 come livelli statici.

I componenti custom sono esclusivamente visuali: non cambiano il firmware e non simulano la potenza elettrica, i MOSFET o i 12 V reali. La documentazione completa della simulazione e dei file da copiare manualmente nel progetto Wokwi è in `simulation/README.md`.

La CI Wokwi rimane per ora opzionale: la normale compilazione GitHub Actions non richiede token o servizi esterni.

## Nota elettrica

Con l'introduzione delle stelle WS2811, **Arduino GND e lo 0 V dell'alimentatore 12 V sono collegati in comune** per fornire il riferimento al segnale DATA. Il Mega resta alimentato separatamente a 5 V via USB. Prima del cablaggio definitivo verificare con il multimetro la continuità tra `DC+` e gli eventuali `OUT+` utilizzati. Per pompa e mulino devono inoltre essere verificati corrente nominale, corrente di spunto e protezione dei carichi induttivi.

---

By **Vanni Brutto**

## 🧪 Provare PSN-Presepe online con Wokwi — guida passo passo

La simulazione permette di provare il firmware **direttamente dal browser**, senza installare Arduino IDE e senza collegare il Mega reale.

> **Importante:** Wokwi serve soprattutto a verificare firmware, pulsanti, potenziometro, OLED e sequenze. Non simula fedelmente la parte elettrica a 12 V, la potenza dei MOSFET o i carichi reali. I 16 relè sono rappresentati da indicatori.

### 1. Apri un nuovo Arduino Mega

Apri questo indirizzo nel browser:

**https://wokwi.com/projects/new/arduino-mega**

Deve comparire un progetto nuovo con un **Arduino Mega 2560**.

### 2. Copia il firmware

Nel repository PSN-Presepe apri:

`firmware/PSN-Presepe/PSN-Presepe.ino`

Premi il pulsante GitHub per copiare tutto il contenuto del file.

Torna su Wokwi, apri il file **sketch.ino**, cancella tutto quello che contiene e incolla il firmware PSN-Presepe.

> Su Wokwi il file si chiama `sketch.ino`; nel repository si chiama `PSN-Presepe.ino`. È normale.

### 3. Installa le tre librerie

Nel pannello del codice di Wokwi apri **Library Manager** e aggiungi:

```text
Adafruit NeoPixel
Adafruit SSD1306
Adafruit GFX Library
```

Wokwi creerà automaticamente il proprio `libraries.txt`.

Nel repository è presente anche `simulation/libraries.txt` come riferimento aggiornato delle librerie necessarie.

### 4. Carica il nostro schema elettrico virtuale

Nel repository apri:

`simulation/diagram.json`

Copia **tutto** il contenuto.

In Wokwi apri il file **diagram.json**, seleziona tutto, cancella il contenuto esistente e incolla quello del repository.

Dopo pochi istanti il diagramma deve mostrare il Mega e i componenti del PSN-Presepe.

### 5. Avvia

Premi il pulsante verde **▶ Start Simulation**.

Wokwi compilerà il firmware. La prima compilazione può richiedere qualche secondo.

Se tutto è corretto, il Mega virtuale parte e sul display OLED deve apparire l'interfaccia PSN-Presepe.

### 6. Prova il potenziometro

Clicca sul potenziometro **Durata ciclo** e cambiane il valore.

L'OLED deve mostrare temporaneamente **VELOCITA** e la durata del ciclo. Dopo circa 1,8 secondi ritorna alla schermata della fase corrente.

Per fare prove veloci conviene portare il ciclo verso il minimo, circa **1 minuto**.

### 7. Prova i pulsanti

Usa i tre pulsanti virtuali:

| Pulsante | Cosa deve succedere |
|---|---|
| START/STOP | mette in pausa/riprende il ciclo; in PAUSA l'OLED resta sulla schermata con fase, % fase e valori RGB C/T/A; alla ripresa mostra brevemente RIPRESA |
| AVANTI | salta immediatamente alla fase successiva |
| TEST | avvia la sequenza di prova delle uscite |

Con **AVANTI** puoi quindi controllare rapidamente:

`GIORNO → TRAMONTO → CREPUSCOLO → NOTTE → ALBA → GIORNO`

senza aspettare l'intero ciclo.

### 8. Cosa guardare sull'OLED

Durante il funzionamento normale deve mostrare:

- nome della fase;
- percentuale **0–100% della fase corrente**;
- barra di avanzamento;
- RUN durante il ciclo; quando è in PAUSA la schermata viene sostituita dai valori RGB delle tre strisce;
- durata impostata del ciclo.

La percentuale riparte da 0 quando cambia fase.

### 9. Apri il Serial Monitor

Durante la simulazione apri **Serial Monitor**.

Il firmware comunica a **115200 baud** e stampa informazioni diagnostiche: fase, percentuale del ciclo, durata, valore A0 e stato RUN/PAUSA.

Se l'OLED virtuale non viene rilevato, il firmware deve comunque continuare a funzionare: è intenzionalmente opzionale.

### 10. Cosa rappresentano i LED virtuali

I LED R/G/B simulano i **segnali di comando PWM** delle tre strisce RGB reali. Non rappresentano direttamente una striscia 12 V.

La striscia NeoPixel virtuale rappresenta le **50 stelle**. Wokwi usa un componente addressable compatibile per visualizzare l'effetto; nel presepe reale utilizziamo la stringa WS2811 a 12 V con il cablaggio documentato.

Gli indicatori `Grp_01_01`–`Grp_04_04` rappresentano le 16 uscite dei quattro moduli relè collegate a D25–D40. In modalità TEST vengono accese una alla volta dopo i 14 test di cielo/RGB/stelle; dopo `Grp_04_04` la sequenza riparte dal primo test e START esce dalla modalità TEST.

### 11. Se Wokwi dà errore

Controlla nell'ordine:

1. di aver scelto **Arduino Mega 2560**;
2. che `sketch.ino` contenga l'ultima versione del firmware;
3. che siano installate tutte e tre le librerie;
4. che `diagram.json` sia stato copiato integralmente da `simulation/diagram.json`;
5. leggi il messaggio rosso della compilazione o il Serial Monitor.

Se modifichiamo firmware o cablaggio del progetto, anche i file nella cartella `simulation/` devono essere aggiornati insieme.


> **Stelle:** i 50 pixel WS2811 restano fisicamente disponibili, ma a ogni ciclo ne vengono scelte casualmente solo **20**, mantenute a luminosità volutamente bassa. Tutte le 20 stelle attive hanno un proprio ciclo asincrono e variano dolcemente la luminosità. A ogni nuova notte la disposizione viene rigenerata.
