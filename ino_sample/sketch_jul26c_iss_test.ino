#include <Adafruit_NeoPixel.h>

#define PIN1 6
#define PIN2 12

Adafruit_NeoPixel strip1 = Adafruit_NeoPixel(1, PIN1, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip2 = Adafruit_NeoPixel(1, PIN2, NEO_GRB + NEO_KHZ800);

int n;

void setup() {
  Serial.begin(9600);

  for (n = 2; n <= 13; n++) {
    pinMode(n, OUTPUT);
    digitalWrite(n, LOW);
  }

  strip1.begin();
  strip2.begin();
  strip1.show();
  strip2.show();
}

void loop() {
  if (Serial.available()) {
    char signal = Serial.read();
    Serial.print("Received: ");
    Serial.println(signal); 
    // my ISS signal nearby
    if (signal == '1') {
      colorWipe(strip1.Color(255, 255, 0), 50); 
      colorWipe(strip2.Color(255, 255, 0), 50);
      turn1();
    } else {
      clean();
    }
  }
}

void colorWipe(uint32_t c, uint8_t wait) {
  for (uint16_t i = 0; i < strip1.numPixels(); i++) {
    strip1.setPixelColor(i, c);
    strip1.show();
    delay(wait);
  }
  for (uint16_t i = 0; i < strip2.numPixels(); i++) {
    strip2.setPixelColor(i, c);
    strip2.show();
    delay(wait);
  }
}

void turn1() {
  for (n = 2; n <= 13; n++) {
    digitalWrite(n, HIGH);
    delay(100);
  }
  for (n = 2; n <= 13; n++) {
    digitalWrite(n, LOW);
    delay(100);
  }
}

void clean() {
  for (n = 2; n <= 13; n++) {
    digitalWrite(n, LOW);
  }
  strip1.clear();
  strip2.clear();
  strip1.show();
  strip2.show();
}
