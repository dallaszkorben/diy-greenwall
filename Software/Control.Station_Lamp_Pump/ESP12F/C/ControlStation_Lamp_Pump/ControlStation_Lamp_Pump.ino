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
bool lampActive = false;

#define LED_INITIATE 0
#define LED_COMMUNICATE 1
#define LED_HEALTHY 2
#define LED_ERROR 3

int ledStatus = LED_INITIATE;

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
    ledSignalNetworkError();
    Serial.println("!!! Wait 2 seconds and then restart !!!");
    delay(2000);
    ESP.restart();
  }

  // --- Configure and Register Lamp and Pump --- //
  pinMode(lamp_gpio, OUTPUT);
  pinMode(pump_gpio, OUTPUT);

  if( !registerLamp() || !registerPump() ){
    ledSignalNetworkError();
    Serial.println("!!! Wait 1 minute and then restart !!!");
    delay(60000);
    ESP.restart();
  }

  // --- Web Server --- //
  server.on("/isAlive", HTTP_GET, handleIsAlive );
  server.on("/lamp/status", HTTP_GET, handleLampStatus);
  server.on("/lamp/on", HTTP_POST, handleLampOn);
  server.on("/lamp/off", HTTP_POST, handleLampOff);
  server.on("/pump/status", HTTP_GET, handlePumpStatus);
  server.on("/pump/off", HTTP_POST, handlePumpOff);
  server.on("/pump/on", HTTP_POST, handlePumpOn);
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP server started\n");

  // --- Sync Pump adn Lamp statuses -- //
  if (!syncLampStatus()){// || !syncPumpStatus()){
    ledSignalNetworkError();
    Serial.println("!!! Wait 1 minute and then restart !!!");
    delay(60000);
    ESP.restart();
  }

  Serial.println("===========================\n");

  ledSignalHealthy();
}

bool healthy = true;
long syncTimestamp = 0;
long regTimestamp = 0;
void loop() {

  server.handleClient();
  
  // in every seconds
  if (syncTimestamp != now()){
    syncTimestamp = now();  
    
    // If the pump is ON, in every 10 seconds it tries to sync it.
    if(pumpActive && syncTimestamp%1 == 0){      
      syncPumpStatus();
    }
  }

  // in every seconds
  if (regTimestamp != now()){

    //healthy = true;
    
    // If there is WiFi connection
    if( WiFi.localIP().isSet() and WiFi.isConnected() ){

      regTimestamp = now();  

      // in every 10 seconds it tries to register
      if( regTimestamp%30 == 0 ){
        if( !registerLamp() || !registerPump()){
          healthy = false;
        }else{
          healthy = true;
        }
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
