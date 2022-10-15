//#include <WiFi.h>
//#include <HTTPClient.h>

#include <ESP8266WiFi.h>        // connect to the WiFi
#include <ESP8266WiFiMulti.h>
//#include <esp8266httpclient.h>  // send HTTP request

#include <Preferences.h>
#include <TimeLib.h>


//WEB SERVER: #include <ESP8266WebServer.h> : https://circuits4you.com/2016/12/16/esp8266-web-server-html/
//WEB CLIENT: WiFiClient: https://forum.arduino.cc/t/webclient-with-esp8266/433217

const char* ssid = "Central-Station-006";
const char* password = "viragfal";

// --- Default values for Preferences ---
const bool DEFAULT_NEED_TO_RESET = false;

const String DEFAULT_STATION_ID = "default";
const unsigned long DEFAULT_INTERVAL_REPORT_MILLIS = 600000;      // 10 min
const unsigned long DEFAULT_INTERVAL_REGISTER_MILLIS = 600000;    // 20 min

// --- Preferences values ---
extern unsigned long intervalReportMillis = 0;
extern unsigned long intervalRegisterMillis = 0;

extern bool needToReset = false;

extern String stationId = "";

const String clientPathToInfoTimestamp = "info/timeStamp";
const String clientPathToCamRegister = "cam/register";
//const String clientPathToCamFrameSave = "cam/save/frame/camId/" + camId + "/camRotate/" + camRotate;
String clientPathToCamFrameSave;

unsigned long previousReconnectMillis = 0;
unsigned long intervalReconnectMillis = 10000;

unsigned long previousRegisterMillis = 0;
//unsigned long intervalRegisterMillis = 60000; // register / 60 seconds

unsigned long previousFrameMillis = 0;
extern unsigned long intervalFrameMillis = 20000; //save 1 frame / minute

int counter = 0;
IPAddress emptyIP = IPAddress(0, 0, 0, 0);  
bool brokenRegister = false;

ESP8266WiFiMulti WiFiMulti;
WiFiClient wifiClient;  // connect to the Internet
//HTTPClient http;        // communicate with Web site

Preferences stationPref;

//void startWebServer();
//bool configurePressure();
//bool configureSonic();
//bool configureRempHum();

//bool postFrame(WiFiClient wifiClient, String clientIp, String clientPort, String clientPathToCamFrameSave);


void wifiEvent(WiFiEvent_t event) {

    switch(event) {
        case WIFI_EVENT_STAMODE_GOT_IP:
            Serial.println("WIFI is connected!");
            Serial.println("   IP address: ");
            Serial.println(WiFi.localIP());
            break;
        case WIFI_EVENT_STAMODE_DISCONNECTED:
            Serial.println("WiFi lost connection");
            Serial.println("   Reconnecting...");
            WiFi.reconnect();
            break;
        case WIFI_EVENT_STAMODE_CONNECTED:
            Serial.println("Successfully connected to Access Point");
            break;
    }
}


void setup() {
  
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  // --- Setup variables - Read Persistent data ---  
  //setupVariables();

  
  Serial.println();
  Serial.print("MAC: ");
  Serial.println(WiFi.macAddress());
  Serial.println();

  // --- Connect to Access Point --- //  
//  if (!connectToAP()){
//    Serial.println("    !!! Connection failed -> reboot !!!");
//    ESP.restart();
//  }


  WiFi.disconnect(true);
  delay(1000);

  WiFi.onEvent(wifiEvent);
  
  WiFi.begin(ssid, password);
  Serial.println("Waiting for WIFI network..."); 




/*
  // --- Sync Time --- //
  if( !syncTime() ){
    Serial.println("    !!! Sync Time failed -> reboot !!!");   
    ESP.restart();
  }

  // --- Configure Cam --- //
  configureCam();
  
  // --- Register Camera Stream --- //
  if ( !registerCam() ){
    Serial.println("    !!! Cam register failed -> reboot !!!");   
    ESP.restart();    
  }
  
  // --- Start Camera Server --- //
  startWebServer();
*/
}


void loop() {

  Serial.println("loop");
  delay(1000);
/*
  if(needToReset){
    needToReset = false;
    saveVariable("needToReset"); 
    delay(2000);   
    ESP.restart();
  }
  
  unsigned long currentMillis = millis();

  //In every 10 seconds tries to RECONNECT if necessarry
  if(currentMillis - previousReconnectMillis >= intervalReconnectMillis){
    //printf("TimeStamp: %u  -  IP: %s\n", currentMillis, WiFi.localIP().toString().c_str());    

    if(WiFi.status() != WL_CONNECTED || WiFi.localIP() == emptyIP){
      printf("Reconnecting to WiFi... TimeStamp: %u  -  IP: %s\n", currentMillis, WiFi.localIP().toString().c_str());
      WiFi.disconnect();
      WiFi.reconnect();
    }
    previousReconnectMillis = currentMillis;
  }

  //In every 60 seconds tries to REGISTER
  if(currentMillis - previousRegisterMillis >= intervalRegisterMillis){

    if ( registerCam() ){
      Serial.println("   Camera was registered"); 
      previousRegisterMillis = currentMillis;      
    }else{
      Serial.println("    !!! Cam register failed !!!");   
      delay(1000);
    } 
    Serial.println();     
  
  //In every 30 seconds tries to take photo and SAVE FRAME
  }else if(currentMillis - previousFrameMillis >= intervalFrameMillis){

    clientPathToCamFrameSave = "cam/save/frame/camId/" + camId + "/camRotate/" + camRotate;

    if(postFrame(wifiClient, clientIp, clientPort, clientPathToCamFrameSave)){      
      Serial.println("   POST /cam/save/frame was sent");      
      previousFrameMillis = currentMillis;
    }else{
      Serial.println("   !!! Camera SAVE FRAME failed !!!");
      previousFrameMillis = currentMillis;
    }
    Serial.println();    
  }
*/
}   
