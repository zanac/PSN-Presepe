# Simulazione Wokwi — PSN-Presepe

[Apri Wokwi con Arduino Mega](https://wokwi.com/projects/new/arduino-mega)

La simulazione segue il cablaggio attuale del firmware su `main`. Per provarla nel browser, crea un progetto Arduino Mega su Wokwi e copia:
- `simulation/diagram.json` nel diagramma Wokwi;
- `firmware/PSN-Presepe/PSN-Presepe.ino` nel file `sketch.ino`;
- `simulation/libraries.txt` nel Library Manager (`libraries.txt`).

## Componenti simulati

| Hardware reale | Simulazione | Pin Mega |
|---|---|---|
| RGB cielo tramite MOSFET | 3 LED indicatori PWM | D2/D3/D4 |
| Stelle WS2811 12 V, 50 pixel | striscia NeoPixel WS2812 **5 V solo nel simulatore** | D5 |
| RGB tramonto, sinistra | 3 LED indicatori PWM | D10/D11/D12 |
| RGB alba, destra | 3 LED indicatori PWM | D44/D45/D46 |
| OLED ELEGOO EL-SM-008 I²C 0x3C | SSD1306 128×64 | SDA D20 / SCL D21 |
| START/STOP, AVANTI, TEST | 3 pulsanti verso GND | D22/D23/D24 |
| B10K | potenziometro | A0 |
| Quattro schede relè da 4 canali | **16 LED indicatori di pin**, non relè di potenza | D25–D40 |

**Importante:** le 16 uscite relè D25–D40 sono gestite dal firmware e nel simulatore usano HIGH=ON (`RELE_ACTIVE_LOW=false`). Gli indicatori sono denominati `Grp_01_01`–`Grp_04_04`. La modalità TEST le prova singolarmente; inoltre la tabella `SCHEDULAZIONE_RELE[]` gestisce le accensioni durante le fasi. Nel modulo relè reale andranno comunque verificati i selettori HIGH/LOW e la compatibilità degli ingressi prima del collegamento definitivo.

La striscia Wokwi WS2812 è un sostituto visivo: **nel montaggio reale le stelle WS2811 richiedono 12 V protetti, GND comune e una resistenza dati da 330–470 Ω**. I LED RGB Wokwi rappresentano i segnali PWM, non simulano l'alimentazione a 12 V né la portata dei MOSFET. La simulazione non sostituisce la verifica elettrica dei moduli reali.

## Librerie

Il firmware richiede `Adafruit NeoPixel`, `Adafruit SSD1306` e `Adafruit GFX Library`. L'OLED resta opzionale: se non è presente, il programma prosegue.

La GitHub Action `Arduino Mega Build` compila il firmware, ma **non esegue automaticamente la simulazione Wokwi**. Il file `wokwi.toml` è predisposto per un eventuale futuro test automatizzato.

> **Stelle:** i 50 pixel WS2811 restano fisicamente disponibili, ma a ogni ciclo ne vengono scelte casualmente solo **20**, mantenute a luminosità volutamente bassa. Di queste, esattamente **7** variano dolcemente la luminosità durante la notte per simulare il tremolio. A ogni nuova notte la disposizione viene rigenerata.


## Comandi e modalità TEST

- **START/STOP** mette in pausa e riprende il ciclo. In pausa l'OLED mostra stabilmente fase, percentuale della fase e i valori RGB correnti: `C` = cielo principale, `T` = tramonto, `A` = alba. Alla ripresa compare brevemente `RIPRESA`.
- **AVANTI** salta all'inizio della fase successiva.
- **TEST** entra nella modalità di collaudo e, a ogni pressione, passa al test successivo. **START/STOP** esce dalla modalità TEST e ripristina il punto del ciclo precedente.

La sequenza TEST attuale comprende **30 passaggi**: CIELO R/G/B, TRAMONTO R/G/B, ALBA R/G/B, STELLE R/G/B su tutti i 50 pixel, tutte le 50 stelle in bianco caldo, tutto insieme e infine i 16 relè `Grp_01_01`–`Grp_04_04` uno alla volta.

## Schedulazione relè

Il firmware contiene `SCHEDULAZIONE_RELE[]`, con eventi nel formato `{ FASE, RELE, STATO, PERCENTUALE_FASE }`. L'esempio attuale accende `Grp_01_03` al 30% di TRAMONTO e lo spegne al 50% di NOTTE. La percentuale è relativa alla singola fase.
