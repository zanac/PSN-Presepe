/*
  PresepeController - FASE 1 v2
  Arduino Mega 2560

  USCITE
    D2 = Cielo RGB Rosso
    D3 = Cielo RGB Verde
    D4 = Cielo RGB Blu
    D5 = DATA stelle WS2811 (50 pixel, 12 V)
    D6 = Buzzer piezo passivo opzionale
    D10/D11/D12 = RGB laterale SINISTRA / TRAMONTO (R/G/B)
    D44/D45/D46 = RGB laterale DESTRA / ALBA (R/G/B)

  COMANDI DEFINITIVI
    D22 = START/STOP (pulsante NO verso GND)
    D23 = AVANTI     (pulsante NO verso GND)
    D24 = TEST       (pulsante NO verso GND)
    A0  = Potenziometro lineare B10K

  POTENZIOMETRO
    estremo 1 -> +5V
    cursore  -> A0
    estremo 3 -> GND

  CICLO
    GIORNO -> TRAMONTO -> CREPUSCOLO -> NOTTE -> ALBA -> GIORNO

  Potenziometro:
    ciclo completo regolabile da 1 a 6 minuti.

  Serial Monitor: 115200 baud

  STELLE WS2811:
    +12V -> alimentatore 12 V protetto
    GND  -> 0 V alimentatore E GND Arduino (massa comune)
    DATA -> D5 tramite resistenza 330-470 ohm
    MOSFET #1 canale 4 libero

  NOTA MOSFET:
  Quando avremo verificato il B0GXDL8N7D reale, se gli ingressi
  risultassero active-low basta impostare PWM_INVERTED = true.
*/

#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ============================================================
// CONFIGURAZIONE PIN
// ============================================================

const uint8_t PIN_CIELO_R = 2;
const uint8_t PIN_CIELO_G = 3;
const uint8_t PIN_CIELO_B = 4;
const uint8_t PIN_STELLE_DATA = 5;
const uint8_t PIN_BUZZER = 6; // piezo passivo opzionale: se assente il firmware funziona normalmente

// Strisce RGB laterali da 1 m, dedicate agli effetti direzionali.
// Sinistra = tramonto; destra = alba. D13 resta PWM libero.
const uint8_t PIN_TRAMONTO_R = 10;
const uint8_t PIN_TRAMONTO_G = 11;
const uint8_t PIN_TRAMONTO_B = 12;
const uint8_t PIN_ALBA_R = 44;
const uint8_t PIN_ALBA_G = 45;
const uint8_t PIN_ALBA_B = 46;
const uint16_t NUM_STELLE = 50;
const uint8_t STELLE_ATTIVE = 20;
const uint8_t STELLE_TREMOLANTI = STELLE_ATTIVE; // tutte le 20 stelle attive scintillano
Adafruit_NeoPixel stelle(NUM_STELLE, PIN_STELLE_DATA, NEO_GRB + NEO_KHZ800);

const uint8_t PIN_START = 22;
const uint8_t PIN_NEXT  = 23;
const uint8_t PIN_TEST  = 24;
const uint8_t PIN_POT   = A0;


// -----------------------------------------------------------------------------
// RELÈ: 4 moduli x 4 canali = 16 uscite ON/OFF predisposte.
// D25-D40 sono riservati al cablaggio IN1..IN4 dei quattro moduli.
// La logica scenografica usa una tabella di schedulazione per fase/percentuale.
// -----------------------------------------------------------------------------
const uint8_t PIN_RELE[16] = {
  25, 26, 27, 28,
  29, 30, 31, 32,
  33, 34, 35, 36,
  37, 38, 39, 40
};

const bool PWM_INVERTED = false;
const bool RELE_ACTIVE_LOW = false; // Wokwi: HIGH=ON; verificare i moduli reali prima del collegamento

// OLED ELEGOO EL-SM-008, 128x64, I2C 0x3C.
// Il display e' opzionale: se assente il presepe continua normalmente.
const uint8_t OLED_ADDR = 0x3C;
const uint8_t OLED_W = 128;
const uint8_t OLED_H = 64;
Adafruit_SSD1306 display(OLED_W, OLED_H, &Wire, -1);
bool oledPresente = false;
unsigned long oledPopupFino = 0;
enum OledPopup { OLED_NESSUNO, OLED_PAUSA, OLED_RIPRESA, OLED_AVANTI, OLED_TEST, OLED_VELOCITA };
OledPopup oledPopup = OLED_NESSUNO;
int ultimoPotOled = -1;
const int POT_POPUP_DELTA = 10;
const unsigned long OLED_POPUP_MS = 1800UL;

// Durata ciclo regolabile con il potenziometro
const unsigned long MIN_CYCLE_MS = 1UL * 60UL * 1000UL;
const unsigned long MAX_CYCLE_MS = 6UL * 60UL * 1000UL;

// Fasi in percentuale
const float P_TRAMONTO = 35.0f;
const float P_CREPU    = 45.0f;
const float P_NOTTE    = 50.0f;
const float P_ALBA     = 80.0f;
// ALBA occupa l'ultimo 20% del ciclo e termina direttamente nel nuovo GIORNO.

const unsigned long DEBOUNCE_MS = 40;
const unsigned long DEBUG_INTERVAL_MS = 5000UL;

// ============================================================
// STATO
// ============================================================

enum Fase {
  GIORNO,
  TRAMONTO,
  CREPUSCOLO,
  NOTTE,
  ALBA
};

