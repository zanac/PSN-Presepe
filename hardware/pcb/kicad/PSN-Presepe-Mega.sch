EESchema Schematic File Version 4
LIBS:power
LIBS:device
LIBS:Connector_Generic
LIBS:Transistor_FET
LIBS:Relay
LIBS:Interface_Expansion
EELAYER 29 0
EELAYER END
$Descr A3 16535 11693
Sheet 1 1
Title "PSN-Presepe Mega Controller Rev A"
Date "2026-10-01"
Rev "A"
Comp "zanac / PSN-Presepe"
Comment1 "DESIGN DRAFT - NOT RELEASED FOR 230 VAC CONSTRUCTION"
Comment2 "Functional source for KiCad migration/validation"
Comment3 "Arduino Mega 2560 + 9 RGB MOSFET + 16 relays"
Comment4 "230 VAC contact zone must remain isolated from SELV"
$EndDescr
Text Notes 900 900 0 120 ~ 24
PSN-PRESEPE PCB REV A - FUNCTIONAL SCHEMATIC
Text Notes 900 1150 0 70 ~ 12
WARNING: draft. Validate relay footprint, creepage/clearance and ERC/DRC before fabrication.
Text Notes 900 1600 0 100 ~ 20
ARDUINO MEGA 2560 INTERFACE
Text Notes 900 1850 0 60 ~ 12
D2,D3,D4 = CIELO R,G,B
Text Notes 900 2000 0 60 ~ 12
D5 = STELLE DATA   D6 = BUZZER   D8 = CASETTE DATA
Text Notes 900 2150 0 60 ~ 12
D7,D11,D12 = TRAMONTO R,G,B
Text Notes 900 2300 0 60 ~ 12
D20,D21 = OLED SDA,SCL
Text Notes 900 2450 0 60 ~ 12
D22,D23,D24 = START,NEXT,TEST
Text Notes 900 2600 0 60 ~ 12
D25..D40 = RELAY 1..16
Text Notes 900 2750 0 60 ~ 12
D44,D45,D46 = ALBA R,G,B   A0 = B10K
Text Notes 900 3300 0 100 ~ 20
RGB POWER STAGES x9
Text Notes 900 3550 0 60 ~ 12
PWM -> 100R -> IRLZ44N gate; 100k gate-GND; source=GND; drain=LED negative
Text Notes 900 3700 0 60 ~ 12
Three 4-way terminals: +12V,R,G,B for CIELO / TRAMONTO / ALBA
Text Notes 900 4250 0 100 ~ 20
WS2811
Text Notes 900 4500 0 60 ~ 12
D5 -> 390R -> STELLE DATA; D8 -> 390R -> CASETTE DATA
Text Notes 900 4650 0 60 ~ 12
Each connector: +12V / GND / DATA
Text Notes 900 5200 0 100 ~ 20
16 RELAY COIL DRIVERS - SELV
Text Notes 900 5450 0 60 ~ 12
U1 ULN2803C: D25..D32 -> K1..K8 coil negative
Text Notes 900 5600 0 60 ~ 12
U2 ULN2803C: D33..D40 -> K9..K16 coil negative
Text Notes 900 5750 0 60 ~ 12
Coil positive = +12V_RELAY; ULN COM = +12V_RELAY; ULN GND = GND
Text Notes 900 5900 0 60 ~ 12
470uF/25V bulk on +12V_RELAY plus local 100nF decoupling
Text Notes 8500 1600 0 100 ~ 20
230 VAC CONTACT ZONE
Text Notes 8500 1850 0 70 ~ 12
K1..K16 candidate: Omron G5Q-1 DC12 SPDT
Text Notes 8500 2050 0 70 ~ 12
Each relay exposes independent COM / NO / NC only.
Text Notes 8500 2250 0 70 ~ 12
No shared mains L/N bus on PCB.
Text Notes 8500 2550 0 70 ~ 12
Terminal candidate: Phoenix Contact MKDS 1,5/3-5,08 (1715734)
Text Notes 8500 2900 0 70 ~ 12
NO SELV COPPER OR GROUND PLANE ACROSS ISOLATION BARRIER.
Text Notes 8500 3100 0 70 ~ 12
Final numerical creepage/clearance requires standards/environment review.
Text Notes 8500 3600 0 100 ~ 20
12 V DISTRIBUTION
Text Notes 8500 3850 0 60 ~ 12
J1 -> F_MAIN -> reverse-polarity protection -> +12V_BUS
Text Notes 8500 4000 0 60 ~ 12
Branches: CIELO / TRAMONTO / ALBA / STELLE / CASETTE / RELAY
Text Notes 8500 4500 0 100 ~ 20
USER INTERFACE
Text Notes 8500 4750 0 60 ~ 12
Buttons: D22/D23/D24 to NO contact, other side GND; INPUT_PULLUP
Text Notes 8500 4900 0 60 ~ 12
RV1 B10K: +5V / A0 wiper / GND
Text Notes 8500 5050 0 60 ~ 12
OLED: +5V / GND / SDA(D20) / SCL(D21)
Text Notes 8500 5200 0 60 ~ 12
Buzzer D6 through optional transistor driver
Text Notes 8500 5900 0 100 ~ 20
NEXT CAD STEP
Text Notes 8500 6150 0 60 ~ 12
Replace functional blocks with exact symbols/footprints after CAD library validation.
Text Notes 8500 6300 0 60 ~ 12
Then annotate, ERC, assign footprints, layout, DRC, Gerber inspection.
$EndSCHEMATC
