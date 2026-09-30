# PSN-Presepe PCB — schema elettrico Rev A

> Configurazione funzionale approvata. Non ancora release di produzione.

## 1. Alimentazione unica
J1: pin 1 +12V_IN, pin 2 GND.
+12V_IN -> F_MAIN/protezione -> +12V_BUS.
+12V_BUS alimenta RGB, STELLE, CASETTE, bobine relè e VIN del Mega. Il pin 5V del Mega NON riceve 12 V; +5V_MEGA è un'uscita logica usata per OLED/B10K.

## 2. MOSFET RGB x9
PWM Mega -> 100R -> gate IRLZ44N; 100k gate-GND; source GND; drain ritorno R/G/B.
Morsetti: CIELO, TRAMONTO, ALBA = +12V/R/G/B.

## 3. WS2811
J_STELLE = +12V / GND / DATA direttamente D5.
J_CASETTE = +12V / GND / DATA direttamente D8.
**Nessuna resistenza serie, buffer o protezione DATA onboard.**

## 4. Pulsanti
J_START D22/GND; J_NEXT D23/GND; J_TEST D24/GND. Contatti NO, firmware INPUT_PULLUP.

## 5. B10K e OLED
RV1 B10K onboard: +5V_MEGA / A0 cursore / GND.
J_OLED: +5V_MEGA / GND / SDA D20 / SCL D21.

## 6. Buzzer
BZ1 piezo passivo onboard, D6; driver discreto se richiesto dal buzzer definitivo.

## 7. Driver 16 relè
U1 ULN2803C: D25..D32 -> K1..K8.
U2 ULN2803C: D33..D40 -> K9..K16.
Bobina positiva -> +12V_RELAY; negativa -> uscita ULN; COM clamp ULN -> +12V_RELAY; GND -> GND.
470uF/25V bulk sul banco relè e decoupling locale.

## 8. Relè
K1..K16: Omron G5Q-1 DC12 candidato, SPDT.
Ogni contatto va soltanto al relativo morsetto JRn: COM / NO / NC.
**Nessuna fase, neutro o barra 230 V comune sulla PCB.**

## 9. Separazione
Bobine e driver sono SELV; i contatti possono essere usati esternamente a 230 VAC. Nessun rame SELV/piano GND deve invadere la barriera verso contatti e morsetti. Clearance/creepage finali saranno fissate nel layout dopo verifica dei footprint e delle condizioni d'impiego.

## 10. Morsetti
1x 2 poli alimentazione; 3x 4 poli RGB; 2x 3 poli WS2811; 3x 2 poli pulsanti; 1x 4 poli OLED; 16x 3 poli relè COM/NO/NC.

## 11. Prima dei Gerber
Verificare footprint G5Q, morsetti, ingresso 12V->VIN Mega, correnti/fusibili, MOSFET, ERC, isolamento, DRC e Gerber.