// ============================================================
// SCHEDULAZIONE RELÈ
// ============================================================
// Ogni riga: { FASE, RELÈ, STATO, % DELLA FASE }.
// La tabella descrive eventi persistenti: quando un evento viene raggiunto,
// il relè mantiene lo stato fino al successivo evento che lo riguarda.
//
// Esempio attuale:
// - Grp_01_03 si accende al 30% del TRAMONTO.
// - Grp_01_03 si spegne al 50% della NOTTE.
//
// Per aggiungere la schedulazione definitiva sarà sufficiente modificare
// questo array. Le percentuali valide sono 0..100.
enum ReleNome : uint8_t {
  Grp_01_01 = 0, Grp_01_02, Grp_01_03, Grp_01_04,
  Grp_02_01,     Grp_02_02, Grp_02_03, Grp_02_04,
  Grp_03_01,     Grp_03_02, Grp_03_03, Grp_03_04,
  Grp_04_01,     Grp_04_02, Grp_04_03, Grp_04_04
};

struct EventoRele {
  Fase fase;
  ReleNome rele;
  bool acceso;
  uint8_t percentualeFase;
};

const EventoRele SCHEDULAZIONE_RELE[] = {
  { TRAMONTO, Grp_01_03, true,  30 },
  { NOTTE,    Grp_01_03, false, 50 }
};

const uint8_t NUM_EVENTI_RELE =
  sizeof(SCHEDULAZIONE_RELE) / sizeof(SCHEDULAZIONE_RELE[0]);

bool running = true;
bool testInCorso = false;
uint8_t testIndice = 0;
bool testEraInMarcia = false;
unsigned long testPausaMs = 0;

unsigned long cycleStartMs = 0;
unsigned long pauseStartedMs = 0;
unsigned long lastDebugMs = 0;

// Ultimi valori RGB realmente richiesti alle tre strisce.
// Servono anche per mostrarli sul display quando il ciclo viene messo in pausa.
uint8_t rgbCieloR = 0, rgbCieloG = 0, rgbCieloB = 0;
uint8_t rgbTramontoR = 0, rgbTramontoG = 0, rgbTramontoB = 0;
uint8_t rgbAlbaR = 0, rgbAlbaG = 0, rgbAlbaB = 0;

// debounce pulsanti
bool lastStartRead = HIGH, stableStart = HIGH;
bool lastNextRead  = HIGH, stableNext  = HIGH;
bool lastTestRead  = HIGH, stableTest  = HIGH;
unsigned long dbStartMs = 0, dbNextMs = 0, dbTestMs = 0;

// ============================================================
// PWM
// ============================================================

void pwmWrite(uint8_t pin, uint8_t value) {
  analogWrite(pin, PWM_INVERTED ? (255 - value) : value);
}

void setCielo(uint8_t r, uint8_t g, uint8_t b) {
  rgbCieloR = r; rgbCieloG = g; rgbCieloB = b;
  pwmWrite(PIN_CIELO_R, r);
  pwmWrite(PIN_CIELO_G, g);
  pwmWrite(PIN_CIELO_B, b);
}

void setTramonto(uint8_t r, uint8_t g, uint8_t b) {
  rgbTramontoR = r; rgbTramontoG = g; rgbTramontoB = b;
  pwmWrite(PIN_TRAMONTO_R, r);
  pwmWrite(PIN_TRAMONTO_G, g);
  pwmWrite(PIN_TRAMONTO_B, b);
}

void setAlba(uint8_t r, uint8_t g, uint8_t b) {
  rgbAlbaR = r; rgbAlbaG = g; rgbAlbaB = b;
  pwmWrite(PIN_ALBA_R, r);
  pwmWrite(PIN_ALBA_G, g);
  pwmWrite(PIN_ALBA_B, b);
}

// ============================================================
// STELLE WS2811
// ============================================================
// Effetto naturale: ogni notte viene generato un cielo diverso.
// Ogni notte vengono scelte casualmente 20 stelle su 50, con luminosita'
// massime differenti. Compaiono nel crepuscolo, restano attive di notte e
// scompaiono durante l'alba. Tutte le 20 hanno variazioni asincrone individuali.

uint8_t stellaLum[NUM_STELLE];
uint8_t stellaOrdine[NUM_STELLE];
bool stellaTwinkle[NUM_STELLE];
bool cieloGenerato = false;
Fase ultimaFaseStelle = GIORNO;

void generaCieloStellato() {
  // Ogni notte scegliamo casualmente solo 20 delle 50 stelle fisiche.
  // Le altre 30 restano completamente spente.
  for (uint16_t i = 0; i < NUM_STELLE; i++) {
    stellaLum[i] = random(22, 76); // luce volutamente tenue: niente effetto "lampadina"
    stellaOrdine[i] = i;
    stellaTwinkle[i] = false;
  }

  // Fisher-Yates su tutti i 50 pixel: i primi 20 saranno quelli attivi.
  for (int i = NUM_STELLE - 1; i > 0; i--) {
    int j = random(i + 1);
    uint8_t tmp = stellaOrdine[i];
    stellaOrdine[i] = stellaOrdine[j];
    stellaOrdine[j] = tmp;
  }

  // Tutte le 20 stelle attive ricevono il comportamento variabile.
  // Il piccolo shuffle assegna il flag alle stelle gia' selezionate casualmente;
  // STELLE_TREMOLANTI coincide attualmente con STELLE_ATTIVE, quindi sono tutte.
  uint8_t candidati[STELLE_ATTIVE];
  for (uint8_t i = 0; i < STELLE_ATTIVE; i++) candidati[i] = i;
  for (int i = STELLE_ATTIVE - 1; i > 0; i--) {
    int j = random(i + 1);
    uint8_t tmp = candidati[i];
    candidati[i] = candidati[j];
    candidati[j] = tmp;
  }
  for (uint8_t n = 0; n < STELLE_TREMOLANTI; n++)
    stellaTwinkle[stellaOrdine[candidati[n]]] = true;

  cieloGenerato = true;
}

