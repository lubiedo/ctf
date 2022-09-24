#include <stdio.h>
#include <stdint.h>

#include "writing.h"

void write(uint8_t d){
  printf("\t\tWire writing: ");
  if (d >= ' ' && d <= '~' )
    printf("%c (0x%x)\n", d, d);
  else
    printf("'%d' (0x%x)\n", d, d);
}

void expanderWrite(uint8_t _data){
  /* Wire.beginTransmission(_Addr); */
  write((int)(_data) | 0x08);
  /* Wire.endTransmission(); */
}

void pulseEnable(uint8_t _data){
  expanderWrite(_data | En);	// En high
  expanderWrite(_data & ~En);	// En low
}

void write4bits(uint8_t b) {
  printf("\t4-bits written: %d\n", b);
  expanderWrite(b);
  pulseEnable(b);
}

void send(uint8_t value, uint8_t mode) {
  uint8_t highnib=value&0xf0;
  uint8_t lownib=(value<<4)&0xf0;
  write4bits((highnib)|mode);
  write4bits((lownib)|mode); 
}

void command(uint8_t value) {
  printf("Command: 0x%0x\n", value);
  send(value, 0);
}

int _numlines = 12;
void setCursor(uint8_t col, uint8_t row){
  int row_offsets[] = { 0x00, 0x40, 0x14, 0x54 };
  if ( row > _numlines ) {
    row = _numlines-1;    // we count rows starting w/0
  }
  command(LCD_SETDDRAMADDR | (col + row_offsets[row]));
}

int main(void) {
  char *string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  command(LCD_CLEARDISPLAY);
  setCursor(0,0);

  while (*string)
  {
    printf("++ Writing letter: %c\n", *string);
    send(*(string++), Rs);
  }
  return 0;
}
