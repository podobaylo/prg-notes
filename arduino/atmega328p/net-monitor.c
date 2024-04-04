/////// http://ur4uqu.com/cam/user/Main/tmp/v2024-02-22_11-22-47.jpg
#include <EtherCard.h>
 
static byte mymac[] = { 0x74,0x69,0x69,0x2D,0x00,0x01 };
 
byte Ethernet::buffer[700];
static uint32_t timer;
 
const char website[] PROGMEM = "ur4uqu.com";
 
String url;
 
static void my_callback (byte status, word off, word len) {
  Serial.println(">>>");
  Ethernet::buffer[off+1000] = 0;
  Serial.print((const char*) Ethernet::buffer + off);
  Serial.println("...");
}
 
void setup () {
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
  pinMode(A6, INPUT);
  pinMode(A7, INPUT);
  pinMode(3, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
  pinMode(5, INPUT_PULLUP);
  pinMode(6, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP);
  pinMode(8, INPUT_PULLUP);
  pinMode(9, INPUT_PULLUP);
 
  Serial.begin(57600);
  Serial.println(F("\n[webClient]"));
 
  // Change 'SS' to your Slave Select pin, if you arn't using the default pin
  if (ether.begin(sizeof Ethernet::buffer, mymac, SS) == 0)
    Serial.println(F("Failed to access Ethernet controller"));
  if (!ether.dhcpSetup())
    Serial.println(F("DHCP failed"));
 
  ether.printIp("IP:  ", ether.myip);
  ether.printIp("GW:  ", ether.gwip);
  ether.printIp("DNS: ", ether.dnsip);
 
#if 1
  // use DNS to resolve the website's IP address
  if (!ether.dnsLookup(website))
    Serial.println("DNS failed");
#elif 2
  // if website is a string containing an IP address instead of a domain name,
  // then use it directly. Note: the string can not be in PROGMEM.
  char websiteIP[] = "192.168.1.1";
  ether.parseIp(ether.hisip, websiteIP);
#else
  // or provide a numeric IP address instead of a string
  byte hisip[] = { 192,168,1,1 };
  ether.copyIp(ether.hisip, hisip);
#endif
 
  ether.printIp("SRV: ", ether.hisip);
}
 
void loop () {
  ether.packetLoop(ether.packetReceive());
 
 if (millis() > timer) {
  timer = millis() + 60000;
  Serial.println();
  Serial.print("<<< REQ ");
 
  // Read analog values from A0 to A7
  int av0 = analogRead(A0);
  int av1 = analogRead(A1);
  int av2 = analogRead(A2);
  int av3 = analogRead(A3);
  int av4 = analogRead(A4);
  int av5 = analogRead(A5);
  int av6 = analogRead(A6);
  int av7 = analogRead(A7);
  int dv3 = digitalRead(3);
  int dv4 = digitalRead(4);
  int dv5 = digitalRead(5);
  int dv6 = digitalRead(6);
  int dv7 = digitalRead(7);
  int dv8 = digitalRead(8);
  int dv9 = digitalRead(9);
 
  // Construct the URL with the analog values
  url = "ard-con.php?id=1&a0=" + String(av0);
  url += "&a1=" + String(av1);
  url += "&a2=" + String(av2);
  url += "&a3=" + String(av3);
  url += "&a4=" + String(av4);
  url += "&a5=" + String(av5);
  url += "&a6=" + String(av6);
  url += "&a7=" + String(av7);
  url += "&d3=" + String(dv3);
  url += "&d4=" + String(dv4);
  url += "&d5=" + String(dv5);
  url += "&d6=" + String(dv6);
  url += "&d7=" + String(dv7);
  url += "&d8=" + String(dv8);
  url += "&d9=" + String(dv9);
 
  // Convert the URL to a const char* pointer
  const char* fullUrl = url.c_str();
 
  // Send the HTTP request to the server
  ether.browseUrl(PSTR("/"), fullUrl, website, my_callback);
 
 }
 
}
