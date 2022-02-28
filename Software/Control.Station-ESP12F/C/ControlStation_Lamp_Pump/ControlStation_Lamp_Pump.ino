#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <TimeLib.h>
#include "FS.h"

HTTPClient http;
WiFiClient wifiClient;
ESP8266WebServer server(80);

// --- Config file ---
String essid;
String password;
String webserver_ip;
String webserver_path_info_timestamp;
String webserver_path_lamp_register;
String webserver_path_pump_register;
String webserver_path_info_is_alive;

String lamp_id;
int lamp_gpio;
String pump_id;
int pump_gpio;
int led_status_gpio;
int led_status_inverse;
int register_interval_sec;
int reset_hours;

bool pumpActive;
// -------------------

void setup() {
  Serial.begin(115200);
  Serial.println("\n");
  delay(2000);
  
  // --- Config --- //
  Serial.println("========== Setup ==========");
  Serial.println("vvv Reading Config file vvv");

  if(!SPIFFS.begin()){
    Serial.println("Failed to mount file system");
    Serial.println("!!! Wait 1 minute and then restart !!!");
    delay(60000);
    ESP.restart();
  }

  if(!loadConfig()){
    Serial.println("Failed to load config");
    return;
  }else{
    Serial.println("^^^    Config loaded    ^^^\n");    
  }

  // --- Connect to WiFi --- //
  connectToWiFi();

  Serial.println("\n");

  // --- Sync Time --- //
  if( !syncTime() ){
    Serial.println("!!! Wait 1 minute and then restart !!!");
    delay(60000);
    ESP.restart();
  }

  // --- Configure and Register Lamp and Pump --- //
  pinMode(lamp_gpio, OUTPUT);
  pinMode(pump_gpio, OUTPUT);

  if( !registerLamp() || !registerPump() ){
    Serial.println("!!! Wait 1 minute and then restart !!!");
    delay(60000);
    ESP.restart();
  }

  // --- Web Server --- //
  server.on("/isAlive", HTTP_GET, handleIsAlive );
  server.on("/lamp/on", HTTP_POST, handleLampOn);
  server.on("/lamp/off", HTTP_POST, handleLampOff);
  server.on("/pump/off", HTTP_POST, handlePumpOff);
  server.on("/pump/on", HTTP_POST, handlePumpOn);
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP server started\n");

  // --- Pump status -- //
  if (!syncPumpStatus()){
    Serial.println("!!! Wait 1 minute and then restart !!!");
    delay(60000);
    ESP.restart();
  }

  Serial.println("===========================\n");
}

long timestamp = 0;
void loop() {

  server.handleClient();

  if (pumpActive && timestamp != now()){
    timestamp = now();
    if(timestamp%10 == 0){
      syncPumpStatus();
    }
  }
}
