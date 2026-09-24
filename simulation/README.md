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

**Importante:** le 16 uscite relè sono soltanto *predisposte* nel firmware: la logica e la polarità HIGH/LOW dei moduli reali non sono ancora state definite. Gli indicatori Wokwi non sono un test del funzionamento dei relè e possono mostrare stati indefiniti se i pin sono ancora configurati come ingressi.

La striscia Wokwi WS2812 è un sostituto visivo: **nel montaggio reale le stelle WS2811 richiedono 12 V protetti, GND comune e una resistenza dati da 330–470 Ω**. I LED RGB Wokwi rappresentano i segnali PWM, non simulano l'alimentazione a 12 V né la portata dei MOSFET. La simulazione non sostituisce la verifica elettrica dei moduli reali.

## Librerie

Il firmware richiede `Adafruit NeoPixel`, `Adafruit SSD1306` e `Adafruit GFX Library`. L'OLED resta opzionale: se non è presente, il programma prosegue.

La GitHub Action `Arduino Mega Build` compila il firmware, ma **non esegue automaticamente la simulazione Wokwi**. Il file `wokwi.toml` è predisposto per un eventuale futuro test automatizzato.