void mostraStelle(float livello) {
  livello = constrain(livello, 0.0f, 1.0f);
  stelle.clear();

  // Durante il crepuscolo entrano progressivamente le 20 stelle scelte;
  // durante l'alba scompaiono progressivamente. Mai piu' di 20 accese.
  uint8_t visibili = (uint8_t)(livello * STELLE_ATTIVE + 0.5f);
  if (visibili > STELLE_ATTIVE) visibili = STELLE_ATTIVE;

  for (uint8_t pos = 0; pos < visibili; pos++) {
    uint8_t i = stellaOrdine[pos];
    float locale = livello * STELLE_ATTIVE - pos;
    locale = constrain(locale, 0.0f, 1.0f);

    uint16_t v = (uint16_t)(stellaLum[i] * locale);

    // Ogni stella attiva segue autonomamente un ciclo di luminosita':
    // livello pieno -> dissolvenza a zero -> pausa spenta -> riaccensione.
    // Durate e offset differenti evitano che le 20 stelle si muovano insieme.
    if (stellaTwinkle[i] && v > 5) {
      // Durata pseudo-casuale e stabile per ogni pixel: circa 3,2-6,1 s.
      // Anche l'offset e' diverso per ogni stella, cosi' partono vicine ma non insieme
      // e col tempo si sfasano sempre di piu'.
      const unsigned long periodo = 3200UL + ((unsigned long)(i * 37U) % 30UL) * 100UL;
      const unsigned long offset = ((unsigned long)(i * 173U) % 900UL);
      const unsigned long faseMs = (millis() + offset) % periodo;
      const unsigned long pTw = (faseMs * 100UL) / periodo;
      uint8_t fattore = 100;

      if (pTw < 45) {
        fattore = 100;                              // piena luminosita'
      } else if (pTw < 55) {
        fattore = (uint8_t)((55UL - pTw) * 10UL);  // 100 -> 0
      } else if (pTw < 80) {
        fattore = 0;                                // SPENTA per il 25% del ciclo
      } else if (pTw < 90) {
        fattore = (uint8_t)((pTw - 80UL) * 10UL);  // 0 -> 100
      } else {
        fattore = 100;
      }

      // A fattore zero scriviamo esplicitamente nero sul pixel.
      if (fattore == 0) {
        v = 0;
      } else {
        v = (v * fattore) / 100U;
      }
    }

    // Bianco caldo tenue.
    stelle.setPixelColor(i, stelle.Color(
      (uint8_t)v,
      (uint8_t)((v * 72U) / 100U),
      (uint8_t)((v * 38U) / 100U)
    ));
  }
  stelle.show();
}

void setStelle(uint8_t value) {
  if (!cieloGenerato) generaCieloStellato();
  mostraStelle(value / 255.0f);
}

void tuttoSpento() {
  setCielo(0, 0, 0);
  setTramonto(0, 0, 0);
  setAlba(0, 0, 0);
  setStelle(0);
}

// ============================================================
// TEMPO / POTENZIOMETRO
// ============================================================

unsigned long durataCiclo() {
  int raw = analogRead(PIN_POT);

  // Ruotando verso il massimo elettrico di A0:
  // ciclo piu' lungo. A0=0 -> 1 minuto (default se il cursore e' a GND), A0=1023 -> 6 minuti.
  return map(raw, 0, 1023, MIN_CYCLE_MS, MAX_CYCLE_MS);
}

float percentualeCiclo(unsigned long durata) {
  unsigned long riferimento = running ? millis() : pauseStartedMs;
  unsigned long elapsed = riferimento - cycleStartMs;
  elapsed %= durata;
  return (elapsed * 100.0f) / durata;
}

float progresso(float p, float inizio, float fine) {
  if (fine <= inizio) return 0.0f;
  return constrain((p - inizio) / (fine - inizio), 0.0f, 1.0f);
}

uint8_t interpola8(uint8_t da, uint8_t a, float t) {
  t = constrain(t, 0.0f, 1.0f);
  return (uint8_t)(da + ((float)a - da) * t);
}

// ============================================================
// FASI
// ============================================================

Fase faseDaPercentuale(float p) {
  if (p < P_TRAMONTO) return GIORNO;
  if (p < P_CREPU)    return TRAMONTO;
  if (p < P_NOTTE)    return CREPUSCOLO;
  if (p < P_ALBA)     return NOTTE;
  return ALBA;
}

const char* nomeFase(Fase f) {
  switch (f) {
    case GIORNO:        return "GIORNO";
    case TRAMONTO:      return "TRAMONTO";
    case CREPUSCOLO:    return "CREPUSCOLO";
    case NOTTE:         return "NOTTE";
    case ALBA:          return "ALBA";
  }
  return "?";
}

float inizioFase(Fase f) {
  switch (f) {
    case GIORNO:        return 0.0f;
    case TRAMONTO:      return P_TRAMONTO;
    case CREPUSCOLO:    return P_CREPU;
    case NOTTE:         return P_NOTTE;
    case ALBA:          return P_ALBA;
  }
  return 0.0f;
}

Fase faseSuccessiva(Fase f) {
  switch (f) {
    case GIORNO:        return TRAMONTO;
    case TRAMONTO:      return CREPUSCOLO;
    case CREPUSCOLO:    return NOTTE;
    case NOTTE:         return ALBA;
    case ALBA:          return GIORNO;
  }
  return GIORNO;
}

float fineFase(Fase f) {
  switch (f) {
    case GIORNO:     return P_TRAMONTO;
    case TRAMONTO:   return P_CREPU;
    case CREPUSCOLO: return P_NOTTE;
    case NOTTE:      return P_ALBA;
    case ALBA:       return 100.0f;
  }
  return 100.0f;
}

uint8_t indiceFase(Fase f) {
  return (uint8_t)f;
}

void scriviRele(uint8_t indice, bool acceso) {
  if (indice >= 16) return;
  digitalWrite(PIN_RELE[indice],
               acceso ? (RELE_ACTIVE_LOW ? LOW : HIGH)
                      : (RELE_ACTIVE_LOW ? HIGH : LOW));
}

