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
int pump_gpio;
int led_status_gpio;
int led_status_inverse;
int register_interval_sec;
int reset_hours;
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
    return;
  }

  if(!loadConfig()){
    Serial.println("Failed to load config");
    return;
  }else{
    Serial.println("^^^    Config loaded    ^^^\n");    
  }

  // --- Configure Lamp --- //
  pinMode(lamp_gpio, OUTPUT);   // Initialize the LED_BUILTIN pin as an output  

  // --- Connect to WiFi --- //
  if (!connectToWiFi()){
    return;
  }

  Serial.println("\n");

  // --- Sync Time --- //
  syncTime();

  // --- Register Lamp --- //
  registerLamp();

  // --- Web Server --- //
  server.on("/isAlive", HTTP_GET, handleIsAlive );
  server.on("/lamp/on", HTTP_POST, handleLampOn);
  server.on("/lamp/off", HTTP_POST, handleLampOff);
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP server started");

  Serial.println("===========================\n");
}

int cycle = 0;
void loop() {

  server.handleClient();
  
//  if(cycle%60 == 0){
//    connectToWiFiIfNotConnected();
//    //isAlive();
//  }
//
//  cycle++;
//  delay(1000);
}
