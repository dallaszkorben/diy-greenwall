#include <ESP8266WiFi.h>        //WiFI related functionalities
#include <ESP8266WebServer.h>   //Handles HTTP protocols
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <Preferences.h>

#define MAX_RECONNECTION_LOOP 50
#define LED_INITIATE 0
#define LED_COMMUNICATE 1
#define LED_HEALTHY 2
#define LED_ERROR 3

int ledStatus = LED_INITIATE;
/*
 * Call services:
 *    curl -s --request GET http://192.168.50.101:80/all/aggregated
 *    curl -s --request GET http://192.168.50.101:80/all/actual
 *    curl -s --request GET http://192.168.50.101:80/pressure
 *    curl -s --request GET http://192.168.50.101:80/temperature
 *    curl -s --request GET http://192.168.50.101:80/humidity
 *    curl -s --request GET http://192.168.50.101:80/distance
 *    curl -s --request GET http://192.168.50.101:80/duration
 *    
 *    curl -s --request POST --header "Content-Type: application/json" http://192.168.50.101:80/configure --data {"stationId": "S02"} 
 * 
 * Continously read the values from this module on the same network:
 *    for i in $(seq 1 10000); do echo -n "$i `date -I'seconds'`: "; result=`curl -s -w "%{http_code}"  --max-time 20 http://192.168.50.101:80/all/aggregated `; code=`echo $result|grep -Po "\\d{3}$"`; if [[ $code == "200" ]] ; then echo $result; else echo $code; continue; fi; sleep 20; done\
 * 
 * Continously read the duration from this module on the same network:
 *    watch 'curl -s --header "Content-Type: application/json" --request GET http://192.168.50.112:80/duration | grep -oP "duration\":\"\d+[.]\d+"'
 */
const String version = "CS-0.0.3";

const char* ssid = "Central-Station-006";
const char* password = "viragfal";
const int serverPort = 80;

// --- Default values for Preferences ---
const bool          DEFAULT_NEED_TO_REPORT = false;
const bool          DEFAULT_NEED_TO_RESET = false;

const String        DEFAULT_CLIENT_IP   = "192.168.0.104"; 
const String        DEFAULT_CLIENT_PORT = "80";

const String        DEFAULT_CLIENT_PATH_TO_REGISTER = "sensor/register";
const String        DEFAULT_CLIENT_PATH_TO_REPORT   = "sensor/add";
const String        DEFAULT_CLIENT_PATH_TO_INFO_TIMESTAMP = "info/timeStamp";

const String        DEFAULT_STATION_ID                = "default";
const unsigned long DEFAULT_INTERVAL_REPORT_MILLIS    = 600300;              // 10 min
const unsigned long DEFAULT_INTERVAL_REGISTER_MILLIS  = 120600;              // 2 min
const unsigned long DEFAULT_INTERVAL_RESET_MILLIS     = 3600900;             // 60 min
const unsigned long DEFAULT_INTERVAL_CONNECTION_MILLIS= 60200;               // 1 min
const int           DEFAULT_SENSOR_TEMPHUM_OUT_GPIO   = 0;
const int           DEFAULT_SENSOR_DISTANCE_ECHO_GPIO = 14;
const int           DEFAULT_SENSOR_DISTANCE_TRIG_GPIO = 12;

const double        DEFAULT_SENSOR_DISTANCE_PARAMETER_A = 0.0;
const double        DEFAULT_SENSOR_DISTANCE_PARAMETER_B = 0.017171;
const double        DEFAULT_SENSOR_DISTANCE_PARAMETER_C = 0.0;

// --- Preferences values ---
unsigned long intervalReportMillis      = 0;
long intervalRegisterMillis    = 0;
unsigned long intervalResetMillis       = 0;
unsigned long intervalConnectionMillis  = 0;

bool   needToReset  =     false;
bool   needToReport =     false;
String stationId    =     "";

int    sensorTempHumOutGPIO   = NULL;
int    sensorDistanceEchoGPIO = NULL;
int    sensorDistanceTrigGPIO = NULL;

double  sensorDistanceParA = 0.0;
double  sensorDistanceParB = 0.0;
double  sensorDistanceParC = 0.0;

String clientIp   = "";  
String clientPort = "";

String clientPathToRegister;
String clientPathToReport;
String clientPathToInfoTimestamp;

// ---

double avgBmpTempCounter  = 0;
double avgBmpPressCounter  = 0;
double avgBmpTemp     = NULL;
double avgBmpPress    = NULL;
bool isSensorBmp;

