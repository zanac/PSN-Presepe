# PSN-Presepe PCB — layout meccanico Rev A

## Riferimenti meccanici verificati

- Arduino Mega 2560 Rev3: circa 101.52 x 53.3 mm; usare il CAD/meccanica ufficiale Arduino per posizione definitiva di header e fori.
- Omron G5Q-1: ingombro massimo circa 20.3 x 10.3 mm; footprint a 5 pin ricavato esclusivamente dal disegno PCB ufficiale Omron.

## Architettura meccanica

La PCB è una **carrier/shield estesa**: il Mega 2560 si innesta direttamente tramite header femmina e resta completamente sostituibile. USB e connettore di alimentazione del Mega devono rimanere accessibili.

### Outline di lavoro Rev A

Prima ipotesi da validare nel CAD:
- larghezza: 220 mm
- altezza: 120 mm
- FR-4 1.6 mm
- 2 layer

L'outline è volutamente abbondante: verrà ridotto solo dopo placement reale e controllo delle distanze.

## Zone funzionali

Vista dall'alto:

```
  BORDO SINISTRO / USB MEGA
  +----------------------------------------------------------------------------------+
  |                                                                                  |
  |   ARDUINO MEGA 2560             SELV / DRIVER             RELAY CONTACT SIDE      |
  |   ~101.5 x 53.3                 U1/U2                     K1..K8   JR1..JR8       |
  |                                                           K9..K16  JR9..JR16      |
  |   B10K   BUZZER                                                                  |
  |                                                                                  |
  | J1  OLED  START NEXT TEST | CIELO | TRAMONTO | ALBA | STELLE | CASETTE           |
  +----------------------------------------------------------------------------------+
       BORDO BASSA TENSIONE                                  BORDO MORSETTI RELÈ
```

## Mega 2560

- orientamento con USB rivolto verso il bordo sinistro;
- nessun componente alto davanti a USB, jack o pulsante RESET;
- header shield posizionati usando geometria ufficiale, non una griglia 2.54 mm approssimata;
- ricordare l'offset non standard fra alcuni header Arduino;
- +12V_BUS raggiunge il percorso VIN del Mega, mai il pin +5V;
- +5V_MEGA viene usato solo come alimentazione logica per OLED/B10K.

## Zona RGB / bassa tensione

I 9 IRLZ44N vengono raggruppati in tre blocchi:
1. CIELO R/G/B
2. TRAMONTO R/G/B
3. ALBA R/G/B

Ogni blocco è vicino al relativo morsetto +12V/R/G/B per mantenere corti i percorsi di corrente.

Sul bordo inferiore, da sinistra verso destra:
- J1 +12V/GND
- J_OLED
- J_START
- J_NEXT
- J_TEST
- J_CIELO
- J_TRAMONTO
- J_ALBA
- J_STELLE
- J_CASETTE

STELLE e CASETTE hanno DATA diretto rispettivamente da D5 e D8: nessuna resistenza/buffer onboard.

## Zona relè

16 G5Q-1 in due file da 8.

Orientamento preliminare: asse lungo del relè verso il relativo morsetto, così le piste COM/NO/NC rimangono corte e non devono attraversare la zona bobine.

Ogni relè termina esclusivamente nel proprio morsetto:
`COM | NO | NC`

Non esistono bus L/N o ponti 230 V sulla PCB.

U1 e U2 (ULN2803C) restano sul lato bobine/SELV, fra Mega e banco relè.

## Separazione

Anche se la PCB non distribuisce la rete, i morsetti COM/NO/NC possono essere collegati esternamente a 230 VAC.

Pertanto:
- zona contatti trattata come potenzialmente a tensione di rete;
- nessun piano GND SELV sotto la zona contatti;
- nessuna pista 5/12 V attraversa la zona contatti;
- barriera continua tra lato bobine/SELV e routing dei contatti;
- eventuali slot saranno definiti dopo placement del footprint esatto;
- valori definitivi di creepage/clearance vengono impostati prima del routing finale.

## Fori di fissaggio

Prevedere almeno:
- 4 fori agli angoli della carrier;
- supporto meccanico vicino al Mega;
- almeno 2 supporti aggiuntivi nella metà relè se l'outline resta vicino a 220 mm.

Posizioni definitive solo dopo placement.

## Stato

Questo documento congela l'architettura e l'outline iniziale, non le coordinate finali. Il prossimo passaggio CAD è creare il footprint shield Mega dal riferimento ufficiale e il footprint G5Q-1 dal datasheet, quindi posizionare realmente i 16 relè e i morsetti e ridimensionare l'outline.