// Ricostruisce lo stato dei 16 relè direttamente dalla posizione corrente
// del ciclo. Questo rende la schedulazione deterministica anche dopo AVANTI,
// pausa/ripresa o variazioni della durata del ciclo.
void aggiornaReleSchedulati(float p) {
  Fase faseAttuale = faseDaPercentuale(p);
  float inizio = inizioFase(faseAttuale);
  float fine = fineFase(faseAttuale);
  float pctFase = (fine > inizio)
                    ? constrain((p - inizio) * 100.0f / (fine - inizio), 0.0f, 100.0f)
                    : 0.0f;

  for (uint8_t r = 0; r < 16; r++) {
    bool stato = false;

    // Trova l'ultimo evento applicabile al relè dall'inizio del ciclo
    // fino alla posizione corrente.
    for (uint8_t i = 0; i < NUM_EVENTI_RELE; i++) {
      const EventoRele &ev = SCHEDULAZIONE_RELE[i];
      if ((uint8_t)ev.rele != r) continue;

      bool fasePassata = indiceFase(ev.fase) < indiceFase(faseAttuale);
      bool faseCorrenteRaggiunta =
        ev.fase == faseAttuale && pctFase >= ev.percentualeFase;

      if (fasePassata || faseCorrenteRaggiunta)
        stato = ev.acceso;
    }

    scriviRele(r, stato);
  }
}

// ============================================================
// OLED
// ============================================================

void oledMostraPopup(OledPopup tipo) {
  if (!oledPresente) return;
  oledPopup = tipo;
  oledPopupFino = millis() + OLED_POPUP_MS;
}

float percentualeFase(float p, Fase f) {
  float a = inizioFase(f), b = 100.0f;
  switch (f) {
    case GIORNO: b = P_TRAMONTO; break;
    case TRAMONTO: b = P_CREPU; break;
    case CREPUSCOLO: b = P_NOTTE; break;
    case NOTTE: b = P_ALBA; break;
    case ALBA: b = 100.0f; break;
  }
  return constrain((p-a)*100.0f/(b-a),0.0f,100.0f);
}

void oledCentro(const __FlashStringHelper *s, int y, uint8_t size=1) {
  display.setTextSize(size);
  int16_t x1,y1; uint16_t w,h;
  display.getTextBounds(s,0,y,&x1,&y1,&w,&h);
  display.setCursor((OLED_W-w)/2,y);
  display.print(s);
}

void mostraOledTest() {
  if (!oledPresente) return;
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0,0); display.print(F("MODALITA' TEST"));
  display.setCursor(0,14); display.print(F("Test ")); display.print(testIndice + 1); display.print(F("/30"));
  display.setCursor(0,30);
  if (testIndice < 14) {
    switch (testIndice) {
      case 0: display.print(F("CIELO ROSSO")); break;
      case 1: display.print(F("CIELO VERDE")); break;
      case 2: display.print(F("CIELO BLU")); break;
      case 3: display.print(F("TRAMONTO ROSSO")); break;
      case 4: display.print(F("TRAMONTO VERDE")); break;
      case 5: display.print(F("TRAMONTO BLU")); break;
      case 6: display.print(F("ALBA ROSSO")); break;
      case 7: display.print(F("ALBA VERDE")); break;
      case 8: display.print(F("ALBA BLU")); break;
      case 9: display.print(F("STELLE ROSSE")); break;
      case 10: display.print(F("STELLE VERDI")); break;
      case 11: display.print(F("STELLE BLU")); break;
      case 12: display.print(F("STELLE WS2811")); break;
      case 13: display.print(F("TUTTO INSIEME")); break;
    }
  } else {
    uint8_t n = testIndice - 14;
    uint8_t gruppo = n / 4 + 1;
    uint8_t rele = n % 4 + 1;
    display.print(F("Grp_"));
    if (gruppo < 10) display.print('0');
    display.print(gruppo);
    display.print('_');
    if (rele < 10) display.print('0');
    display.print(rele);
  }
  display.setCursor(0,48); display.print(F("TEST=avanti START=esci"));
  display.display();
}

void mostraOledRgbPausa(float p) {
  if (!oledPresente) return;
  Fase f = faseDaPercentuale(p);
  int pf = (int)(percentualeFase(p, f) + 0.5f);

  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0,0);
  display.print(F("PAUSA "));
  display.print(nomeFase(f));
  display.print(' ');
  display.print(pf);
  display.print('%');

  display.setCursor(0,16);
  display.print(F("C "));
  display.print(rgbCieloR); display.print(',');
  display.print(rgbCieloG); display.print(',');
  display.print(rgbCieloB);

  display.setCursor(0,32);
  display.print(F("T "));
  display.print(rgbTramontoR); display.print(',');
  display.print(rgbTramontoG); display.print(',');
  display.print(rgbTramontoB);

  display.setCursor(0,48);
  display.print(F("A "));
  display.print(rgbAlbaR); display.print(',');
  display.print(rgbAlbaG); display.print(',');
  display.print(rgbAlbaB);

  display.display();
}

