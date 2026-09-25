# Simulazione Wokwi — PSN-Presepe

[Apri Wokwi con Arduino Mega](https://wokwi.com/projects/new/arduino-mega)

La simulazione segue il cablaggio attuale del firmware del branch di lavoro. Per lo sviluppo e i test usare `dev`; `main` resta la versione stabile. Per provarla nel browser, crea un progetto Arduino Mega su Wokwi e copia:
- `simulation/diagram.json` nel diagramma Wokwi;
- in alternativa, `simulation/diagram-no-display.json` per provare il sistema senza OLED;
- `firmware/PSN-Presepe/PSN-Presepe.ino` nel file `sketch.ino`;
- `simulation/rgb-strip.chip.json` e `simulation/rgb-strip.chip.c` nel progetto Wokwi;
- `simulation/libraries.txt` nel Library Manager (`libraries.txt`).

## Variante senza display

Il file `simulation/diagram-no-display.json` è una variante del diagramma principale creata appositamente per verificare il comportamento del controller quando l'OLED non è collegato. Contiene lo stesso hardware simulato di `diagram.json`, ad eccezione del display SSD1306 e dei relativi collegamenti VCC, GND, SDA e SCL.

**Regola di manutenzione:** ogni modifica futura a `simulation/diagram.json` che riguarda cablaggio, controlli, stelle, relè, strisce RGB o altri componenti deve essere riportata anche in `simulation/diagram-no-display.json`. Le modifiche che riguardano esclusivamente l'OLED restano invece solo nel diagramma principale.

Per eseguire il test senza display, copiare il contenuto di `diagram-no-display.json` nel `diagram.json` del progetto Wokwi. Il firmware non va modificato: deve rilevare l'assenza dell'OLED e continuare normalmente con autotest, ciclo scenografico, pulsanti, stelle, RGB e relè.

## Componenti simulati

| Hardware reale | Simulazione | Pin Mega |
|---|---|---|
| RGB cielo tramite MOSFET | barra custom `chip-rgb-strip` | D2/D3/D4 |
| Stelle WS2811 12 V, 50 pixel | striscia NeoPixel WS2812 **5 V solo nel simulatore** | D5 |
| Buzzer piezo passivo opzionale | buzzer Wokwi | D6 |
| RGB tramonto, sinistra | barra custom `chip-rgb-strip` | D10/D11/D12 |
| RGB alba, destra | barra custom `chip-rgb-strip` | D44/D45/D46 |
| OLED ELEGOO EL-SM-008 I²C 0x3C | SSD1306 128×64 | SDA D20 / SCL D21 |
| START/STOP, AVANTI, TEST | 3 pulsanti verso GND | D22/D23/D24 |
| B10K | potenziometro | A0 |
| Quattro schede relè da 4 canali | **16 LED indicatori di pin**, non relè di potenza | D25–D40 |

**Importante:** le 16 uscite relè D25–D40 sono gestite dal firmware e nel simulatore usano HIGH=ON (`RELE_ACTIVE_LOW=false`). Gli indicatori sono denominati `Grp_01_01`–`Grp_04_04`. La modalità TEST le prova singolarmente; inoltre la tabella `SCHEDULAZIONE_RELE[]` gestisce le accensioni durante le fasi. Nel modulo relè reale andranno comunque verificati i selettori HIGH/LOW e la compatibilità degli ingressi prima del collegamento definitivo.

La striscia Wokwi WS2812 è un sostituto visivo: **nel montaggio reale le stelle WS2811 richiedono 12 V protetti, GND comune e una resistenza dati da 330–470 Ω**. Le barre RGB custom Wokwi rappresentano i segnali PWM, non simulano l'alimentazione a 12 V né la portata dei MOSFET. La simulazione non sostituisce la verifica elettrica dei moduli reali.

## Componenti custom RGB Strip

Le tre strisce RGB analogiche non sono più rappresentate dai normali `wokwi-rgb-led`. Questi ultimi, anche quando ricevono RGB `(0,0,0)`, mantengono visibile il corpo chiaro del LED e possono dare l'impressione che una striscia spenta sia bianca.

Per evitare questa ambiguità PSN-Presepe usa un componente Wokwi personalizzato chiamato **RGB Strip**, composto da:

- `simulation/rgb-strip.chip.json`: definizione del componente, dei pin R/G/B e dell'area grafica;
- `simulation/rgb-strip.chip.c`: logica che legge i tre segnali PWM e disegna la barra tramite framebuffer;
- `simulation/diagram.json`: contiene tre istanze `chip-rgb-strip`, una per CIELO, TRAMONTO e ALBA.

Il componente misura il duty-cycle dei tre segnali PWM del Mega e visualizza direttamente il colore risultante. Gestisce anche i casi estremi di `analogWrite(0)` e `analogWrite(255)`, che sull'AVR diventano livelli logici statici. Sotto la zona colorata il framebuffer disegna inoltre una fascia nera con il nome **ALBA**, **CIELO** o **TRAMONTO**; l'istanza seleziona il testo tramite l'attributo numerico `labelId`.

La convenzione visiva è quindi volutamente semplice: **nero = striscia spenta**. Per esempio, durante GIORNO le barre ALBA e TRAMONTO sono nere perché il firmware invia `(0,0,0)`; durante le dissolvenze la barra cambia colore e luminosità seguendo il PWM.

Questo componente è **solo una rappresentazione grafica della simulazione**: non modifica il firmware e non simula elettricamente i MOSFET, l'alimentazione 12 V, le correnti o la potenza delle strisce reali.

### Aggiornare manualmente il progetto Wokwi

Quando cambia soltanto il firmware, è sufficiente ricopiare `PSN-Presepe.ino` in `sketch.ino`. Quando cambia il diagramma o il componente RGB custom, ricopiare anche i relativi file dalla cartella `simulation/`.

Per una nuova simulazione completa servono quindi almeno `sketch.ino`, `diagram.json`, `rgb-strip.chip.json`, `rgb-strip.chip.c` e le librerie indicate in `libraries.txt`.

## Librerie

Il firmware richiede `Adafruit NeoPixel`, `Adafruit SSD1306` e `Adafruit GFX Library`. L'OLED resta opzionale: se non è presente, il programma prosegue.

La GitHub Action `Arduino Mega Build` compila il firmware, ma **non esegue automaticamente la simulazione Wokwi**. Il file `wokwi.toml` è predisposto per un eventuale futuro test automatizzato.

> **Stelle:** i 50 pixel WS2811 restano fisicamente disponibili, ma a ogni ciclo ne vengono scelte casualmente solo **20**, mantenute a luminosità volutamente bassa. Tutte le 20 stelle attive hanno un proprio ciclo asincrono e variano dolcemente la luminosità. A ogni nuova notte la disposizione viene rigenerata.


## Boot simulato

All'avvio il firmware esegue anche in Wokwi l'autotest reale: **ALBA**, **CIELO** e **TRAMONTO** diventano bianchi per 2 secondi ciascuno, quindi tutti i 50 pixel delle **STELLE** diventano bianchi per 2 secondi. In contemporanea il buzzer passivo opzionale su **D6** riproduce, a tempo più sostenuto, **Astro del ciel** fino alla frase **“mite agnello Redentor”**. Se la melodia supera gli 8 secondi dell'autotest visivo, le uscite vengono spente e il boot ne attende la conclusione prima di mostrare PRONTO; se il buzzer reale non è collegato il firmware continua normalmente. L'OLED mostra l'avanzamento complessivo con una progress bar. Finito il test, le uscite vengono spente, l’OLED mostra **PRONTO** per 900 ms e parte da zero il normale ciclo nella fase GIORNO.

## Comandi e modalità TEST

- **START/STOP** mette in pausa e riprende il ciclo. In pausa l'OLED mostra stabilmente fase, percentuale della fase e i valori RGB correnti: `C` = cielo principale, `T` = tramonto, `A` = alba. Alla ripresa compare brevemente `RIPRESA`.
- **AVANTI** salta all'inizio della fase successiva.
- **TEST** entra nella modalità di collaudo e, a ogni pressione, passa al test successivo. **START/STOP** esce dalla modalità TEST e ripristina il punto del ciclo precedente.

La sequenza TEST attuale comprende **30 passaggi**: CIELO R/G/B, TRAMONTO R/G/B, ALBA R/G/B, STELLE R/G/B su tutti i 50 pixel, tutte le 50 stelle in bianco caldo, tutto insieme e infine i 16 relè `Grp_01_01`–`Grp_04_04` uno alla volta.

## Schedulazione relè

Il firmware contiene `SCHEDULAZIONE_RELE[]`, con eventi nel formato `{ FASE, RELE, STATO, PERCENTUALE_FASE }`. L'esempio attuale accende `Grp_01_03` al 30% di TRAMONTO e lo spegne al 50% di NOTTE. La percentuale è relativa alla singola fase.
