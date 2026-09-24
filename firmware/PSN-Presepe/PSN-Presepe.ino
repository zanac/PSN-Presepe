/*
  PresepeController - FASE 1 v2
  Arduino Mega 2560

  USCITE
    D2 = Cielo RGB Rosso
    D3 = Cielo RGB Verde
    D4 = Cielo RGB Blu
    D5 = DATA stelle WS2811 (50 pixel, 12 V)
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
    ciclo completo regolabile da 5 a 60 minuti.

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

// ============================================================
// CONFIGURAZIONE PIN
// ============================================================

const uint8_t PIN_CIELO_R = 2;
const uint8_t PIN_CIELO_G = 3;
const uint8_t PIN_CIELO_B = 4;
const uint8_t PIN_STELLE_DATA = 5;

// Strisce RGB laterali da 1 m, dedicate agli effetti direzionali.
// Sinistra = tramonto; destra = alba. D13 resta PWM libero.
const uint8_t PIN_TRAMONTO_R = 10;
const uint8_t PIN_TRAMONTO_G = 11;
const uint8_t PIN_TRAMONTO_B = 12;
const uint8_t PIN_ALBA_R = 44;
const uint8_t PIN_ALBA_G = 45;
const uint8_t PIN_ALBA_B = 46;
const uint16_t NUM_STELLE = 50;
Adafruit_NeoPixel stelle(NUM_STELLE, PIN_STELLE_DATA, NEO_GRB + NEO_KHZ800);

const uint8_t PIN_START = 22;
const uint8_t PIN_NEXT  = 23;
const uint8_t PIN_TEST  = 24;
const uint8_t PIN_POT   = A0;


// -----------------------------------------------------------------------------
// RELÈ: 4 moduli x 4 canali = 16 uscite ON/OFF predisposte.
// D25-D40 sono riservati al cablaggio IN1..IN4 dei quattro moduli.
// La logica scenografica e il livello HIGH/LOW verranno definiti in seguito.
// -----------------------------------------------------------------------------
const uint8_t PIN_RELE[16] = {
  25, 26, 27, 28,
  29, 30, 31, 32,
  33, 34, 35, 36,
  37, 38, 39, 40
};

const bool PWM_INVERTED = false;

// Durata ciclo regolabile con il potenziometro
const unsigned long MIN_CYCLE_MS = 5UL  * 60UL * 1000UL;
const unsigned long MAX_CYCLE_MS = 60UL * 60UL * 1000UL;

// Fasi in percentuale
const float P_TRAMONTO = 35.0f;
const float P_CREPU    = 45.0f;
const float P_NOTTE    = 50.0f;
const float P_ALBA     = 80.0f;
const float P_GIORNO2  = 90.0f;

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
  ALBA,
  GIORNO_FINALE
};

bool running = true;
bool testInCorso = false;

unsigned long cycleStartMs = 0;
unsigned long pauseStartedMs = 0;
unsigned long lastDebugMs = 0;

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
  pwmWrite(PIN_CIELO_R, r);
  pwmWrite(PIN_CIELO_G, g);
  pwmWrite(PIN_CIELO_B, b);
}

void setTramonto(uint8_t r, uint8_t g, uint8_t b) {
  pwmWrite(PIN_TRAMONTO_R, r);
  pwmWrite(PIN_TRAMONTO_G, g);
  pwmWrite(PIN_TRAMONTO_B, b);
}

void setAlba(uint8_t r, uint8_t g, uint8_t b) {
  pwmWrite(PIN_ALBA_R, r);
  pwmWrite(PIN_ALBA_G, g);
  pwmWrite(PIN_ALBA_B, b);
}

// ============================================================
// STELLE WS2811
// ============================================================
// Effetto naturale: ogni notte viene generato un cielo diverso.
// Le stelle hanno luminosita' massima differente e compaiono/scompaiono
// progressivamente. Una piccola parte scintilla molto lentamente.

uint8_t stellaLum[NUM_STELLE];
uint8_t stellaOrdine[NUM_STELLE];
bool stellaTwinkle[NUM_STELLE];
bool cieloGenerato = false;
Fase ultimaFaseStelle = GIORNO;

void generaCieloStellato() {
  for (uint16_t i = 0; i < NUM_STELLE; i++) {
    stellaLum[i] = random(35, 181);       // luminosita' massima volutamente limitata
    stellaOrdine[i] = i;
    stellaTwinkle[i] = (random(100) < 18); // ~18% scintilla
  }

  // Fisher-Yates: ordine casuale di accensione.
  for (int i = NUM_STELLE - 1; i > 0; i--) {
    int j = random(i + 1);
    uint8_t tmp = stellaOrdine[i];
    stellaOrdine[i] = stellaOrdine[j];
    stellaOrdine[j] = tmp;
  }
  cieloGenerato = true;
}

void mostraStelle(float livello) {
  livello = constrain(livello, 0.0f, 1.0f);
  stelle.clear();

  // Numero di stelle visibili cresce progressivamente.
  uint16_t visibili = (uint16_t)(livello * NUM_STELLE + 0.5f);

  for (uint16_t pos = 0; pos < visibili; pos++) {
    uint8_t i = stellaOrdine[pos];
    float locale = livello * NUM_STELLE - pos;
    locale = constrain(locale, 0.0f, 1.0f);

    uint16_t v = (uint16_t)(stellaLum[i] * locale);

    // Scintillio morbido e limitato, senza lampeggi netti.
    if (stellaTwinkle[i] && v > 10) {
      uint8_t onda = (uint8_t)((millis() / (28UL + (i % 17))) & 0x1F);
      if (onda > 15) onda = 31 - onda;
      v = (v * (88U + onda)) / 103U;
    }

    // Bianco caldo ottenuto miscelando RGB.
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
  // ciclo piu' breve = effetto piu' veloce.
  return map(raw, 0, 1023, MAX_CYCLE_MS, MIN_CYCLE_MS);
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
  if (p < P_GIORNO2)  return ALBA;
  return GIORNO_FINALE;
}

const char* nomeFase(Fase f) {
  switch (f) {
    case GIORNO:        return "GIORNO";
    case TRAMONTO:      return "TRAMONTO";
    case CREPUSCOLO:    return "CREPUSCOLO";
    case NOTTE:         return "NOTTE";
    case ALBA:          return "ALBA";
    case GIORNO_FINALE: return "GIORNO";
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
    case GIORNO_FINALE: return P_GIORNO2;
  }
  return 0.0f;
}

Fase faseSuccessiva(Fase f) {
  switch (f) {
    case GIORNO:        return TRAMONTO;
    case TRAMONTO:      return CREPUSCOLO;
    case CREPUSCOLO:    return NOTTE;
    case NOTTE:         return ALBA;
    case ALBA:          return GIORNO_FINALE;
    case GIORNO_FINALE: return GIORNO;
  }
  return GIORNO;
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

  uint8_t r = 0, g = 0, b = 0, stelle = 0;
  uint8_t tr = 0, tg = 0, tb = 0; // luce laterale tramonto
  uint8_t ar = 0, ag = 0, ab = 0; // luce laterale alba

  switch (fase) {

    case GIORNO:
      r = 255;
      g = 210;
      b = 145;
      stelle = 0;
      break;

    case TRAMONTO: {
      float t = progresso(p, P_TRAMONTO, P_CREPU);

      r = 255;
      g = interpola8(210, 65, t);
      b = interpola8(145, 15, t);
      stelle = 0;

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
      stelle = interpola8(0, 235, t);
      break;
    }

    case NOTTE:
      r = 8;
      g = 12;
      b = 55;
      stelle = 235;
      break;

    case ALBA: {
      float t = progresso(p, P_ALBA, P_GIORNO2);

      r = interpola8(8, 255, t);
      g = interpola8(12, 180, t);
      b = interpola8(55, 100, t);
      stelle = interpola8(235, 0, t);

      // Alba direzionale dalla striscia destra: compare, raggiunge
      // il massimo a meta' fase e si fonde nuovamente con il giorno.
      {
        float arco = 1.0f - fabs(2.0f * t - 1.0f);
        ar = (uint8_t)(255.0f * arco);
        ag = (uint8_t)(135.0f * arco);
        ab = (uint8_t)(45.0f * arco);
      }
      break;
    }

    case GIORNO_FINALE: {
      float t = progresso(p, P_GIORNO2, 100.0f);

      r = 255;
      g = interpola8(180, 210, t);
      b = interpola8(100, 145, t);
      stelle = 0;
      break;
    }
  }

  setCielo(r, g, b);
  setTramonto(tr, tg, tb);
  setAlba(ar, ag, ab);
  setStelle(stelle);
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
  if (running) {
    pauseStartedMs = millis();
    running = false;
    Serial.println(F("PAUSA"));
  } else {
    unsigned long durataPausa = millis() - pauseStartedMs;

    // Sposta l'origine del ciclo per riprendere esattamente
    // dal punto in cui era stato fermato.
    cycleStartMs += durataPausa;

    running = true;
    Serial.println(F("RIPRESA"));
  }
}

// ============================================================
// TEST
// ============================================================

void fadeTest(uint8_t pin) {
  for (int v = 0; v <= 255; v += 5) {
    pwmWrite(pin, v);
    delay(8);
  }

  for (int v = 255; v >= 0; v -= 5) {
    pwmWrite(pin, v);
    delay(8);
  }

  pwmWrite(pin, 0);
}

void testUscite() {
  if (testInCorso) return;

  testInCorso = true;

  bool eraInMarcia = running;
  unsigned long tempoPausa = millis();

  running = false;
  tuttoSpento();

  Serial.println();
  Serial.println(F("=== TEST FASE 1 ==="));

  Serial.println(F("CH1 / D2 - ROSSO"));
  fadeTest(PIN_CIELO_R);

  Serial.println(F("CH2 / D3 - VERDE"));
  fadeTest(PIN_CIELO_G);

  Serial.println(F("CH3 / D4 - BLU"));
  fadeTest(PIN_CIELO_B);

  Serial.println(F("RGB LATERALE SINISTRA / TRAMONTO"));
  fadeTest(PIN_TRAMONTO_R);
  fadeTest(PIN_TRAMONTO_G);
  fadeTest(PIN_TRAMONTO_B);

  Serial.println(F("RGB LATERALE DESTRA / ALBA"));
  fadeTest(PIN_ALBA_R);
  fadeTest(PIN_ALBA_G);
  fadeTest(PIN_ALBA_B);

  Serial.println(F("D5 DATA - WS2811 STELLE"));
  for (uint8_t v = 0; v <= 250; v += 10) { setStelle(v); delay(20); }
  for (int v = 250; v >= 0; v -= 10) { setStelle((uint8_t)v); delay(20); }

  tuttoSpento();

  Serial.println(F("=== FINE TEST ==="));
  Serial.println();

  // Il tempo trascorso durante il test non deve far avanzare il ciclo.
  if (eraInMarcia) {
    cycleStartMs += millis() - tempoPausa;
    running = true;
  } else {
    pauseStartedMs = millis();
    running = false;
  }

  testInCorso = false;
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
// SETUP
// ============================================================

void setup() {
  Serial.begin(115200);
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
  stelle.begin();
  stelle.clear();
  stelle.show();

  pinMode(PIN_START, INPUT_PULLUP);
  pinMode(PIN_NEXT,  INPUT_PULLUP);
  pinMode(PIN_TEST,  INPUT_PULLUP);

  tuttoSpento();

  delay(300);

  cycleStartMs = millis();

  Serial.println();
  Serial.println(F("========================================"));
  Serial.println(F(" PRESEPE CONTROLLER - FASE 1 v2"));
  Serial.println(F("========================================"));
  Serial.println(F("D2  = RGB Rosso"));
  Serial.println(F("D3  = RGB Verde"));
  Serial.println(F("D4  = RGB Blu"));
  Serial.println(F("D5  = DATA WS2811 (50 stelle)"));
  Serial.println(F("D10/D11/D12 = RGB SINISTRA / TRAMONTO"));
  Serial.println(F("D44/D45/D46 = RGB DESTRA / ALBA"));
  Serial.println(F("D22 = START/STOP"));
  Serial.println(F("D23 = AVANTI"));
  Serial.println(F("D24 = TEST"));
  Serial.println(F("A0  = VELOCITA' 5-60 minuti"));
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
    faseAvanti();
  }

  if (pulsantePremuto(PIN_TEST,
                      lastTestRead, stableTest, dbTestMs)) {
    testUscite();
  }

  // ----- ciclo scenografico -----

  if (!testInCorso) {
    unsigned long durata = durataCiclo();
    float p = percentualeCiclo(durata);

    aggiornaScena(p);

    // ----- diagnostica -----
    if (millis() - lastDebugMs >= DEBUG_INTERVAL_MS) {
      lastDebugMs = millis();
      stampaStato(durata, p);
    }
  }
}
