#include <WiFi.h>
#include <TimeLib.h>

const char* ssid = "Central-Station-006";
const char* password = "viragfal";
//const char* ssid = "blabla2.4";
//const char* password = "Elmebetegek Almaiban";

const String serverIp = "192.168.50.3";                         // REPLACE WITH YOUR Raspberry Pi IP ADDRESS
//const String serverIp = "192.168.0.104";                        // REPLACE WITH YOUR Raspberry Pi IP ADDRESS
const int serverPort = 80;
  
void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  Serial.println();
  Serial.print("MAC: ");
  Serial.println(WiFi.macAddress());

  // --- Connect to Access Point --- //  
  if (!connectToApIfNotConnected()){
    Serial.println("    !!! Connection failed -> reboot !!!");
    ESP.restart();
  }  
}

unsigned long previousMillis = 0;
unsigned long intervalMillis = 10000;

int counter = 0;
IPAddress emptyIP = IPAddress(0, 0, 0, 0);  

void loop() {

  unsigned long currentMillis = millis();

  //In every 10 seconds
  if(currentMillis - previousMillis >= intervalMillis){
    printf("TimeStamp: %u  -  IP: %s\n", currentMillis, WiFi.localIP().toString().c_str());    

//    if(WiFi.status() != WL_CONNECTED || WiFi.localIP() == emptyIP){
      printf("        Reconnecting to WiFi... TimeStamp: %u  -  IP: %s\n", currentMillis, WiFi.localIP().toString().c_str());
      //Serial.println("Reconnecting to WiFi ...");
      WiFi.disconnect();
      WiFi.reconnect();
//    }
    previousMillis = currentMillis;
  }
 }   
}