double avgDhtTempCounter  = 0;
double avgDhtHumCounter  = 0;
double avgDhtTemp     = NULL;
double avgDhtHum      = NULL;

double avgHcsrCounter = 0;
double avgHcsrDist    = NULL;

//--- define functions ---
bool registerSensorStation(bool needToPrint);
bool reportSensors(bool needToPrint);

void ledSignalInitiate();
void ledSignalNetworkError();
void ledSignalCommunicate();
void ledSignalHealthy();

double getAvgTemp();
void setupVariables();
void wifiEvent(WiFiEvent_t event);
bool connectToAccessPoint(bool needToPrint);

bool configureDistanceSensor();
double getDuration(bool needToPrint);
double getDistanceByDuration(double duration);
double getSampleOfDistance(int sample);
double add1SampleToMovingAverageDistance(bool reset);

bool configureTempHumSensor();
struct DHT_Struct getTempHum(bool needToPrint);
struct DHT_Struct getSampleOfTempHum(int sample);
struct DHT_Struct add1SampleToMovingAverageTempHum(bool reset);

bool configurePressTempSensor();
struct BMP180_Struct getPressTemp(bool needToPrint);
struct BMP180_Struct getSampleOfPressTemp(int sample);
struct BMP180_Struct add1SampleToMovingAveragePressTemp(bool reset);

bool configureHttpServer();

Preferences stationPref;

ESP8266WebServer server(serverPort); //Server on port 80
WiFiClient client;
HTTPClient http;

struct DHT_Struct {
  double humidity;
  double temperature;
};

struct BMP180_Struct {
  double pressure;
  double temperature;
};

int loopCounter;
int numberOfMeasure;
unsigned long previousConnectionMillis;
long previousRegisterMillis;
unsigned long previousReportMillis;
unsigned long currentMillis;

void setup() {
    Serial.begin(115200);
    Serial.println("\n");
    delay(2000);

    pinMode(LED_BUILTIN, OUTPUT);  
    ledSignalInitiate();

    // --- Read Persistent Data --- //
    setupVariables();

    Serial.println();
    Serial.println("===== Connect to acceess Point =====");  
    Serial.println("Module information:");
    Serial.print("   MAC: ");
    Serial.println(WiFi.macAddress());
    
    //WiFi.disconnect();
    delay(1000);
    WiFi.onEvent(wifiEvent);
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);    
    Serial.print("   SSID: ");
    Serial.println(WiFi.SSID());
    Serial.print("   RSSI: ");
    Serial.println(WiFi.RSSI());

    // --- Connect to Access Point --- ///
    if(!connectToAccessPoint(false)){
      ledSignalInitiate();
      Serial.println();
      Serial.println();
      Serial.println("!!! Must be restarted !!!");
      Serial.println();
      Serial.println();
      delay(10000);
      ESP.restart();
    }
    WiFi.setAutoReconnect(true);
    WiFi.persistent(true);
    WiFi.setSleep(false);

    Serial.print("   IP address: ");
    Serial.println(WiFi.localIP());
    Serial.println("====================================");
    Serial.println();

    // --- Sync Time --- //
    if( !syncTime() ){
      Serial.println("    !!! Sync Time failed -> reboot !!!");  
      delay(10000); 
      ESP.restart();
    }

    Serial.println("======== Configure Sensors =========");

    // --- Configure Pressure Temperature sensor --- //
    if( !configurePressTempSensor()){
      Serial.println("!!! Not possible to configure Pressure/Temperature Sensor. It will be ignored !!!");      
      Serial.println();
    }

    // --- Configure Temperature Humidity sensor --- //
    if( !configureTempHumSensor()){
      Serial.println("!!! Not possible to configure Temperature/Humidity Sensor. It will be ignored !!!");
      Serial.println();
    }

    // --- Configure Distance sensor --- //
    if( !configureDistanceSensor()){
      Serial.println("!!! Not possible to configure Sonic Sensor. It will be ignored !!!");
      Serial.println();
    }
    Serial.println("====================================");
    Serial.println();

    // --- Configure HTTP server --- //
    Serial.println("========= Start WEB server =========");
    if( !configureHttpServer()){
      ledSignalNetworkError();
      Serial.println("!!! Not possible to configure HTTP server. The Module will be restarted !!!");
      Serial.println();
      Serial.println();
      delay(10000);
      ESP.restart();
    } 
    Serial.printf("Web server started, open %s in a web browser\n", WiFi.localIP().toString().c_str());
    Serial.println("====================================");
    Serial.println();

    ledSignalHealthy();

    //Serial.setDebugOutput(true);

  loopCounter = 0;
  numberOfMeasure = 30;
  previousConnectionMillis = millis();
  previousRegisterMillis = -(intervalRegisterMillis); //Reason to fill up with the -interval length is to take sample at the first time in the loop
  previousReportMillis = millis();                    
  currentMillis = millis();                           
}