void aggiornaOled(unsigned long durata, float p) {
  if (!oledPresente) return;
  static unsigned long ultimoRefresh=0;
  if (millis()-ultimoRefresh < 120) return;
  ultimoRefresh=millis();

  // In pausa i valori RGB restano visibili stabilmente, così possono essere
  // annotati e riutilizzati per tarare i colori della scenografia.
  if (!running && !testInCorso) {
    mostraOledRgbPausa(p);
    return;
  }

  if (oledPopup != OLED_NESSUNO && (long)(millis()-oledPopupFino)>=0) oledPopup=OLED_NESSUNO;
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);

  if (oledPopup != OLED_NESSUNO) {
    display.setTextSize(2);
    display.setCursor(8,8);
    switch(oledPopup) {
      case OLED_PAUSA: display.print(F("PAUSA")); break;
      case OLED_RIPRESA: display.print(F("RIPRESA")); break;
      case OLED_AVANTI: display.print(F("AVANTI")); break;
      case OLED_TEST: display.print(F("TEST")); break;
      case OLED_VELOCITA: display.print(F("VELOCITA")); break;
      default: break;
    }
    display.setTextSize(1);
    display.setCursor(8,38);
    if (oledPopup==OLED_VELOCITA) {
      display.print(F("Ciclo: ")); display.print(durata/60000UL); display.print(F(" min"));
    } else if (oledPopup==OLED_AVANTI) {
      display.print(F("Fase: ")); display.print(nomeFase(faseDaPercentuale(p)));
    } else if (oledPopup==OLED_TEST) {
      display.print(F("Test uscite in corso"));
    } else {
      display.print(running ? F("Ciclo in esecuzione") : F("Ciclo fermo"));
    }
  } else {
    Fase f=faseDaPercentuale(p);
    int pf=(int)(percentualeFase(p,f)+0.5f);
    display.setTextSize(1);
    display.setCursor(0,0); display.print(F("PSN-PRESEPE"));
    display.setCursor(0,14); display.print(nomeFase(f));
    display.setCursor(94,14); display.print(pf); display.print('%');
    display.drawRect(0,27,128,11,SSD1306_WHITE);
    int fill=(pf*124)/100;
    if(fill>0) display.fillRect(2,29,fill,7,SSD1306_WHITE);
    display.setCursor(0,47);
    display.print(running ? F("RUN ") : F("PAUSA "));
    display.print(F("Ciclo ")); display.print(durata/60000UL); display.print(F(" min"));
  }
  display.display();
}

bool inizializzaOled() {
  Wire.begin();
  Wire.beginTransmission(OLED_ADDR);
  if (Wire.endTransmission()!=0) return false;
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) return false;
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  // Startup splash: PSN-Presepe! by Vanni
  display.setCursor(27,18); display.print(F("PSN-Presepe!"));
  display.setCursor(30,36); display.print(F("by Vanni 015"));
  display.display();
  delay(3000);
  return true;
}

void saltaAPercentuale(float p) {
  unsigned long durata = durataCiclo();
  unsigned long offset = (unsigned long)(durata * (p / 100.0f));

  cycleStartMs = millis() - offset;

  if (!running)
    pauseStartedMs = millis();
}

void faseAvanti() {
  unsigned long durata = durataCiclo();
  float p = percentualeCiclo(durata);
  Fase nuova = faseSuccessiva(faseDaPercentuale(p));

  saltaAPercentuale(inizioFase(nuova));

  Serial.print(F("AVANTI -> "));
  Serial.println(nomeFase(nuova));
  oledMostraPopup(OLED_AVANTI);
}

// ============================================================
// SCENA
// ============================================================

void aggiornaScena(float p) {
  Fase fase = faseDaPercentuale(p);

  // Genera una nuova disposizione a ogni ingresso nel crepuscolo.
  if (fase == CREPUSCOLO && ultimaFaseStelle != CREPUSCOLO) {
    generaCieloStellato();
  }
  ultimaFaseStelle = fase;

  uint8_t r = 0, g = 0, b = 0, livelloStelle = 0;
  uint8_t tr = 0, tg = 0, tb = 0; // luce laterale tramonto
  uint8_t ar = 0, ag = 0, ab = 0; // luce laterale alba

  switch (fase) {

    case GIORNO:
      r = 255;
      g = 210;
      b = 145;
      livelloStelle = 0;
      break;

    case TRAMONTO: {
      float t = progresso(p, P_TRAMONTO, P_CREPU);

      r = 255;
      g = interpola8(210, 65, t);
      b = interpola8(145, 15, t);
      livelloStelle = 0;

      // La luce laterale sinistra entra gradualmente e crea uno
      // spostamento della luce verso il lato del tramonto.
      // Sale, raggiunge il massimo a meta' fase e poi cala dolcemente.
      {
        float arco = 1.0f - fabs(2.0f * t - 1.0f);
        tr = (uint8_t)(255.0f * arco);
        tg = (uint8_t)(72.0f * arco);
        tb = (uint8_t)(12.0f * arco);
      }
      break;
    }

    case CREPUSCOLO: {
      float t = progresso(p, P_CREPU, P_NOTTE);

      r = interpola8(255, 8, t);
      g = interpola8(65, 12, t);
      b = interpola8(15, 55, t);
      livelloStelle = interpola8(0, 235, t);
      break;
    }

    case NOTTE:
      r = 8;
      g = 12;
      b = 55;
      livelloStelle = 235;
      break;

    case ALBA: {
      float t = progresso(p, P_ALBA, 100.0f);

      r = interpola8(8, 255, t);
      g = interpola8(12, 210, t);
      b = interpola8(55, 145, t);
      livelloStelle = interpola8(235, 0, t);

      // Alba direzionale dalla striscia destra: sale dolcemente nella
      // prima parte della fase, poi cala progressivamente fino a ZERO.
      // Negli ultimi istanti la dissolvenza rallenta (smoothstep), cosi'
      // il passaggio ALBA -> GIORNO non produce uno stacco visibile.
      {
        float arco;
        if (t < 0.35f) {
          float x = t / 0.35f;
          x = x * x * (3.0f - 2.0f * x);
          arco = x;
        } else {
          float x = (t - 0.35f) / 0.65f;
          x = x * x * (3.0f - 2.0f * x);
          arco = 1.0f - x;
        }
        ar = (uint8_t)(255.0f * arco);
        ag = (uint8_t)(135.0f * arco);
        ab = (uint8_t)(45.0f * arco);
      }
      break;
    }

  }

  setCielo(r, g, b);
  setTramonto(tr, tg, tb);
  setAlba(ar, ag, ab);
  setStelle(livelloStelle);
}

