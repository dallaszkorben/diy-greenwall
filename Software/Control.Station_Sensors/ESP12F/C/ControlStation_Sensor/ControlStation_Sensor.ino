#include <ESP8266WiFi.h>        //WiFI related functionalities
#include <ESP8266WebServer.h>   //Handles HTTP protocols
#include <Preferences.h>

#define MAX_RECONNECTION_LOOP 50
#define LED_INITIATE 0
#define LED_COMMUNICATE 1
#define LED_HEALTHY 2
#define LED_ERROR 3

int ledStatus = LED_INITIATE;
/*
 * Call services:
 *    curl -s http://192.168.50.101:80/all/aggregated
 *    curl -s http://192.168.50.101:80/all/actual
 *    curl -s http://192.168.50.101:80/all/pressure
 *    curl -s http://192.168.50.101:80/all/temperature
 *    curl -s http://192.168.50.101:80/all/humidity
 *    curl -s http://192.168.50.101:80/all/distance
 *    
 *    curl -s http://192.168.50.101:80/configure
 * 
 * Continously read the values from this module on the same network 
 *    for i in $(seq 1 10000); do echo -n "$i `date -I'seconds'`: "; result=`curl -s -w "%{http_code}"  --max-time 20 http://192.168.50.101:80/all/aggregated `; code=`echo $result|grep -Po "\\d{3}$"`; if [[ $code == "200" ]] ; then echo $result; else echo $code; continoue; fi; sleep 20; done
 * 
 */

const char* ssid = "Central-Station-006";
const char* password = "viragfal";
const int serverPort = 80;

// --- Default values for Preferences ---
const bool          DEFAULT_NEED_TO_RESET = false;

const String        DEFAULT_CLIENT_IP   = "192.168.0.104"; 
const String        DEFAULT_CLIENT_PORT = "80";

const String        DEFAULT_CLIENT_PATH_TO_REGISTER = "sensor/register";
const String        DEFAULT_CLIENT_PATH_TO_REPORT   = "sensor/add";

const String        DEFAULT_STATION_ID                = "default";
const unsigned long DEFAULT_INTERVAL_REPORT_MILLIS    = 60300;  //600000;    // 10 min
const unsigned long DEFAULT_INTERVAL_REGISTER_MILLIS  = 120600;              // 2 min
const unsigned long DEFAULT_INTERVAL_RESET_MILLIS     = 1800900;             // 30 min
const unsigned long DEFAULT_INTERVAL_CONNECTION_MILLIS= 60200;               // 1 min
const int           DEFAULT_SENSOR_TEMPHUM_OUT_GPIO   = 0;
const int           DEFAULT_SENSOR_DISTANCE_ECHO_GPIO = 14;
const int           DEFAULT_SENSOR_DISTANCE_TRIG_GPIO = 12;

// --- Preferences values ---
unsigned long intervalReportMillis      = 0;
unsigned long intervalRegisterMillis    = 0;
unsigned long intervalResetMillis       = 0;
unsigned long intervalConnectionMillis  = 0;

bool   needToReset  =     false;
String stationId    =     "";

int    sensorTempHumOutGPIO   = NULL;
int    sensorDistanceEchoGPIO = NULL;
int    sensorDistanceTrigGPIO = NULL;

String clientIp   = "";  
String clientPort = "";

String clientPathToRegister;
String clientPathToReport;

// ---
bool isSensorPressure = false;
bool isSensorTempHum  = false;
bool isSensorSonic    = false;

int validSensorPressureValue;
int validSensorTempHumValue;
int validSensorDistanceValue;

double avgBmpCounter  = 0;
double avgBmpTemp     = NULL;
double avgBmpPress    = NULL;

double avgDhtCounter  = 0;
double avgDhtTemp     = NULL;
double avgDhtHum      = NULL;

double avgHcsrCounter = 0;
double avgHcsrDist    = NULL;

//--- define functions ---
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

struct DHT_Struct {
  double humidity;
  double temperature;
};

struct BMP180_Struct {
  double pressure;
  double temperature;
};

ESP8266WebServer server(serverPort); //Server on port 80

void setup() {
    Serial.begin(115200);
    Serial.println("\n");
    delay(2000);

    pinMode(LED_BUILTIN, OUTPUT);  
    ledSignalInitiate();

    // --- Read Persistent Data --- //
    setupVariables();

    Serial.println();
    Serial.println("==================");
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

    Serial.print("   IP address: ");
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
    
    Serial.println(WiFi.localIP());
    Serial.println("==================");
    Serial.println();

    if( !configurePressTempSensor()){
      Serial.println("!!! Not possible to configure Pressure/Temperature Sensor. It will be ignored !!!");      
      Serial.println();
      Serial.println();
      isSensorPressure = false;
    }else{
      isSensorPressure = true;
    }

    if( !configureTempHumSensor()){
      Serial.println("!!! Not possible to configure Temperature/Humidity Sensor. It will be ignored !!!");
      Serial.println();
      Serial.println();
      isSensorTempHum = false;
    }else{
      isSensorTempHum = true;
    }

    if( !configureDistanceSensor()){
      Serial.println("!!! Not possible to configure Sonic Sensor. It will be ignored !!!");
      Serial.println();
      Serial.println();
      isSensorSonic = false;
    }else{
      isSensorSonic = true;
    }

    if( !configureHttpServer()){
      ledSignalNetworkError();
      Serial.println("!!! Not possible to configure HTTP server. The Module will be restarted !!!");
      Serial.println();
      Serial.println();
      delay(10000);
      ESP.restart();
    } 

    Serial.println();
    Serial.println();

    //Serial.setDebugOutput(true);

    Serial.println("==================");
    Serial.printf("Web server started, open %s in a web browser\n", WiFi.localIP().toString().c_str());

    ledSignalHealthy();
}