void loop() {
  
  int actualMeasureLoop = loopCounter % numberOfMeasure; //range: 0-29. In the first 0. 1. 2. loop will be taken 1-1 sample
  loopCounter++;

  ///////////////////////////////////
  // BMP180 - Pressure + Temperature
  ///////////////////////////////////
  // Tries to take Pressure/Temperture sample in every 0. loop
  if(actualMeasureLoop == 0){    
    struct BMP180_Struct bmp180Result = add1SampleToMovingAveragePressTemp(false);
  }
  
  ///////////////////////////////////
  // DHT - Temperature + Humidity
  ///////////////////////////////////
  // Tries to take Temperature+mumidity sample in every 1. loop
  if(actualMeasureLoop == 1){    
    struct DHT_Struct dhtResult = add1SampleToMovingAverageTempHum(false);
  }
  
  ///////////////////////////////////
  // HCSR04 - Distance
  ///////////////////////////////////
  // Take Distance sample in every 2. loop
  if(actualMeasureLoop == 2){    
    double hcsrResult = add1SampleToMovingAverageDistance(false);
  }

  currentMillis = millis();

  // --------------------------------------------
  //
  //In every 60 seconds (1min) checks if there is connection
  //
  // --------------------------------------------
  if(currentMillis - previousConnectionMillis >= intervalConnectionMillis){
    ledSignalCommunicate();
    if(!connectToAccessPoint(false)){
      Serial.println("!!! Must be restarted !!!");
      Serial.println();
      Serial.println();
      ESP.restart();
    }else{
//      Serial.print("Connection is OK: ");
//      Serial.println(WiFi.localIP());
    }
    ledSignalHealthy();
    previousConnectionMillis = currentMillis;     
  }
  
  // --------------------------------------------
  //
  //In every 120 seconds (2min) tries to REGISTER
  //
  // --------------------------------------------
  if(currentMillis - previousRegisterMillis >= intervalRegisterMillis){
    ledSignalCommunicate();   
    if ( registerSensorStation(false) ){
      Serial.print("Sensor Station was registered at "); 
      Serial.println(getOffsetDateString());
Serial.print(avgHcsrDist);      
Serial.print(" = ");      
Serial.println(avgHcsrCounter);       
      previousRegisterMillis = currentMillis;      
    }else{
      ledSignalNetworkError();
      Serial.print("!!! Sensor Station register failed at");
      Serial.println(getOffsetDateString());
      delay(1000);
    } 
    ledSignalHealthy();
  }
  
  // --------------------------------------------
  //
  //In every 600 seconds (10min) tries to REPORT
  //
  // --------------------------------------------

//  Serial.print(currentMillis); 
//  Serial.print("-");
//  Serial.print(previousReportMillis); 
//  Serial.print(">=");
//  Serial.println(intervalReportMillis); 
    
  if(needToReport && (currentMillis - previousReportMillis >= intervalReportMillis)){

    ledSignalCommunicate();

Serial.print(avgHcsrDist);      
Serial.print(" = ");      
Serial.print(avgHcsrCounter);    
Serial.println("   ");      
    
    if ( reportSensors(false) ){
      Serial.print("Sensors was reported at "); 
      Serial.println(getOffsetDateString());
      previousReportMillis = currentMillis;
      delay(5000);      
    }else{
      ledSignalNetworkError();
      Serial.print("!!! Sensors report failed at: ");   
      Serial.println(getOffsetDateString());
      delay(2000);
    } 
    ledSignalHealthy();
    
//    Serial.println();   
  }

  // --------------------------------------------
  //
  //In every 3600 seconds (1hour) RESTART
  //
  // --------------------------------------------
  if(currentMillis >= intervalResetMillis){
    Serial.println();
    Serial.println("===========================");
    Serial.println("");    
    Serial.println("      !!!   RESET   !!!    ");
    Serial.println("");    
    Serial.println("===========================");
    Serial.println();
    ESP.reset();
  }  
  
  server.handleClient();          //Handle client requests
  
  delay(10);
}