// ============================================================
// PULSANTI
// ============================================================

bool pulsantePremuto(uint8_t pin,
                     bool &lastRead,
                     bool &stable,
                     unsigned long &lastChange) {

  bool lettura = digitalRead(pin);
  unsigned long now = millis();

  if (lettura != lastRead) {
    lastRead = lettura;
    lastChange = now;
  }

  if ((now - lastChange) >= DEBOUNCE_MS && lettura != stable) {
    stable = lettura;

    if (stable == LOW)
      return true;
  }

  return false;
}

void toggleStartStop() {
  if (testInCorso) {
    tuttoSpento();
    spegniRele();
    testInCorso = false;
    testIndice = 0;

    // Il tempo passato in TEST non deve far avanzare il ciclo.
    if (testEraInMarcia) {
      cycleStartMs += millis() - testPausaMs;
      running = true;
    } else {
      pauseStartedMs = millis();
      running = false;
    }

    Serial.println(F("USCITA MODALITA' TEST"));
    oledPopup = OLED_NESSUNO;
    float p = percentualeCiclo(durataCiclo());
    aggiornaScena(p);
    aggiornaReleSchedulati(p);
    aggiornaOled(durataCiclo(), p);
    return;
  }

  if (running) {
    pauseStartedMs = millis();
    running = false;
    Serial.println(F("PAUSA"));
    oledPopup = OLED_NESSUNO;
  } else {
    unsigned long durataPausa = millis() - pauseStartedMs;

    // Sposta l'origine del ciclo per riprendere esattamente
    // dal punto in cui era stato fermato.
    cycleStartMs += durataPausa;

    running = true;
    Serial.println(F("RIPRESA"));
    oledMostraPopup(OLED_RIPRESA);
  }
}

// ============================================================
// TEST
// ============================================================

void spegniRele() {
  for (uint8_t i = 0; i < 16; i++)
    scriviRele(i, false);
}

void accendiRele(uint8_t indice) {
  spegniRele();
  if (indice < 16)
    scriviRele(indice, true);
}

void applicaTestCorrente() {
  tuttoSpento();
  spegniRele();

  if (testIndice >= 14) {
    uint8_t n = testIndice - 14;
    accendiRele(n);
    uint8_t gruppo = n / 4 + 1;
    uint8_t rele = n % 4 + 1;
    Serial.print(F("TEST "));
    Serial.print(testIndice + 1);
    Serial.print(F("/30 - Grp_0"));
    Serial.print(gruppo);
    Serial.print(F("_0"));
    Serial.println(rele);
    mostraOledTest();
    return;
  }

  switch (testIndice) {
    case 0:
      setCielo(255, 0, 0);
      Serial.println(F("TEST 1/30 - CIELO ROSSO"));
      break;
    case 1:
      setCielo(0, 255, 0);
      Serial.println(F("TEST 2/30 - CIELO VERDE"));
      break;
    case 2:
      setCielo(0, 0, 255);
      Serial.println(F("TEST 3/30 - CIELO BLU"));
      break;
    case 3:
      setTramonto(255, 0, 0);
      Serial.println(F("TEST 4/30 - TRAMONTO ROSSO"));
      break;
    case 4:
      setTramonto(0, 255, 0);
      Serial.println(F("TEST 5/30 - TRAMONTO VERDE"));
      break;
    case 5:
      setTramonto(0, 0, 255);
      Serial.println(F("TEST 6/30 - TRAMONTO BLU"));
      break;
    case 6:
      setAlba(255, 0, 0);
      Serial.println(F("TEST 7/30 - ALBA ROSSO"));
      break;
    case 7:
      setAlba(0, 255, 0);
      Serial.println(F("TEST 8/30 - ALBA VERDE"));
      break;
    case 8:
      setAlba(0, 0, 255);
      Serial.println(F("TEST 9/30 - ALBA BLU"));
      break;
    case 9:
      // Verifica il canale rosso di tutti i 50 pixel WS2811.
      stelle.clear();
      for (uint16_t i = 0; i < NUM_STELLE; i++)
        stelle.setPixelColor(i, stelle.Color(70, 0, 0));
      stelle.show();
      Serial.println(F("TEST 10/30 - STELLE ROSSE"));
      break;
    case 10:
      // Verifica il canale verde di tutti i 50 pixel WS2811.
      stelle.clear();
      for (uint16_t i = 0; i < NUM_STELLE; i++)
        stelle.setPixelColor(i, stelle.Color(0, 70, 0));
      stelle.show();
      Serial.println(F("TEST 11/30 - STELLE VERDI"));
      break;
    case 11:
      // Verifica il canale blu di tutti i 50 pixel WS2811.
      stelle.clear();
      for (uint16_t i = 0; i < NUM_STELLE; i++)
        stelle.setPixelColor(i, stelle.Color(0, 0, 70));
      stelle.show();
      Serial.println(F("TEST 12/30 - STELLE BLU"));
      break;
    case 12:
      // Test scenografico esistente: tutte le 50 stelle in bianco caldo tenue.
      stelle.clear();
      for (uint16_t i = 0; i < NUM_STELLE; i++)
        stelle.setPixelColor(i, stelle.Color(70, 50, 27));
      stelle.show();
      Serial.println(F("TEST 13/30 - TUTTE LE 50 STELLE"));
      break;
    case 13:
      setCielo(120, 90, 70);
      setTramonto(180, 50, 8);
      setAlba(180, 95, 30);
      stelle.clear();
      for (uint16_t i = 0; i < NUM_STELLE; i++)
        stelle.setPixelColor(i, stelle.Color(45, 32, 17));
      stelle.show();
      Serial.println(F("TEST 14/30 - TUTTO INSIEME"));
      break;
  }

  mostraOledTest();
}

