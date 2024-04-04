// http://ur4uqu.com/
///////// http://ur4uqu.com/cam/user/Main/tmp/v2024-01-26_17-06-11.jpg
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <Wire.h>
#include <I2C_RTC.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <SD.h>
#include <Adafruit_ADS1X15.h>
Adafruit_ADS1115 ads; 
 
#define PIN_SPI_CS 10
File myFile;
String fname ="log.txt";
 
static DS1307 RTC;
//#define SEALEVELPRESSURE_HPA (1013.25)
#define SEALEVELPRESSURE_HPA (1024.40)
 
Adafruit_BME280 bme; 
unsigned long delayTime;
 
#define ONE_WIRE_BUS 4
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire, ONE_WIRE_BUS);
 
void setup() {
    Serial.begin(9600);
 
 
    RTC.begin();
    RTC.setHourMode(CLOCK_H24);
 
    delayTime = 58000;
 
  if (!SD.begin(PIN_SPI_CS)) {
    Serial.println(F("SD CARD FAILED!!!"));
    while (1); 
  }
  if (!ads.begin()) {
    Serial.println("Failed to initialize ADS.");
    while (1);
  }
  ads.startADCReading(ADS1X15_REG_CONFIG_MUX_DIFF_0_1, /*continuous=*/false);
  Serial.println(F("SD CARD INITIALIZED."));
  pinMode(9, OUTPUT);
//////////////
if (0){
 
  myFile = SD.open(fname, FILE_READ);
  if (myFile) {
    int line_count = 0;
    while (myFile.available()) {
      char line[255]; 
      int line_length = myFile.readBytesUntil('\n', line, 100); // read line-by-line from Micro SD Card
      line_count++;
 
      Serial.print(F("Line "));
      Serial.print(line_count);
      Serial.print(F(": "));
      Serial.write(line, line_length); // print the character to Serial Monitor
      // \n character is escaped by readBytesUntil function
      Serial.write('\n'); // print a new line charactor
    }
    myFile.close();
  } else {
    Serial.print("SD Card: error on opening file:"+fname);
  }
}
//////////////
 
//  SD.remove(fname); //!!!!!!!!!! delete the file if existed
  tolog("Start");
}
 
 
void loop() { 
 
  if (!ads.conversionComplete()) {
    return;
  }
  int16_t results = ads.getLastConversionResults();
//  Serial.print("Differential: "); Serial.print(results); Serial.print("("); Serial.print(ads.computeVolts(results)); Serial.println("mV)");
 
 
   tolog(mydate()+" / "+st_bme()+" / V16= "+String(ads.computeVolts(results))+" / "+st_tmp());
 
  // Start another conversion.
  ads.startADCReading(ADS1X15_REG_CONFIG_MUX_DIFF_0_1, /*continuous=*/false);
 
//   delay(delayTime);
}
 
String mydate(){ 
  return String(RTC.getYear())+"-"+String(RTC.getMonth(),2)+"-"+String(RTC.getDay())+" "+String(RTC.getHours())+":"+String(RTC.getMinutes())+":"+String(RTC.getSeconds());
}
 
String st_bme() {
    unsigned status;
    String tt="";
 
    status = bme.begin(0x76);  
 
  if (status) {    
    return String(bme.readTemperature()) + " °C " + String(bme.readHumidity()) + " % " + String((bme.readPressure()/100.0F)+37) + " hPa " + String(bme.readAltitude(SEALEVELPRESSURE_HPA)) + " m";
  }
 
}
 
String st_tmp() {
    String tt="";
    sensors.begin(); 
    delay(10);
    sensors.requestTemperatures();
 
  for(int i=0;i<sensors.getDeviceCount();i++) {
    tt += "T"+String(i)+": "+String(sensors.getTempCByIndex(i))+" ";
  } 
 
return tt;  
}
 
void tolog(String ss){
 
 Serial.println(ss); 
 
  myFile = SD.open(fname, FILE_WRITE);
 
  if (myFile) {
    myFile.println(ss); 
    myFile.close();
    myledb();
  } else {
    Serial.print(F("SD Card: error "));
    SD.begin(PIN_SPI_CS);
  }
}
 
void myledb(){
  digitalWrite(9, HIGH);
  delay(1000);
  digitalWrite(9, LOW);
}
