#include <Arduino.h>
#include <Arduino_FreeRTOS.h>
 
const int del=100;  
 
int currentDirection = 3;
 
// Pins for LEDs and buttons
const int pinL = 11;
const int pinR = 12;
const int pinA = LED_BUILTIN;
const int pinBtnL = 2;
const int pinBtnR = 3;
const int pinBtnA = 4;
const int pinBtnO = 5;
const int pinBtnT = 6;
const int pinBtnH = 7;
const int pinBtnS = 8;
const int pinBtnX = 9;
 
void flash(int pin) {
  if ( currentDirection == 0) {digitalWrite(pinL, HIGH);};
  if ( currentDirection == 1) {digitalWrite(pinR, HIGH);};  
  if ( currentDirection == 2) {digitalWrite(pinL, HIGH); digitalWrite(pinR, HIGH);};
  if ( currentDirection == 3) {digitalWrite(LED_BUILTIN, HIGH);};   
  delay(500);
 
  digitalWrite(pinL, LOW);  digitalWrite(pinR, LOW);  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
 
  Serial.println(currentDirection);
}
 
void tnx(int pin) {
for (int i = 0; i < 5; i++) {
  digitalWrite(pinL, HIGH);
  delay(del);
  digitalWrite(pinL, LOW);
 
  digitalWrite(pinR, HIGH);
  delay(del);
  digitalWrite(pinR, LOW);
}
  digitalWrite(pinL, LOW);  digitalWrite(pinR, LOW);  digitalWrite(LED_BUILTIN, LOW);  
  currentDirection = 3;
 
  Serial.println("TNX");
}
 
void txT(){
  digitalWrite(pinL, HIGH); digitalWrite(pinR, HIGH);
  delay(500);
  digitalWrite(pinL, LOW);  digitalWrite(pinR, LOW);
  delay(200);
  }
void txD(){
  digitalWrite(pinL, HIGH); digitalWrite(pinR, HIGH);
  delay(100);
  digitalWrite(pinL, LOW);  digitalWrite(pinR, LOW);
  delay(200);
  }
void txP(){
  delay(500);
  digitalWrite(pinL, LOW);  digitalWrite(pinR, LOW);
  }
 
void ham(int pin) {
txT();txP();
txT();txD();txP();
txT();txD();txD();txT();txP();
 
  digitalWrite(pinL, LOW);  digitalWrite(pinR, LOW);  digitalWrite(LED_BUILTIN, LOW);  
  currentDirection = 3;
 
  Serial.println("HAM");
}
void sos(int pin) {
delay(1000);
txD();txD();txD();txP();
txT();txT();txT();txP();
txD();txD();txD();txP();
delay(1000);
  Serial.println("SOS");
}
void xx(int pin) {
 
  digitalWrite(pinL, HIGH);
  delay(20);
  digitalWrite(pinL, LOW);
delay(10);
  digitalWrite(pinR, HIGH);
  delay(20);
  digitalWrite(pinR, LOW);
 
  delay(5000);
  Serial.println("X");
}
 
// Set up LEDs and buttons as inputs
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(pinL, OUTPUT);
  pinMode(pinR, OUTPUT);
  pinMode(pinA, OUTPUT);
  pinMode(pinBtnL, INPUT_PULLUP);
  pinMode(pinBtnR, INPUT_PULLUP);
  pinMode(pinBtnA, INPUT_PULLUP);
  pinMode(pinBtnO, INPUT_PULLUP);
  pinMode(pinBtnT, INPUT_PULLUP);
  pinMode(pinBtnH, INPUT_PULLUP);
  pinMode(pinBtnS, INPUT_PULLUP);
  pinMode(pinBtnX, INPUT_PULLUP);
  pinMode(10, INPUT_PULLUP);
 
  Serial.begin(57600);
 
  xTaskCreate(scanButtons, "ScanButtons", 128, NULL, 1, NULL);
  xTaskCreate(flashTurnSignals, "FlashTurnSignals", 128, NULL, 1, NULL);
 
  vTaskStartScheduler();
}
 
// Task to scan buttons
void scanButtons(void *pvParameters) {
  while (true) {
 
    int stateBtnL = digitalRead(pinBtnL);
    if (stateBtnL == LOW) {
      currentDirection = 0;
    }
 
    int stateBtnR = digitalRead(pinBtnR);
    if (stateBtnR == LOW) {
      currentDirection = 1;
    }
 
    int stateBtnA = digitalRead(pinBtnA);
    if (stateBtnA == LOW) {
      currentDirection = 2;
    }
 
    int stateBtnO = digitalRead(pinBtnO);
    if (stateBtnO == LOW) {
      currentDirection = 3;
    }
 
    int stateBtnT = digitalRead(pinBtnT);
    if (stateBtnT == LOW) {
      currentDirection = 4;
    }
 
        int stateBtnH = digitalRead(pinBtnH);
    if (stateBtnH == LOW) {
      currentDirection = 5;
    }
 
        int stateBtnS = digitalRead(pinBtnS);
    if (stateBtnS == LOW) {
      currentDirection = 6;
    }
 
        int stateBtnX = digitalRead(pinBtnX);
    if (stateBtnX == LOW) {
      currentDirection = 7;
    }
 
  }
}
 
// Task to flash turn signals
void flashTurnSignals(void *pvParameters) {
  int i=0;
  while (true) {
    switch (currentDirection) {
      case 0:
        flash(currentDirection);
        break;
      case 1:
        flash(currentDirection);
        break;
      case 2:
        flash(currentDirection);
        break;
      case 3:
        flash(currentDirection);
        break;
      case 4:
        tnx(currentDirection);
        break;
      case 5:
        ham(currentDirection);
        break;
      case 6:
        sos(currentDirection);
        break;
      case 7:
        xx(currentDirection);
        break;        
    }
  }
}
 
void loop() {
    vTaskDelete(NULL);
}

