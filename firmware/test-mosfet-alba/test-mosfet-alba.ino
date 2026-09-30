/*
  TEST A/B MOSFET RGB - Arduino Mega 2560
  ---------------------------------------
  Confronto simultaneo, a parita' di algoritmo:
    TRAMONTO = vecchia scheda MOSFET: D7, D11, D12
    ALBA     = nuova scheda MOSFET:   D44, D45, D46
    A0       = potenziometro
    D23      = AVANTI -> modalita' SOLO ROSSO
    D22      = START  -> modalita' RGB COMPLETO
    OLED I2C 128x64, 0x3C

  Il potenziometro varia continuamente:
    SOLO ROSSO: rosso tenue -> rosso pieno
    RGB: arancio tenue -> bianco caldo luminoso

  Entrambe le strisce ricevono SEMPRE gli stessi valori logici e lo stesso
  algoritmo: PWM hardware 8 bit + gamma 2.0, SENZA dithering temporale.
*/

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const uint8_t PIN_OLD_R = 7;
const uint8_t PIN_OLD_G = 11;
const uint8_t PIN_OLD_B = 12;
const uint8_t PIN_NEW_R = 44;
const uint8_t PIN_NEW_G = 45;
const uint8_t PIN_NEW_B = 46;

const uint8_t PIN_START = 22;
const uint8_t PIN_NEXT  = 23;
const uint8_t PIN_POT   = A0;

const int POT_RAW_MAX = 680;
const bool PWM_INVERTED = false;

const uint8_t OLED_ADDR = 0x3C;
Adafruit_SSD1306 display(128, 64, &Wire, -1);
bool oledPresente = false;

enum Modalita { SOLO_ROSSO, RGB_COMPLETO };
Modalita modalita = SOLO_ROSSO;

// Estremi logici RGB del test completo.
const uint8_t LOW_R  = 24;
const uint8_t LOW_G  = 5;
const uint8_t LOW_B  = 0;
const uint8_t HIGH_R = 255;
const uint8_t HIGH_G = 185;
const uint8_t HIGH_B = 95;

uint8_t gamma2(uint8_t value) {
  uint32_t squared = (uint32_t)value * value;
  return (uint8_t)((squared * 255UL + 32512UL) / 65025UL);
}

void pwmWrite(uint8_t pin, uint8_t logical) {
  uint8_t physical = gamma2(logical);
  analogWrite(pin, PWM_INVERTED ? 255 - physical : physical);
}

uint8_t interpola(uint8_t a, uint8_t b, uint16_t x) {
  return a + ((long)(b - a) * x + 500L) / 1000L;
}

void scriviEntrambe(uint8_t r, uint8_t g, uint8_t b) {
  // Stessi identici valori, nello stesso loop, ai vecchi e ai nuovi MOSFET.
  pwmWrite(PIN_OLD_R, r);
  pwmWrite(PIN_NEW_R, r);
  pwmWrite(PIN_OLD_G, g);
  pwmWrite(PIN_NEW_G, g);
  pwmWrite(PIN_OLD_B, b);
  pwmWrite(PIN_NEW_B, b);
}

bool pressione(uint8_t pin) {
  static bool precStart = HIGH, precNext = HIGH;
  bool ora = digitalRead(pin);
  bool &prec = (pin == PIN_START) ? precStart : precNext;
  bool evento = (prec == HIGH && ora == LOW);
  prec = ora;
  return evento;
}

void setup() {
  const uint8_t uscite[] = {PIN_OLD_R,PIN_OLD_G,PIN_OLD_B,PIN_NEW_R,PIN_NEW_G,PIN_NEW_B};
  for (uint8_t i=0; i<6; i++) {
    pinMode(uscite[i], OUTPUT);
    analogWrite(uscite[i], 0);
  }
  pinMode(PIN_START, INPUT_PULLUP);
  pinMode(PIN_NEXT, INPUT_PULLUP);

  Serial.begin(115200);
  Wire.begin();
#if defined(WIRE_HAS_TIMEOUT)
  Wire.setWireTimeout(25000UL, true);
#endif
  Wire.beginTransmission(OLED_ADDR);
  if (Wire.endTransmission() == 0)
    oledPresente = display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
}

void loop() {
  static int filtrato = -1;
  static unsigned long ultimoOled = 0;
  static unsigned long ultimoTasto = 0;

  if (millis() - ultimoTasto > 180) {
    if (pressione(PIN_NEXT)) {
      modalita = SOLO_ROSSO;
      ultimoTasto = millis();
    }
    if (pressione(PIN_START)) {
      modalita = RGB_COMPLETO;
      ultimoTasto = millis();
    }
  }

  int raw = constrain(analogRead(PIN_POT), 0, POT_RAW_MAX);
  if (filtrato < 0) filtrato = raw;
  filtrato = (filtrato * 7 + raw) / 8;

  // Potenziometro fisicamente invertito: raw basso = luminosita' alta.
  int invertito = POT_RAW_MAX - filtrato;
  uint16_t x = (uint32_t)invertito * 1000UL / POT_RAW_MAX;
  uint32_t xx = x;
  uint16_t smooth = (uint16_t)((xx * xx * (3000UL - 2UL * xx)) / 1000000UL);

  uint8_t r, g, b;
  if (modalita == SOLO_ROSSO) {
    // Parte da un rosso logico basso ma visibile e arriva al 100%.
    r = interpola(24, 255, smooth);
    g = 0;
    b = 0;
  } else {
    r = interpola(LOW_R, HIGH_R, smooth);
    g = interpola(LOW_G, HIGH_G, smooth);
    b = interpola(LOW_B, HIGH_B, smooth);
  }

  scriviEntrambe(r, g, b);

  if (millis() - ultimoOled >= 100) {
    ultimoOled = millis();
    uint8_t pr=gamma2(r), pg=gamma2(g), pb=gamma2(b);

    Serial.print(modalita == SOLO_ROSSO ? F("ROSSO") : F("RGB"));
    Serial.print(F(" A0=")); Serial.print(filtrato);
    Serial.print(F(" RGB=")); Serial.print(r); Serial.print(',');
    Serial.print(g); Serial.print(','); Serial.print(b);
    Serial.print(F(" PWM=")); Serial.print(pr); Serial.print(',');
    Serial.print(pg); Serial.print(','); Serial.println(pb);

    if (oledPresente) {
      display.clearDisplay();
      display.setTextColor(SSD1306_WHITE);
      display.setTextSize(1);
      display.setCursor(0,0); display.print(F("TEST A/B MOSFET"));
      display.setCursor(0,13);
      display.print(modalita == SOLO_ROSSO ? F("AVANTI: SOLO ROSSO") : F("START: RGB COMPLETO"));
      display.setCursor(0,27); display.print(F("A0 ")); display.print(filtrato);
      display.print(F("  ")); display.print((smooth+5)/10); display.print('%');
      display.setCursor(0,40); display.print(F("RGB "));
      display.print(r); display.print(','); display.print(g); display.print(','); display.print(b);
      display.setCursor(0,53); display.print(F("PWM "));
      display.print(pr); display.print(','); display.print(pg); display.print(','); display.print(pb);
      display.display();
    }
  }

  delay(5);
}
