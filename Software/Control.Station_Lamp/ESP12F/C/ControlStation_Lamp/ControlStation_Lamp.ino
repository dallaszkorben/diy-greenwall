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
String webserver_path_info_is_alive;

String lamp_id;
int lamp_gpio;
int led_status_gpio;
int led_status_inverse;
int register_interval_sec;
int regular_reset_seconds;

bool lampActive = false;

#define LED_INITIATE 0
#define LED_COMMUNICATE 1
#define LED_HEALTHY 2
#define LED_ERROR 3

int ledStatus = LED_INITIATE;

bool healthy = true;
long syncTimestamp = 0;
long regTimestamp = 0;
long resetTimestamp = 0;

String timeOffsetString;
int timeOffsetInt;

// 3600000 = 1h
//unsigned long intervalRestartMillis = 3600000;
unsigned long intervalRestartMillis = 120000;

// -------------------

void setup() {
  Serial.begin(115200);
  Serial.println("\n");
  delay(2000);

  pinMode(LED_BUILTIN, OUTPUT);  

  ledSignalInitiate();
  
  // --- Config --- //
  Serial.println("========== Setup ==========");
  Serial.println("vvv Reading Config file vvv");

  if(!SPIFFS.begin()){
    Serial.println("Failed to mount file system");
    Serial.println("!!! Wait 10 seconds and then restart !!!");
    delay(10000);
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

  // --- Sync Time --- //
  if( !syncTime() ){
    ledSignalNetworkError();
    Serial.println("==========================");
    Serial.println("===   !!!  RESET  !!!  ===");
    Serial.println("===  Failed Sync Time  ===");
    Serial.println("==========================");
    ESP.restart();
  }

  // --- Configure and Register Lamp --- //
  pinMode(lamp_gpio, OUTPUT);

  if( !registerLamp() ){
    ledSignalNetworkError();
    Serial.println("=================================");
    Serial.println("===     !!!  RESET  !!!       ===");
    Serial.println("===  Failed to register LAMP  ===");
    Serial.println("=================================");
    delay(60000);
    ESP.restart();
  }

  // --- Web Server --- //
  server.on("/isAlive", HTTP_GET, handleIsAlive );
  server.on("/lamp/status", HTTP_GET, handleLampStatus);
  server.on("/lamp/on", HTTP_POST, handleLampOn);
  server.on("/lamp/off", HTTP_POST, handleLampOff);
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP server started\n");

  // --- Sync Lamp statuses -- //
  if (!syncLampStatus()){
    ledSignalNetworkError();
    Serial.println("=============================");
    Serial.println("===     !!!  RESET  !!!   ===");
    Serial.println("===  Failed to Sync Lamp  ===");
    Serial.println("=============================");
    delay(60000);
    ESP.restart();
  }

  ledSignalHealthy();

  resetTimestamp = now() + regular_reset_seconds;
  Serial.print("Next reset will be at: ");
  Serial.println(resetTimestamp);

  Serial.println("\n============== setup() finished =================\n\n");

}

void loop() {

  server.handleClient();

  // in every seconds
  if (syncTimestamp != now()){
    syncTimestamp = now();  
  }

  // reset_hours
  if (now() > resetTimestamp){
    Serial.println("=========================");
    Serial.println("===  !!!  RESET  !!!  ===");
    Serial.println("===      Regular      ===");
    Serial.print(  "=== Time: ");
    Serial.print(now());
    Serial.println("  ===");
    Serial.println("=========================");
    ESP.reset();    
  }

  // in every seconds
  if (regTimestamp != now()){

    // If there is WiFi connection
    if( WiFi.localIP().isSet() and WiFi.isConnected() ){

      regTimestamp = now();  

      // in every 30 seconds it tries to register
      if( regTimestamp%30 == 0 ){

        if( !registerLamp()){
          healthy = false;
        }else{
          healthy = true;
        }
      }

      // in every hour it resets
      if( millis() >= intervalRestartMillis ){
        Serial.println();
        Serial.println("==========================");
        Serial.println("===  !!!  RESET   !!!  ===");
        Serial.println("===      general       ===");
        Serial.println("==========================");
        Serial.println();
        ESP.reset();
      }
            
    }else{
      //healthy = false;
    }
  }

  if( healthy && ledStatus == LED_ERROR){
    Serial.print("changed to HEALTHY - healthy: ");
    Serial.print(healthy);
    Serial.print(" ledStatus: ");
    Serial.println(ledStatus);
    
    ledSignalHealthy();
  }else if(!healthy && ledStatus == LED_HEALTHY){
    Serial.print("changed to ERROR - healthy: ");
    Serial.print(healthy);
    Serial.print(" ledStatus: ");
    Serial.println(ledStatus);

    ledSignalNetworkError();
  }
  
}
