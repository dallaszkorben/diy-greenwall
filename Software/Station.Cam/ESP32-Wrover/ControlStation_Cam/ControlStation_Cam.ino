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
const String camId = "8";
const String clientPathToInfoTimestamp = "info/timeStamp";
const String clientPathToCamRegister = "cam/register";
const String clientPathToCamFrameSave = "cam/save/frame/camId/" + camId;

unsigned long previousReconnectMillis = 0;
unsigned long intervalReconnectMillis = 10000;

unsigned long previousRegisterMillis = 0;
unsigned long intervalRegisterMillis = 60000; // register / 60 seconds

unsigned long previousFrameSaveMillis = 0;
unsigned long intervalFrameSaveMillis = 20000; //save 1 frame / minute

HTTPClient http;
WiFiClient wifiClient;

void startWebServer();
void startWebServer();
void configureCam();
bool postFrame(WiFiClient wifiClient, String clientIp, int clientPort, String clientPathToCamFrameSave);

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

  // --- Configure Cam --- //
  configureCam();
  
  // --- Register Camera Stream --- //
  if ( !registerCam() ){
    Serial.println("    !!! Cam register failed -> reboot !!!");   
    ESP.restart();    
  }
  
  // --- Start Camera Server --- //
  startWebServer();
}

int counter = 0;
IPAddress emptyIP = IPAddress(0, 0, 0, 0);  

bool brokenRegister = false;

void loop() {

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
    } 
    Serial.println();   
  }

  //In every 30 seconds tries to SAVE FRAME
  else if(currentMillis - previousFrameSaveMillis >= intervalFrameSaveMillis){

    if(postFrame(wifiClient, clientIp, clientPort, clientPathToCamFrameSave)){      
      Serial.println("   POST /cam/save/frame was sent");      
      previousFrameSaveMillis = currentMillis;
    }else{
      Serial.println("   !!! Camera SAVE FRAME failed !!!");
    }
    Serial.println();    
  }

  delay(10);
}   
