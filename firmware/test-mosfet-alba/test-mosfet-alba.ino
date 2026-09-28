/*
  TEST MOSFET ALBA - Arduino Mega 2560
  ------------------------------------
  Test dedicato ai nuovi moduli MOSFET sui collegamenti gia' esistenti:
    D44 -> ALBA R
    D45 -> ALBA G
    D46 -> ALBA B
    A0  -> potenziometro (hardware invertito: raw 0 = massimo logico)
    OLED I2C 128x64 -> 0x3C

  Il potenziometro controlla CONTINUAMENTE il test, senza scaglioni 1/3/5 min:
    minimo -> arancio molto tenue
    massimo -> bianco caldo luminoso

  PWM hardware Arduino 8 bit + gamma 2.0, SENZA dithering temporale.
*/

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const uint8_t PIN_ALBA_R = 44;
const uint8_t PIN_ALBA_G = 45;
const uint8_t PIN_ALBA_B = 46;
const uint8_t PIN_POT = A0;

const int POT_RAW_MAX = 680;   // valore reale misurato sul presepe
const bool PWM_INVERTED = false;

const uint8_t OLED_ADDR = 0x3C;
Adafruit_SSD1306 display(128, 64, &Wire, -1);
bool oledPresente = false;

// Estremi LOGICI prima della gamma.
// Si parte volutamente sopra lo zero per osservare bene la zona di bassa luce.
const uint8_t LOW_R  = 24;
const uint8_t LOW_G  = 5;
const uint8_t LOW_B  = 0;

const uint8_t HIGH_R = 255;
const uint8_t HIGH_G = 185;
const uint8_t HIGH_B = 95;

uint8_t gamma2(uint8_t value) {
  // Gamma 2.0 -> PWM fisico 8 bit, arrotondato. Nessun dithering.
  uint32_t squared = (uint32_t)value * (uint32_t)value;
  return (uint8_t)((squared * 255UL + 32512UL) / 65025UL);
}

void pwmWrite(uint8_t pin, uint8_t logical) {
  uint8_t physical = gamma2(logical);
  analogWrite(pin, PWM_INVERTED ? 255 - physical : physical);
}

uint8_t interpola(uint8_t a, uint8_t b, uint16_t x) {
  // x 0..1000
  return a + ((long)(b - a) * x + 500L) / 1000L;
}

void setup() {
  pinMode(PIN_ALBA_R, OUTPUT);
  pinMode(PIN_ALBA_G, OUTPUT);
  pinMode(PIN_ALBA_B, OUTPUT);
  analogWrite(PIN_ALBA_R, 0);
  analogWrite(PIN_ALBA_G, 0);
  analogWrite(PIN_ALBA_B, 0);

  Serial.begin(115200);
  Wire.begin();
#if defined(WIRE_HAS_TIMEOUT)
  Wire.setWireTimeout(25000UL, true);
#endif
  Wire.beginTransmission(OLED_ADDR);
  if (Wire.endTransmission() == 0)
    oledPresente = display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);

  if (oledPresente) {
    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);
    display.setTextSize(1);
    display.setCursor(0,0); display.print(F("TEST MOSFET ALBA"));
    display.setCursor(0,18); display.print(F("8 bit + gamma 2.0"));
    display.setCursor(0,32); display.print(F("NO dithering"));
    display.setCursor(0,48); display.print(F("Ruota A0..."));
    display.display();
  }
}

void loop() {
  static int filtrato = -1;
  static unsigned long ultimoOled = 0;

  int raw = constrain(analogRead(PIN_POT), 0, POT_RAW_MAX);
  if (filtrato < 0) filtrato = raw;

  // Filtro leggero contro il rumore ADC, senza introdurre scaglioni.
  filtrato = (filtrato * 7 + raw) / 8;

  // Il potenziometro del presepe e' elettricamente invertito.
  int invertito = POT_RAW_MAX - filtrato;
  uint16_t x = (uint32_t)invertito * 1000UL / POT_RAW_MAX;

  // Smoothstep: movimento morbido mantenendo tutti i valori intermedi.
  uint32_t xx = x;
  uint16_t smooth = (uint16_t)((xx * xx * (3000UL - 2UL * xx)) / 1000000UL);

  uint8_t r = interpola(LOW_R, HIGH_R, smooth);
  uint8_t g = interpola(LOW_G, HIGH_G, smooth);
  uint8_t b = interpola(LOW_B, HIGH_B, smooth);

  pwmWrite(PIN_ALBA_R, r);
  pwmWrite(PIN_ALBA_G, g);
  pwmWrite(PIN_ALBA_B, b);

  if (millis() - ultimoOled >= 100) {
    ultimoOled = millis();
    uint8_t pr = gamma2(r), pg = gamma2(g), pb = gamma2(b);

    Serial.print(F("A0=")); Serial.print(filtrato);
    Serial.print(F("  %=")); Serial.print((smooth + 5) / 10);
    Serial.print(F("  RGB=")); Serial.print(r); Serial.print(',');
    Serial.print(g); Serial.print(','); Serial.print(b);
    Serial.print(F("  PWM=")); Serial.print(pr); Serial.print(',');
    Serial.print(pg); Serial.print(','); Serial.println(pb);

    if (oledPresente) {
      display.clearDisplay();
      display.setTextColor(SSD1306_WHITE);
      display.setTextSize(1);
      display.setCursor(0,0); display.print(F("TEST MOSFET ALBA"));
      display.setCursor(0,14); display.print(F("A0 ")); display.print(filtrato);
      display.print(F("  ")); display.print((smooth + 5) / 10); display.print('%');
      display.setCursor(0,28); display.print(F("RGB "));
      display.print(r); display.print(','); display.print(g); display.print(','); display.print(b);
      display.setCursor(0,42); display.print(F("PWM "));
      display.print(pr); display.print(','); display.print(pg); display.print(','); display.print(pb);
      display.setCursor(0,55); display.print(F("arancio -> bianco"));
      display.display();
    }
  }

  delay(5);
}