void testUscite() {
  if (!testInCorso) {
    testInCorso = true;
    testIndice = 0;
    testEraInMarcia = running;
    testPausaMs = millis();
    running = false;
    oledPopup = OLED_NESSUNO;

    Serial.println();
    Serial.println(F("=== MODALITA' TEST ==="));
    Serial.println(F("TEST = test successivo, START = esci"));
  } else {
    testIndice = (testIndice + 1) % 30;
  }

  applicaTestCorrente();
}

// ============================================================
// DEBUG
// ============================================================

void stampaStato(unsigned long durata, float p) {
  Serial.print(F("Fase: "));
  Serial.print(nomeFase(faseDaPercentuale(p)));

  Serial.print(F(" | "));
  Serial.print(p, 1);
  Serial.print(F("%"));

  Serial.print(F(" | ciclo: "));
  Serial.print(durata / 60000UL);
  Serial.print(F(" min"));

  Serial.print(F(" | A0: "));
  Serial.print(analogRead(PIN_POT));

  Serial.print(F(" | "));
  Serial.println(running ? F("RUN") : F("PAUSA"));
}

// ============================================================
// SEQUENZA DI BOOT / AUTOTEST VISIVO
// ============================================================

const unsigned long BOOT_STEP_MS = 2000UL;
const uint8_t BOOT_STEP_COUNT = 4;

// "Astro del ciel" sul buzzer passivo opzionale, fino a "mite agnello Redentor".
// Tempo volutamente più sostenuto rispetto alla rev.014.
// La melodia può proseguire oltre l'autotest visivo: il boot attende la sua conclusione.
const uint16_t BOOT_MELODY_FREQ[] = {
  392, 440, 392, 330, 392, 440, 392, 330,
  587, 587, 494, 523, 523, 392,
  440, 440, 523, 494, 440, 392, 440, 392, 330,
  440, 440, 523, 494, 440, 392, 440, 392, 330
};
const uint16_t BOOT_MELODY_MS[] = {
  420, 420, 560, 900, 420, 420, 560, 900,
  560, 420, 560, 560, 420, 900,
  420, 420, 560, 420, 420, 560, 420, 420, 900,
  420, 420, 560, 420, 420, 560, 420, 420, 1100
};
const uint8_t BOOT_MELODY_COUNT = sizeof(BOOT_MELODY_FREQ) / sizeof(BOOT_MELODY_FREQ[0]);
int8_t bootNotaCorrente = -1;

void aggiornaMelodiaBoot(unsigned long elapsedTotale) {
  unsigned long limite = 0;
  uint8_t nota = BOOT_MELODY_COUNT;
  for (uint8_t i = 0; i < BOOT_MELODY_COUNT; i++) {
    limite += BOOT_MELODY_MS[i];
    if (elapsedTotale < limite) {
      nota = i;
      break;
    }
  }

  if (nota >= BOOT_MELODY_COUNT) {
    if (bootNotaCorrente != -1) {
      noTone(PIN_BUZZER);
      bootNotaCorrente = -1;
    }
    return;
  }

  if (bootNotaCorrente != (int8_t)nota) {
    tone(PIN_BUZZER, BOOT_MELODY_FREQ[nota]);
    bootNotaCorrente = nota;
  }
}

void mostraOledBoot(const __FlashStringHelper *fase, uint8_t step, unsigned long elapsedStep) {
  if (!oledPresente) return;

  // Avanzamento complessivo sui 4 passi da 2 secondi.
  unsigned long fatto = (unsigned long)step * BOOT_STEP_MS + elapsedStep;
  unsigned long totale = (unsigned long)BOOT_STEP_COUNT * BOOT_STEP_MS;
  uint8_t pct = (uint8_t)min(100UL, (fatto * 100UL) / totale);

  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print(F("PSN-PRESEPE"));
  display.setCursor(0, 15);
  display.print(F("Inizializzazione"));
  display.setCursor(0, 29);
  display.print(fase);
  display.setCursor(102, 29);
  display.print(pct);
  display.print('%');

  display.drawRect(0, 45, 128, 11, SSD1306_WHITE);
  int fill = (pct * 124) / 100;
  if (fill > 0) display.fillRect(2, 47, fill, 7, SSD1306_WHITE);
  display.display();
}

void attesaBoot(const __FlashStringHelper *fase, uint8_t step) {
  unsigned long start = millis();
  unsigned long elapsed = 0;
  do {
    elapsed = millis() - start;
    if (elapsed > BOOT_STEP_MS) elapsed = BOOT_STEP_MS;
    mostraOledBoot(fase, step, elapsed);
    aggiornaMelodiaBoot((unsigned long)step * BOOT_STEP_MS + elapsed);
    delay(40);
  } while (millis() - start < BOOT_STEP_MS);
}

