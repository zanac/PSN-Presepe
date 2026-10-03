EESchema Schematic File Version 4
EELAYER 29 0
EELAYER END
$Descr A3 16535 11693
Sheet 1 1
Title "PSN-Presepe Mega Controller Rev A"
Date "2026-10-01"
Rev "A"
Comp "zanac / PSN-Presepe"
Comment1 "APPROVED FUNCTIONAL ARCHITECTURE - CAD VALIDATION PENDING"
Comment2 "Single 12V input; Mega shield/carrier"
Comment3 "16 dry-contact relays; 9 RGB MOSFET"
Comment4 "WS2811 DATA direct to terminals"
$EndDescr
Text Notes 900 900 0 120 ~ 24
PSN-PRESEPE PCB REV A
Text Notes 900 1200 0 70 ~ 12
J1: +12V / GND. +12V_BUS feeds loads, relay coils and Mega VIN path. Never feed 12V into Mega 5V.
Text Notes 900 1700 0 80 ~ 16
MEGA PINOUT
Text Notes 900 1950 0 60 ~ 12
D2/3/4 CIELO; D5 STELLE; D6 BUZZER; D7/11/12 TRAMONTO; D8 CASETTE
Text Notes 900 2100 0 60 ~ 12
D20/21 OLED; D22/23/24 buttons; D25..40 relays; D44/45/46 ALBA; A0 B10K
Text Notes 900 2700 0 80 ~ 16
RGB x9: PWM -> 100R -> IRLZ44N gate; 100k gate-GND; source GND; drain LED negative
Text Notes 900 3100 0 80 ~ 16
WS2811 TERMINALS
Text Notes 900 3350 0 60 ~ 12
STELLE = +12V / GND / DATA directly from D5
Text Notes 900 3500 0 60 ~ 12
CASETTE = +12V / GND / DATA directly from D8
Text Notes 900 3650 0 60 ~ 12
NO SERIES DATA RESISTORS OR BUFFER ON PCB
Text Notes 900 4250 0 80 ~ 16
UI: START D22/GND; NEXT D23/GND; TEST D24/GND; OLED +5/GND/SDA/SCL
Text Notes 900 4450 0 60 ~ 12
B10K and passive buzzer are mounted onboard.
Text Notes 900 5100 0 80 ~ 16
RELAY COILS
Text Notes 900 5350 0 60 ~ 12
U1 ULN2803C D25..D32 -> K1..K8; U2 D33..D40 -> K9..K16
Text Notes 900 5500 0 60 ~ 12
Coil + = +12V_RELAY; ULN COM clamp = +12V_RELAY; common SELV GND
Text Notes 8500 1700 0 90 ~ 18
RELAY CONTACT TERMINALS
Text Notes 8500 2000 0 70 ~ 12
K1..K16 each terminate ONLY at COM / NO / NC.
Text Notes 8500 2200 0 70 ~ 12
NO MAINS L/N DISTRIBUTION EXISTS ON THIS PCB.
Text Notes 8500 2400 0 70 ~ 12
External wiring may use 230 VAC, therefore contact area remains isolated from SELV.
Text Notes 8500 3000 0 80 ~ 16
TERMINALS
Text Notes 8500 3250 0 60 ~ 12
12V/GND; CIELO 4p; TRAMONTO 4p; ALBA 4p; STELLE 3p; CASETTE 3p
Text Notes 8500 3400 0 60 ~ 12
START 2p; NEXT 2p; TEST 2p; OLED 4p; 16 x COM/NO/NC 3p
Text Notes 8500 4100 0 70 ~ 12
Draft source: exact footprints, ERC, isolation rules, PCB DRC and Gerbers still pending.
$EndSCHEMATC
