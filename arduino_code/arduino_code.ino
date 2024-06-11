#include <Wire.h>
#include "HX711.h"

const int LOADCELL_DOUT_PIN = 2;
const int LOADCELL_SCK_PIN = 3;
const byte I2C_ADDRESS = 0x08;

HX711 scale;

void setup() {
  Wire.begin(I2C_ADDRESS); // I2C 주소 설정
  Wire.onRequest(requestEvent); // I2C 요청 이벤트 설정
  Serial.begin(9600);

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale();
  scale.tare(); // 초기 무게 설정
}

void loop() {
  // 메인 루프는 비워두거나 다른 작업을 수행할 수 있습니다.
}

void requestEvent() {
  float weight = scale.get_units(10);
  byte weightBytes[sizeof(float)];
  memcpy(weightBytes, &weight, sizeof(weight));
  Wire.write(weightBytes, sizeof(weightBytes)); // 무게 데이터를 I2C로 전송
}
