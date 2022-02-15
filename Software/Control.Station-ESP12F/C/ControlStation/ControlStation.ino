#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <TimeLib.h>
#include "FS.h"

void setup() {
  Serial.begin(115200);
  Serial.println("\n");
  delay(2000);
  
  // --- Config --- //
  Serial.println("========== Setup ==========");
  Serial.println("vvv Reading Config file vvv");

  if(!SPIFFS.begin()){
    Serial.println("Failed to mount file system");
    return;
  }

  if(!loadConfig()){
    Serial.println("Failed to load config");
    return;
  }else{
    Serial.println("^^^    Config loaded    ^^^\n");    
  }

  // --- Connect to WiFi --- //
  if (!connectToWiFi()){
    return;
  }

  Serial.println("\n");

  // --- Sync Time --- //
  syncTime();

  Serial.println("===========================\n");
}

void loop() {
  Serial.println(getOffsetDateString());
  delay(10000);
}
