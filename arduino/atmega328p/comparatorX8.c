// http://ur4uqu.com/

void setup() {
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
  pinMode(A6, INPUT);
  pinMode(A7, INPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);
}
 
float limit = 1.22; 
static uint32_t timer;
int ii=0;
 
void loop() {
 
float v0 = analogRead(A0) * (5.0 / 1023.0);
float v1 = analogRead(A1) * (5.0 / 1023.0);
float v2 = analogRead(A2) * (5.0 / 1023.0);
float v3 = analogRead(A3) * (5.0 / 1023.0);
float v4 = analogRead(A4) * (5.0 / 1023.0);
float v5 = analogRead(A5) * (5.0 / 1023.0);
float v6 = analogRead(A6) * (5.0 / 1023.0);
float v7 = analogRead(A7) * (5.0 / 1023.0);
 
if ( v0 < limit ) { digitalWrite(5, HIGH); } else { digitalWrite(5, LOW); }
if ( v1 < limit ) { digitalWrite(6, HIGH); } else { digitalWrite(6, LOW); }
if ( v2 < limit ) { digitalWrite(7, HIGH); } else { digitalWrite(7, LOW); }
if ( v3 < limit ) { digitalWrite(8, HIGH); } else { digitalWrite(8, LOW); }
if ( v4 < limit ) { digitalWrite(9, HIGH); } else { digitalWrite(9, LOW); }
if ( v5 < limit ) { digitalWrite(10, HIGH); } else { digitalWrite(10, LOW); }
if ( v6 < limit ) { digitalWrite(11, HIGH); } else { digitalWrite(11, LOW); }
if ( v7 < limit ) { digitalWrite(12, HIGH); } else { digitalWrite(12, LOW); }
 
if (millis() >= timer) {
timer = millis() + 1000;
  Serial.print(" limit="); Serial.print(limit);
  Serial.print(" < A0="); Serial.print(v0);
  Serial.print(" A1="); Serial.print(v1);
  Serial.print(" A2="); Serial.print(v2);
  Serial.print(" A3="); Serial.print(v3);
  Serial.print(" A4="); Serial.print(v4);
  Serial.print(" A5="); Serial.print(v5);
  Serial.print(" A6="); Serial.print(v6);
  Serial.print(" A7="); Serial.print(v7);
  Serial.println(" iter="+String(ii));
  ii=0;
}
ii++;
}
