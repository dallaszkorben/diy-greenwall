#include <WiFi.h>
#include <TimeLib.h>
#include <HTTPClient.h>

//const char* ssid = "Central-Station-006";
//const char* password = "viragfal";
const char* ssid = "blabla2.4";
const char* password = "Elmebetegek Almaiban";

//const String clientIp = "192.168.50.3";                         // REPLACE WITH YOUR Raspberry Pi IP ADDRESS
const String clientIp = "192.168.0.104";
const int clientPort = 80;
const String clientPathToInfoTimestamp = "info/timeStamp";

void startWebServer();

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

  // --- Sync Time --- //
  if( !syncTime() ){
    Serial.println("    !!! Sync Time failed -> reboot !!!");   
    ESP.restart();
  }

  // --- Start Camera Server --- //
  startWebServer();
}

unsigned long previousMillis = 0;
unsigned long intervalMillis = 10000;
unsigned long previousSecs = 0;
unsigned long intervalSecs = 32;

int counter = 0;
IPAddress emptyIP = IPAddress(0, 0, 0, 0);  

HTTPClient http;
WiFiClient wifiClient;

bool brokenRequest = false;

void loop() {

  unsigned long currentMillis = millis();

  //In every 10 seconds
  if(currentMillis - previousMillis >= intervalMillis){
    //printf("TimeStamp: %u  -  IP: %s\n", currentMillis, WiFi.localIP().toString().c_str());    

    if(WiFi.status() != WL_CONNECTED || WiFi.localIP() == emptyIP){
      printf("Reconnecting to WiFi... TimeStamp: %u  -  IP: %s\n", currentMillis, WiFi.localIP().toString().c_str());
      WiFi.disconnect();
      WiFi.reconnect();
    }
    previousMillis = currentMillis;
  }

  delay(10);
}   