int loopCounter = 0;
int numberOfMeasure = 30;
unsigned long previousConnectionMillis = millis();
unsigned long previousRegisterMillis = millis();  //Reason to fill up with the actual time is to take sample at the first time in the loop
unsigned long previousReportMillis = millis();    //Reason to fill up with the actual time is to take sample at the first time in the loop
unsigned long currentMillis = millis();           //Reason to fill up with the actual time is to take sample at the first time in the loop

void loop() {
  
  int actualMeasure = loopCounter % numberOfMeasure; //range: 0-29. In the first 0. 1. 2. loop will be taken 1-1 sample
  loopCounter++;

  ///////////////////////////////////
  //
  // BMP180 - Pressure + Temperature
  //
  ///////////////////////////////////
  validSensorPressureValue = 0;
  
  // Take Pressure/Temperture sample in every 0. loop
  if(actualMeasure == 0 && isSensorPressure){    
    struct BMP180_Struct bmp180Result;
    bmp180Result = add1SampleToMovingAveragePressTemp(false);
/*
    if(bmp180Result.temperature != NULL){
      validSensorPressureValue++;
      Serial.print("Temperature: "); 
      Serial.print(bmp180Result.temperature);
      Serial.print(" °C, ");
    }
    if(bmp180Result.pressure != NULL){
      validSensorPressureValue++;
      Serial.print("Pressure: "); 
      Serial.print(bmp180Result.pressure);
      Serial.print(" Pa, ");
    }
    if(validSensorPressureValue){  
      Serial.print("   (");
      Serial.print(avgBmpCounter);
      Serial.print(")");    
      Serial.println();
    }
*/    
  }

  ///////////////////////////////////
  //
  // DHT - Temperature + Humidity
  //
  ///////////////////////////////////
  validSensorTempHumValue = 0;
  
  // Take Temperature+mumidity sample in every 1. loop
  if(actualMeasure == 1 && isSensorTempHum){    
    struct DHT_Struct dhtResult;
    dhtResult = add1SampleToMovingAverageTempHum(false);
 /*   
    if(dhtResult.temperature != NULL){
      validSensorTempHumValue++;
      Serial.print("Temperature: "); 
      Serial.print(dhtResult.temperature);
      Serial.print(" °C, ");
    }
    if(dhtResult.humidity != NULL){
      validSensorTempHumValue++;
      Serial.print("Humidity: "); 
      Serial.print(dhtResult.humidity);
      Serial.print(" %, ");
    }
    
    if(validSensorTempHumValue){
      Serial.print("   (");
      Serial.print(avgDhtCounter);
      Serial.print(")");    

      Serial.println();
    }
*/    
  }

  ///////////////////////////////////
  //
  // HCSR04 - Distance
  //
  ///////////////////////////////////
  validSensorDistanceValue = 0;
    
    // Take Distance sample in every 2. loop
    if(actualMeasure == 2 && isSensorSonic){    
    double hcsrResult;
    hcsrResult = add1SampleToMovingAverageDistance(false);
/*
    if(hcsrResult != NULL){
      validSensorDistanceValue++;
      Serial.print("Distance: "); 
      Serial.print(hcsrResult);
      Serial.print(" cm ");
    }
    
    if(validSensorDistanceValue){
      Serial.print("   (");
      Serial.print(avgHcsrCounter);
      Serial.print(")");    

      Serial.println();      
    }
*/    
  }

//  if(validSensorPressureValue || validSensorTempHumValue || validSensorDistanceValue){
//    Serial.println();
//  }

  currentMillis = millis();
  // --------------------------------------------
  //
  //In every 120 seconds (2min) tries to REGISTER
  //
  // --------------------------------------------
  if(currentMillis - previousRegisterMillis >= intervalRegisterMillis){
    ledSignalCommunicate();
//    Serial.println();    
    if ( registerSensorStation(false) ){
//      Serial.println("Sensor Station was registered"); 
      previousRegisterMillis = currentMillis;      
    }else{
      ledSignalNetworkError();
      Serial.println("!!! Sensor Station register failed !!!");   
      delay(1000);
    } 
    ledSignalHealthy();
//    Serial.println();   
  }

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
  //In every 600 seconds (10min) tries to REPORT
  //
  // --------------------------------------------
  if(currentMillis - previousReportMillis >= intervalReportMillis){
//    Serial.println(); 

    ledSignalCommunicate();
    if ( reportSensors(false) ){
      Serial.println("Sensors was reported"); 
      previousReportMillis = currentMillis;
      delay(5000);      
    }else{
      ledSignalNetworkError();
      Serial.println("!!! Sensors report failed !!!");   
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
