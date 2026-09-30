# PSN-Presepe PCB — layout Rev A

Scheda carrier/shield: Arduino Mega 2560 innestato direttamente, con USB accessibile dal bordo.

Disposizione:
- zona Mega + B10K + buzzer;
- bordo bassa tensione con ingresso +12V/GND, OLED, 3 pulsanti, 3 RGB e 2 WS2811;
- 9 MOSFET e 2 ULN2803C nella zona SELV;
- 16 relè in due file;
- 16 morsetti COM/NO/NC sul bordo opposto.

La PCB non contiene distribuzione L/N. Ogni relè è un contatto pulito indipendente. Poiché i contatti possono successivamente essere collegati a 230 VAC, la zona contatti/morsetti resta separata dalla SELV con keep-out rame e barriera di isolamento.

STELLE e CASETTE: +12V/GND/DATA direttamente al morsetto, senza componenti sul DATA.

Unico ingresso alimentazione: 12 V. Da esso derivano carichi, bobine e VIN Mega; +5V logico è fornito dal Mega.

Dimensioni PCB da congelare dopo footprint definitivo G5Q e disposizione dei 16 morsetti.
