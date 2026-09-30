# PSN-Presepe PCB — BOM Rev A

| Ref | Q.tà | Componente | Rev A |
|---|---:|---|---|
| MCU1 | 1 | Arduino Mega 2560 | modulo innestabile come shield |
| Q1-Q9 | 9 | MOSFET | IRLZ44N TO-220 |
| U1-U2 | 2 | driver relè | ULN2803C |
| K1-K16 | 16 | relè SPDT 12 V | Omron G5Q-1 DC12 candidato |
| JR1-JR16 | 16 | morsetti relè | 3 poli COM/NO/NC, Phoenix 5.08 mm candidato |
| JC/JT/JA | 3 | morsetti RGB | 4 poli +12V/R/G/B |
| JS/JK | 2 | morsetti WS2811 | 3 poli +12V/GND/DATA |
| JBTN1-3 | 3 | pulsanti | 2 poli segnale/GND |
| JOLED | 1 | OLED | 4 poli +5V/GND/SDA/SCL |
| J1 | 1 | alimentazione | 2 poli +12V/GND |
| RV1 | 1 | B10K | onboard |
| BZ1 | 1 | piezo passivo | onboard |

Passivi: 9x 100R gate, 9x 100k pulldown, decoupling ULN, 470uF/25V banco relè e componenti di protezione/fusione 12 V da finalizzare.

**Non presenti:** resistenze DATA STELLE/CASETTE. D5 e D8 arrivano direttamente ai rispettivi morsetti.

L'unico ingresso di alimentazione della PCB è 12 V. Il Mega viene alimentato dal 12 V attraverso VIN/percorso previsto del modulo; non si applica 12 V al pin 5V.
