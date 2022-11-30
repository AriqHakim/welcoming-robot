#include <Servo.h>

Servo head;
Servo hand;
int headPos = 90;
int currPos = 90;
int handPos = 50;
int handCheckPoint = 50;
int waveLowPos = 50;
int waveHighPos = 140;

void setup() {
  head.attach(8);
  hand.attach(9);
  head.write(90);
  hand.write(50);
  Serial.begin(115200);
}

void loop() {
  String perintah = "";
  while (Serial.available() > 0) {
    char karakter = Serial.read();
    Serial.println(karakter);
    perintah = perintah + karakter;
    delay(10);
  }

  if (perintah.equals("")) {
    return;
  } else {
    currPos = perintah.toInt();
    if(headPos < currPos){
      headPos += 5;
    }

    if(headPos > currPos){
      headPos -= 5;
    }

    head.write(headPos);
    wave();
  }

//  Serial.println(perintah);
//  wave();
}

void wave() {
  if (handCheckPoint <= waveLowPos) {
    handPos += 1;
    hand.write(handPos);
    if (handPos == waveHighPos) {
      handCheckPoint = waveHighPos;
    }
  } else if (handCheckPoint >= waveHighPos) {
    handPos -= 1;
    hand.write(handPos);
    if (handPos == waveLowPos) {
      handCheckPoint = waveLowPos;
    }
  }
  delay(10);
}
