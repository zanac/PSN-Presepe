#include "wokwi-api.h"
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

typedef struct {
  pin_t pins[3];
  uint64_t rise_ns[3];
  uint64_t period_ns[3];
  uint64_t high_ns[3];
  uint64_t last_edge_ns[3];
  uint8_t value[3];
  buffer_t framebuffer;
  uint32_t width;
  uint32_t height;
  timer_t refresh_timer;
} chip_state_t;

static int channel_for_pin(chip_state_t *chip, pin_t pin) {
  for (int i = 0; i < 3; i++) {
    if (chip->pins[i] == pin) return i;
  }
  return -1;
}

static void pin_changed(void *user_data, pin_t pin, uint32_t value) {
  chip_state_t *chip = (chip_state_t *)user_data;
  int ch = channel_for_pin(chip, pin);
  if (ch < 0) return;

  uint64_t now = get_sim_nanos();
  chip->last_edge_ns[ch] = now;

  if (value == HIGH) {
    if (chip->rise_ns[ch] != 0) {
      chip->period_ns[ch] = now - chip->rise_ns[ch];
      if (chip->period_ns[ch] > 0 && chip->high_ns[ch] <= chip->period_ns[ch]) {
        chip->value[ch] = (uint8_t)((chip->high_ns[ch] * 255ULL) / chip->period_ns[ch]);
      }
    }
    chip->rise_ns[ch] = now;
  } else {
    if (chip->rise_ns[ch] != 0) {
      chip->high_ns[ch] = now - chip->rise_ns[ch];
      if (chip->period_ns[ch] > 0 && chip->high_ns[ch] <= chip->period_ns[ch]) {
        chip->value[ch] = (uint8_t)((chip->high_ns[ch] * 255ULL) / chip->period_ns[ch]);
      }
    }
  }
}

static void refresh(void *user_data) {
  chip_state_t *chip = (chip_state_t *)user_data;
  uint64_t now = get_sim_nanos();

  // analogWrite(0) and analogWrite(255) become static LOW/HIGH on AVR.
  // If no PWM edge has arrived for 5 ms, use the actual digital level.
  for (int i = 0; i < 3; i++) {
    if (chip->last_edge_ns[i] == 0 || now - chip->last_edge_ns[i] > 5000000ULL) {
      chip->value[i] = pin_read(chip->pins[i]) == HIGH ? 255 : 0;
    }
  }

  uint32_t bytes = chip->width * chip->height * 4;
  uint8_t *pixels = (uint8_t *)malloc(bytes);
  if (!pixels) return;

  for (uint32_t i = 0; i < chip->width * chip->height; i++) {
    pixels[i * 4 + 0] = chip->value[0];
    pixels[i * 4 + 1] = chip->value[1];
    pixels[i * 4 + 2] = chip->value[2];
    pixels[i * 4 + 3] = 255;
  }

  buffer_write(chip->framebuffer, 0, pixels, bytes);
  free(pixels);
}

void chip_init(void) {
  chip_state_t *chip = (chip_state_t *)calloc(1, sizeof(chip_state_t));

  chip->pins[0] = pin_init("R", INPUT);
  chip->pins[1] = pin_init("G", INPUT);
  chip->pins[2] = pin_init("B", INPUT);

  chip->framebuffer = framebuffer_init(&chip->width, &chip->height);

  const pin_watch_config_t watch = {
    .edge = BOTH,
    .pin_change = pin_changed,
    .user_data = chip,
  };
  for (int i = 0; i < 3; i++) {
    pin_watch(chip->pins[i], &watch);
  }

  timer_config_t timer_config = {
    .callback = refresh,
    .user_data = chip,
  };
  chip->refresh_timer = timer_init(&timer_config);
  timer_start(chip->refresh_timer, 20000, true);
  refresh(chip);
}
