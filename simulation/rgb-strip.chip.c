#include "wokwi-api.h"
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

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
  uint32_t label_attr;
} chip_state_t;

// Minimal 5x7 uppercase font: only letters needed by ALBA, CIELO, TRAMONTO.
typedef struct { char c; uint8_t col[5]; } glyph_t;
static const glyph_t FONT[] = {
  {'A',{0x7E,0x11,0x11,0x11,0x7E}},
  {'B',{0x7F,0x49,0x49,0x49,0x36}},
  {'C',{0x3E,0x41,0x41,0x41,0x22}},
  {'G',{0x3E,0x41,0x49,0x49,0x7A}},
  {'I',{0x00,0x41,0x7F,0x41,0x00}},
  {'L',{0x7F,0x40,0x40,0x40,0x40}},
  {'M',{0x7F,0x02,0x0C,0x02,0x7F}},
  {'N',{0x7F,0x04,0x08,0x10,0x7F}},
  {'O',{0x3E,0x41,0x41,0x41,0x3E}},
  {'R',{0x7F,0x09,0x19,0x29,0x46}},
  {'T',{0x01,0x01,0x7F,0x01,0x01}}
};

static int channel_for_pin(chip_state_t *chip, pin_t pin) {
  for (int i = 0; i < 3; i++) if (chip->pins[i] == pin) return i;
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
      if (chip->period_ns[ch] > 0 && chip->high_ns[ch] <= chip->period_ns[ch])
        chip->value[ch] = (uint8_t)((chip->high_ns[ch] * 255ULL) / chip->period_ns[ch]);
    }
    chip->rise_ns[ch] = now;
  } else if (chip->rise_ns[ch] != 0) {
    chip->high_ns[ch] = now - chip->rise_ns[ch];
    if (chip->period_ns[ch] > 0 && chip->high_ns[ch] <= chip->period_ns[ch])
      chip->value[ch] = (uint8_t)((chip->high_ns[ch] * 255ULL) / chip->period_ns[ch]);
  }
}

static const uint8_t *glyph(char c) {
  for (unsigned i=0; i<sizeof(FONT)/sizeof(FONT[0]); i++) if (FONT[i].c==c) return FONT[i].col;
  return NULL;
}

static void pixel(uint8_t *p, uint32_t w, uint32_t h, int x, int y, uint8_t r, uint8_t g, uint8_t b) {
  if (x<0 || y<0 || x>=(int)w || y>=(int)h) return;
  uint32_t o=((uint32_t)y*w+(uint32_t)x)*4;
  p[o]=r; p[o+1]=g; p[o+2]=b; p[o+3]=255;
}

static void text5x7(uint8_t *p, uint32_t w, uint32_t h, int x, int y, const char *s) {
  while (*s) {
    const uint8_t *g=glyph(*s++);
    if (g) for (int cx=0;cx<5;cx++) for(int cy=0;cy<7;cy++)
      if (g[cx]&(1<<cy)) pixel(p,w,h,x+cx,y+cy,255,255,255);
    x+=6;
  }
}

static void refresh(void *user_data) {
  chip_state_t *chip=(chip_state_t *)user_data;
  uint64_t now=get_sim_nanos();
  for(int i=0;i<3;i++) {
    if(chip->last_edge_ns[i]==0 || now-chip->last_edge_ns[i]>5000000ULL)
      chip->value[i]=pin_read(chip->pins[i])==HIGH ? 255 : 0;
  }

  uint32_t bytes=chip->width*chip->height*4;
  uint8_t *pixels=(uint8_t *)malloc(bytes);
  if(!pixels) return;

  // Top 36 px: actual simulated strip colour. Bottom 16 px: black label area.
  for(uint32_t y=0;y<chip->height;y++) for(uint32_t x=0;x<chip->width;x++) {
    uint32_t o=(y*chip->width+x)*4;
    if(y<36) { pixels[o]=chip->value[0]; pixels[o+1]=chip->value[1]; pixels[o+2]=chip->value[2]; }
    else { pixels[o]=0; pixels[o+1]=0; pixels[o+2]=0; }
    pixels[o+3]=255;
  }

  uint32_t id=attr_read(chip->label_attr);
  const char *label=id==0 ? "ALBA" : (id==1 ? "CIELO" : "TRAMONTO");
  int text_w=(int)strlen(label)*6-1;
  text5x7(pixels,chip->width,chip->height,((int)chip->width-text_w)/2,41,label);

  buffer_write(chip->framebuffer,0,pixels,bytes);
  free(pixels);
}

void chip_init(void) {
  chip_state_t *chip=(chip_state_t *)calloc(1,sizeof(chip_state_t));
  chip->pins[0]=pin_init("R",INPUT);
  chip->pins[1]=pin_init("G",INPUT);
  chip->pins[2]=pin_init("B",INPUT);
  chip->label_attr=attr_init("labelId",0);
  chip->framebuffer=framebuffer_init(&chip->width,&chip->height);

  const pin_watch_config_t watch={.edge=BOTH,.pin_change=pin_changed,.user_data=chip};
  for(int i=0;i<3;i++) pin_watch(chip->pins[i],&watch);

  timer_config_t timer_config={.callback=refresh,.user_data=chip};
  chip->refresh_timer=timer_init(&timer_config);
  timer_start(chip->refresh_timer,20000,true);
  refresh(chip);
}
