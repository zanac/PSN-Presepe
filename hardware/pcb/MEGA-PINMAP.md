# Arduino Mega 2560 — pin map e shield superiore

Questa PCB usa connettori Mega R3 **stackable/pass-through**: un secondo shield può essere montato sopra PSN-Presepe, ma deve rispettare i conflitti elettrici indicati qui.

## Pin occupati da PSN-Presepe

| Pin | Funzione PSN |
|---|---|
| A0 | Potenziometro velocità |
| D2 | CIELO R |
| D3 | CIELO G |
| D4 | CIELO B |
| D5 | STELLE DATA WS2811 |
| D6 | Buzzer |
| D7 | TRAMONTO R |
| D8 | CASETTE DATA WS2811 |
| D11 | TRAMONTO G |
| D12 | TRAMONTO B |
| D20 / SDA | OLED I2C — condivisibile solo con device I2C compatibili e indirizzi non in conflitto |
| D21 / SCL | OLED I2C — condivisibile solo con device I2C compatibili |
| D22 | START |
| D23 | NEXT |
| D24 | TEST |
| D25-D40 | RELAY 1-16 |
| D44 | ALBA R |
| D45 | ALBA G |
| D46 | ALBA B |
| VIN | +12 V alimentazione |

## Pin verificati liberi / protetti dal gate CI

A1, D9, D10, D13, D41, D42, D43 e IOREF non sono collegati a funzioni PSN nella revisione corrente.

Questi pin sono protetti dal controllo CI `check_mega_pinmap.py`: se una modifica PCB li collega accidentalmente, il gate fallisce.

## Regola per un secondo shield

Il pass-through fisico **non implica compatibilità elettrica**. Lo shield superiore non deve pilotare direttamente un pin già usato da PSN. D20/SDA e D21/SCL possono essere condivisi come normale bus I2C se tensione, pull-up, indirizzi e caratteristiche dei dispositivi sono compatibili. Le alimentazioni condivise devono inoltre rispettare i limiti elettrici dell'intero sistema.
