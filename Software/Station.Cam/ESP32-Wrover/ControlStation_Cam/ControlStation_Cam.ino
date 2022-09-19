#include <WiFi.h>
#include <TimeLib.h>
#include <HTTPClient.h>
#include <Preferences.h>

//const char* ssid = "Central-Station-006";
//const char* password = "viragfal";
const char* ssid = "blabla2.4";
const char* password = "Elmebetegek Almaiban";

const String DEFAULT_CAMID = "default";
const String DEFAULT_CAMQUALITY = "SVGA";          // 96X96,QQVGA,QCIF,HQVGA,240X240,QVGA,CIF,HVGA,VGA,SVGA,XGA,HD,SXGA,UXGA
const String DEFAULT_CAMROTATE = "0";              //0, 1, 2, 3
unsigned long DEFAULT_INTERVALFRAME = 20000;       //save 1 frame / minute

const String DEFAULT_CLIENTIP = "192.168.0.104";   // REPLACE WITH YOUR Raspberry Pi IP ADDRESS !!! But it does not work
const String DEFAULT_CLIENTPORT = "80";

extern String camId = "";
extern String camQuality = "";       // 96X96,QQVGA,QCIF,HQVGA,240X240,QVGA,CIF,HVGA,VGA,SVGA,XGA,HD,SXGA,UXGA
extern String camRotate = "";        // 0, 1, 2, 3
extern String clientIp = "";         // REPLACE WITH YOUR Raspberry Pi IP ADDRESS !!! But it does not work
extern String clientPort = "";

const String clientPathToInfoTimestamp = "info/timeStamp";
const String clientPathToCamRegister = "cam/register";
//const String clientPathToCamFrameSave = "cam/save/frame/camId/" + camId;
String clientPathToCamFrameSave;

unsigned long previousReconnectMillis = 0;
unsigned long intervalReconnectMillis = 10000;

unsigned long previousRegisterMillis = 0;
unsigned long intervalRegisterMillis = 60000; // register / 60 seconds

unsigned long previousFrameMillis = 0;
extern unsigned long intervalFrameMillis = 20000; //save 1 frame / minute


HTTPClient http;
WiFiClient wifiClient;

Preferences camPref;
Preferences clientPref;

void startWebServer();
bool configureCam();
bool postFrame(WiFiClient wifiClient, String clientIp, String clientPort, String clientPathToCamFrameSave);

void setup() {
  
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  // --- Setup variables - Read Persistent data ---  
  setupVariables();
  
  Serial.println();
  Serial.print("MAC: ");
  Serial.println(WiFi.macAddress());
  Serial.println();

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
  
  //In every 30 seconds tries to take photo and SAVE FRAME
  }else if(currentMillis - previousFrameMillis >= intervalFrameMillis){

    clientPathToCamFrameSave = "cam/save/frame/camId/" + camId;

    if(postFrame(wifiClient, clientIp, clientPort, clientPathToCamFrameSave)){      
      Serial.println("   POST /cam/save/frame was sent");      
      previousFrameMillis = currentMillis;
    }else{
      Serial.println("   !!! Camera SAVE FRAME failed !!!");
      previousFrameMillis = currentMillis;
    }
    Serial.println();    
  }

  delay(10);
}   
