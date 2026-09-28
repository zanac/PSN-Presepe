/*
  PSN-Presepe - test comparativo PWM CIELO
  Arduino Mega 2560

  Spostare SOLO i tre ingressi del MOSFET della striscia CIELO:
    R -> D2  (Timer3B) - resta collegato
    G -> D3  (Timer3C) - resta collegato
    B -> D5  (Timer3A) - spostare temporaneamente da D4 a D5

  IMPORTANTE: durante il test scollegare la DATA STELLE da D5.

  OLED invariato: I2C 0x3C su SDA D20 / SCL D21.

  Il test ripete automaticamente:
    1) PWM 8 BIT
    2) PWM 12 BIT
    3) 12 BIT + GAMMA

  Ogni modalita' dura 30 s:
    15 s: nero -> arancione
    15 s: arancione -> nero
*/

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <math.h>

const uint8_t PIN_R = 2; // OC3B
const uint8_t PIN_G = 3; // OC3C
const uint8_t PIN_B = 5; // OC3A - temporaneamente al posto di D4

const uint8_t OLED_ADDR = 0x3C;
const uint8_t OLED_W = 128;
const uint8_t OLED_H = 64;
Adafruit_SSD1306 display(OLED_W, OLED_H, &Wire, -1);
bool oledPresente = false;

const unsigned long TEST_MS = 30000UL;
const unsigned long META_MS = TEST_MS / 2UL;

// Arancione di riferimento. Blu volutamente spento.
const uint8_t MAX_R_8 = 190;
const uint8_t MAX_G_8 = 24;
const uint8_t MAX_B_8 = 0;

enum Modalita { PWM8, PWM12, PWM12_GAMMA };
Modalita modalita = PWM8;
unsigned long inizioTest = 0;

void timer3_8bit() {
  // Fast PWM 8 bit, TOP=0x00FF, prescaler 1: ~62.5 kHz.
  TCCR3A = _BV(COM3A1) | _BV(COM3B1) | _BV(COM3C1) | _BV(WGM30);
  TCCR3B = _BV(WGM32) | _BV(CS30);
  OCR3A = OCR3B = OCR3C = 0;
}

void timer3_12bit() {
  // Fast PWM con ICR3 come TOP=4095, prescaler 1: ~3.9 kHz.
  TCCR3A = _BV(COM3A1) | _BV(COM3B1) | _BV(COM3C1) | _BV(WGM31);
  TCCR3B = _BV(WGM33) | _BV(WGM32) | _BV(CS30);
  ICR3 = 4095;
  OCR3A = OCR3B = OCR3C = 0;
}

void scrivi8(uint8_t r, uint8_t g, uint8_t b) {
  OCR3A = b; // D5
  OCR3B = r; // D2
  OCR3C = g; // D3
}

void scrivi12(uint16_t r, uint16_t g, uint16_t b) {
  OCR3A = constrain(b, 0, 4095); // D5
  OCR3B = constrain(r, 0, 4095); // D2
  OCR3C = constrain(g, 0, 4095); // D3
}

uint16_t scala12(uint8_t v) {
  return ((uint32_t)v * 4095UL + 127UL) / 255UL;
}

uint16_t gamma12(uint8_t v) {
  if (v == 0) return 0;
  float x = v / 255.0f;
  return (uint16_t)(pow(x, 2.0f) * 4095.0f + 0.5f);
}

const __FlashStringHelper *nomeModalita() {
  switch (modalita) {
    case PWM8: return F("PWM 8 BIT");
    case PWM12: return F("PWM 12 BIT");
    default: return F("12 BIT + GAMMA");
  }
}

void mostraOled(unsigned long trascorso, float livello) {
  if (!oledPresente) return;
  static unsigned long ultimo = 0;
  if (millis() - ultimo < 100) return;
  ultimo = millis();

  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print(F("TEST CIELO"));

  display.setTextSize(2);
  display.setCursor(0, 16);
  display.print(nomeModalita());

  display.setTextSize(1);
  display.setCursor(0, 42);
  display.print(trascorso < META_MS ? F("SALITA  ") : F("DISCESA "));
  display.print((int)(livello * 100.0f + 0.5f));
  display.print('%');

  display.drawRect(0, 54, 128, 9, SSD1306_WHITE);
  int fill = (int)(livello * 124.0f + 0.5f);
  if (fill > 0) display.fillRect(2, 56, fill, 5, SSD1306_WHITE);
  display.display();
}

void impostaModalita(Modalita nuova) {
  modalita = nuova;
  if (modalita == PWM8) timer3_8bit();
  else timer3_12bit();
  inizioTest = millis();
}

void setup() {
  pinMode(PIN_R, OUTPUT);
  pinMode(PIN_G, OUTPUT);
  pinMode(PIN_B, OUTPUT);
  digitalWrite(PIN_R, LOW);
  digitalWrite(PIN_G, LOW);
  digitalWrite(PIN_B, LOW);

  Serial.begin(115200);
  Wire.begin();
#if defined(WIRE_HAS_TIMEOUT)
  Wire.setWireTimeout(25000UL, true);
#endif
  if (display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    oledPresente = true;
    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);
    display.setTextSize(1);
    display.setCursor(0, 20);
    display.print(F("PSN PWM TEST"));
    display.setCursor(0, 36);
    display.print(F("R:D2 G:D3 B:D5"));
    display.display();
    delay(1500);
  }

  impostaModalita(PWM8);
}

void loop() {
  unsigned long trascorso = millis() - inizioTest;

  if (trascorso >= TEST_MS) {
    scrivi12(0, 0, 0);
    Modalita prossima = (Modalita)(((uint8_t)modalita + 1U) % 3U);
    impostaModalita(prossima);
    trascorso = 0;
  }

  float livello;
  if (trascorso < META_MS)
    livello = (float)trascorso / (float)META_MS;
  else
    livello = (float)(TEST_MS - trascorso) / (float)META_MS;

  livello = constrain(livello, 0.0f, 1.0f);

  uint8_t r8 = (uint8_t)(MAX_R_8 * livello + 0.5f);
  uint8_t g8 = (uint8_t)(MAX_G_8 * livello + 0.5f);
  uint8_t b8 = (uint8_t)(MAX_B_8 * livello + 0.5f);

  if (modalita == PWM8) {
    scrivi8(r8, g8, b8);
  } else if (modalita == PWM12) {
    // 12 bit lineare: conserva lo stesso colore/intensita' massima dell'8 bit.
    uint16_t r = (uint16_t)(scala12(MAX_R_8) * livello + 0.5f);
    uint16_t g = (uint16_t)(scala12(MAX_G_8) * livello + 0.5f);
    uint16_t b = (uint16_t)(scala12(MAX_B_8) * livello + 0.5f);
    scrivi12(r, g, b);
  } else {
    // Gamma applicata alla luminosita' della scena, poi colore arancione.
    uint8_t lum8 = (uint8_t)(255.0f * livello + 0.5f);
    uint16_t lum12 = gamma12(lum8);
    uint16_t r = ((uint32_t)scala12(MAX_R_8) * lum12) / 4095UL;
    uint16_t g = ((uint32_t)scala12(MAX_G_8) * lum12) / 4095UL;
    uint16_t b = ((uint32_t)scala12(MAX_B_8) * lum12) / 4095UL;
    scrivi12(r, g, b);
  }

  mostraOled(trascorso, livello);
}
