#include <Wire.h>
#include <Arduino.h>
#include <HX711.h>

const int loadCellPinDT = A0; // HX711의 DT핀과 연결된 아두이노 핀 번호
const int loadCellPinSCK = A1; // HX711의 SCK핀과 연결된 아두이노 핀 번호
const byte I2C_ADDRESS = 0x08; // I2C 주소

float scaleDivide = 100000; // 무게 보정

HX711 scale;

void setup() {
  Serial.begin(9600); // Baud Rate 설정
  Wire.begin(I2C_ADDRESS); // I2C 주소 설정
  Wire.onRequest(requestEvent); // I2C 요청 이벤트 설정

  scale.begin(loadCellPinDT, loadCellPinSCK); // 연결
  scale.set_scale(); // 기본 스케일 값 설정
  scale.tare(); // 처음 시작시 0점 잡기
}

void loop() {

  delay(1000); // 1초 delay (1초마다 반복)
}

void requestEvent() {
  float weight = scale.get_units() * 1000; // 무게를 gram 단위로 읽음
  byte weightBytes[sizeof(float)];
  memcpy(weightBytes, &weight, sizeof(weight));
  Wire.write(weightBytes, sizeof(weightBytes)); // 무게 데이터를 I2C로 전송
}