void eseguiSequenzaBoot() {
  Serial.println(F("BOOT: autotest visivo uscite + melodia buzzer opzionale"));

  tuttoSpento();
  spegniRele();

  // 1/4 - ALBA: bianco brillante per 2 secondi.
  setAlba(255, 255, 255);
  attesaBoot(F("ALBA"), 0);
  setAlba(0, 0, 0);

  // 2/4 - CIELO principale: bianco brillante per 2 secondi.
  setCielo(255, 255, 255);
  attesaBoot(F("CIELO"), 1);
  setCielo(0, 0, 0);

  // 3/4 - TRAMONTO: bianco brillante per 2 secondi.
  setTramonto(255, 255, 255);
  attesaBoot(F("TRAMONTO"), 2);
  setTramonto(0, 0, 0);

  // 4/4 - tutte le 50 stelle: bianco brillante per 2 secondi.
  stelle.clear();
  for (uint16_t i = 0; i < NUM_STELLE; i++)
    stelle.setPixelColor(i, stelle.Color(255, 255, 255));
  stelle.show();
  attesaBoot(F("STELLE"), 3);

  // Se la melodia è più lunga degli 8 s dell'autotest visivo, completiamola
  // a uscite spente prima di mostrare PRONTO e avviare il ciclo.
  unsigned long durataMelodia = 0;
  for (uint8_t i = 0; i < BOOT_MELODY_COUNT; i++) durataMelodia += BOOT_MELODY_MS[i];
  unsigned long tMelodia = BOOT_STEP_MS * BOOT_STEP_COUNT;
  while (tMelodia < durataMelodia) {
    aggiornaMelodiaBoot(tMelodia);
    delay(20);
    tMelodia += 20;
  }
  noTone(PIN_BUZZER);
  bootNotaCorrente = -1;

  // Fine autotest: tutto spento prima dell'avvio del normale ciclo GIORNO.
  stelle.clear();
  stelle.show();
  tuttoSpento();
  spegniRele();
  mostraOledBoot(F("PRONTO"), BOOT_STEP_COUNT, 0);
  delay(900);

  Serial.println(F("BOOT: completato"));
}

// ============================================================
// SETUP
// ============================================================

void setup() {
  Serial.begin(115200);
  oledPresente = inizializzaOled();
  randomSeed(analogRead(A15) ^ micros());

  pinMode(PIN_CIELO_R, OUTPUT);
  pinMode(PIN_CIELO_G, OUTPUT);
  pinMode(PIN_CIELO_B, OUTPUT);
  pinMode(PIN_TRAMONTO_R, OUTPUT);
  pinMode(PIN_TRAMONTO_G, OUTPUT);
  pinMode(PIN_TRAMONTO_B, OUTPUT);
  pinMode(PIN_ALBA_R, OUTPUT);
  pinMode(PIN_ALBA_G, OUTPUT);
  pinMode(PIN_ALBA_B, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  noTone(PIN_BUZZER);
  stelle.begin();
  stelle.clear();
  stelle.show();

  pinMode(PIN_START, INPUT_PULLUP);
  pinMode(PIN_NEXT,  INPUT_PULLUP);
  pinMode(PIN_TEST,  INPUT_PULLUP);

  // Inizializza le 16 uscite relè in stato spento.
  // Sono usate sia dalla schedulazione scenografica sia dal test manuale.
  for (uint8_t i = 0; i < 16; i++) {
    digitalWrite(PIN_RELE[i], RELE_ACTIVE_LOW ? HIGH : LOW);
    pinMode(PIN_RELE[i], OUTPUT);
  }

  tuttoSpento();
  spegniRele();

  // Autotest di accensione: ALBA -> GIORNO -> TRAMONTO -> STELLE.
  // Ogni passo dura 2 secondi e l'OLED mostra la progress bar complessiva.
  eseguiSequenzaBoot();

  // Il tempo dell'autotest non fa parte del ciclo scenografico.
  cycleStartMs = millis();

  Serial.println();
  Serial.println(F("========================================"));
  Serial.println(F(" PRESEPE CONTROLLER - FASE 1 v2"));
  Serial.println(F("========================================"));
  Serial.println(F("D2  = RGB Rosso"));
  Serial.println(F("D3  = RGB Verde"));
  Serial.println(F("D4  = RGB Blu"));
  Serial.println(F("D5  = DATA WS2811 (50 stelle)"));
  Serial.println(F("D6  = BUZZER passivo opzionale"));
  Serial.println(F("D10/D11/D12 = RGB SINISTRA / TRAMONTO"));
  Serial.println(F("D44/D45/D46 = RGB DESTRA / ALBA"));
  Serial.println(F("D22 = START/STOP"));
  Serial.println(F("D23 = AVANTI"));
  Serial.println(F("D24 = TEST"));
  Serial.println(F("D20/D21 = OLED I2C 0x3C (opzionale)"));
  Serial.println(oledPresente ? F("OLED: OK") : F("OLED: non presente, continuo senza display"));
  Serial.println(F("A0  = DURATA CICLO 1-6 minuti"));
  Serial.print(F("Durata ciclo impostata all\'avvio: "));
  Serial.print(durataCiclo() / 60000UL);
  Serial.println(F(" minuto/i"));
  Serial.print(F("Posizione potenziometro A0: "));
  Serial.println(analogRead(PIN_POT));
  Serial.println();
}

// ============================================================
// LOOP
// ============================================================

void loop() {

  // ----- comandi fisici -----

  if (pulsantePremuto(PIN_START,
                      lastStartRead, stableStart, dbStartMs)) {
    toggleStartStop();
  }

  if (pulsantePremuto(PIN_NEXT,
                      lastNextRead, stableNext, dbNextMs)) {
    if (!testInCorso) faseAvanti();
  }

  if (pulsantePremuto(PIN_TEST,
                      lastTestRead, stableTest, dbTestMs)) {
    testUscite();
  }

  // ----- ciclo scenografico -----

  if (!testInCorso) {
    unsigned long durata = durataCiclo();
    float p = percentualeCiclo(durata);

    int potNow = analogRead(PIN_POT);
    if (ultimoPotOled < 0) ultimoPotOled = potNow;
    if (abs(potNow - ultimoPotOled) >= POT_POPUP_DELTA) {
      ultimoPotOled = potNow;
      oledMostraPopup(OLED_VELOCITA);
    }

    aggiornaScena(p);
    aggiornaReleSchedulati(p);
    aggiornaOled(durata, p);

    // ----- diagnostica -----
    if (millis() - lastDebugMs >= DEBUG_INTERVAL_MS) {
      lastDebugMs = millis();
      stampaStato(durata, p);
    }
  }
}
