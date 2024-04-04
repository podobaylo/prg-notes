//#include <Wire.h>
//#include <SPI.h>
//#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
 
#define SEALEVELPRESSURE_HPA (1013.25)
 
Adafruit_BME280 bme; 
unsigned long delayTime;
 
void setup() {
    Serial.begin(9600);  
    Serial.println("BME280 test");
    unsigned status;
    status = bme.begin(0x76);  
    delayTime = 1000;
}
 
void loop() { 
    Serial.print("Temperature = "+String(bme.readTemperature())+" °C ");
    Serial.print("Pressure = "+String(bme.readPressure() / 100.0F)+ " hPa ");
    Serial.print("Approx. Altitude = "+String(bme.readAltitude(SEALEVELPRESSURE_HPA))+" m ");
    Serial.println("Humidity = "+String(bme.readHumidity())+" % ");
    delay(delayTime);
}
