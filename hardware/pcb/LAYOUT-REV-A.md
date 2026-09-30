# PSN-Presepe PCB — piano meccanico/layout Rev A

## Forma preliminare

Scheda rettangolare larga, orientata in orizzontale.

- Mega 2560 nella metà sinistra, USB accessibile dal bordo esterno.
- comandi utente e bassa tensione lungo bordo sinistro/inferiore;
- RGB e WS2811 lungo bordo inferiore;
- driver relè al centro;
- 16 relè in due file da 8;
- morsetti COM/NO/NC lungo il bordo destro, nella zona 230 V;
- barriera SELV/rete continua e chiaramente serigrafata.

Dimensioni NON ancora congelate: verranno determinate dal footprint reale dei 16 relè e dalla distanza necessaria per i 16 morsetti.

## Zone

[ USB ]
+-----------------------------------------------------------------------+
| MEGA 2560       | DRIVER/BOBINE       | RELÈ       | 230 V TERMINALS |
|                 | U1 U2               | K1..K8     | JR1..JR8        |
| OLED BTN POT    |                     | K9..K16    | JR9..JR16       |
|                 |                     |            |                 |
| RGB / WS2811 / 12V                    |            |                 |
+-----------------------------------------------------------------------+
                                         ^ barriera isolamento ^

## Regole preliminari PCB

- 2 layer FR-4; valutare 1.6 mm / 1 oz come base solo dopo calcolo piste.
- piano GND esclusivamente nella zona SELV.
- nessun copper pour nella barriera.
- nessun rame SELV sotto i contatti dei relè.
- USB e jack/alimentazione del Mega devono restare accessibili.
- fori di fissaggio agli angoli e almeno un supporto nella zona centrale se la scheda diventa molto larga.
- serigrafia lato rete: simbolo alta tensione + “230 VAC”.
- ogni morsetto relè: numero canale + COM / NO / NC.
- ogni morsetto bassa tensione: tensione e polarità chiaramente indicate.

## Scelta importante

Non si porta una L/N comune sulla PCB nella Rev A. Ogni relè espone **tre contatti completamente indipendenti COM/NO/NC**. Questo evita una barra di distribuzione 230 V condivisa sulla scheda e mantiene la PCB utilizzabile anche come semplice contatto pulito.
