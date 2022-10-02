#include <ESP8266WiFi.h>        //WiFI related functionalities
#include <ESP8266WebServer.h>   //Handles HTTP protocols
#include <Preferences.h>

# define MAX_RECONNECTION_LOOP 50

const char* ssid = "Central-Station-006";
const char* password = "viragfal";

const int serverPort = 80;

// --- Default values for Preferences ---
const bool          DEFAULT_NEED_TO_RESET = false;

const String        DEFAULT_STATION_ID =               "default";
const unsigned long DEFAULT_INTERVAL_REPORT_MILLIS =   600000;      // 10 min
const unsigned long DEFAULT_INTERVAL_REGISTER_MILLIS = 600000;      // 20 min
const int           DEFAULT_SENSOR_TEMPHUM_OUT_GPIO = 0;
const int           DEFAULT_SENSOR_DISTANCE_ECHO_GPIO = 14;
const int           DEFAULT_SENSOR_DISTANCE_TRIG_GPIO = 12;


// --- Preferences values ---
extern unsigned long intervalReportMillis =   0;
extern unsigned long intervalRegisterMillis = 0;

extern bool   needToReset =     false;
extern String stationId =       "";

extern int    sensorTempHumOutGPIO = NULL;
extern int    sensorDistanceEchoGPIO = NULL;
extern int    sensorDistanceTrigGPIO = NULL;

// ---
bool isSensorPressure = false;
bool isSensorTempHum = false;
bool isSensorSonic = false;

int validSensorPressureValue;
int validSensorTempHumValue;
int validSensorDistanceValue;

//--- define functions ---
double getPressure();
struct BMP180_Struct getMovingAveragePressure(bool reset);

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
//WiFiServer server(80);

void setup() {
    Serial.begin(115200);

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
      Serial.println();
      Serial.println();
      Serial.println("!!! Must be restarted !!!");
      Serial.println();
      Serial.println();
      ESP.restart();
    }
    
    Serial.println(WiFi.localIP());
    Serial.println("==================");
    Serial.println();

    if( !configurePressureSensor()){
      Serial.println("!!! Not possible to configure Pressure Sensor. It will be ignored !!!");      
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
      Serial.println("!!! Not possible to configure HTTP server. The Module will be restarted !!!");
      Serial.println();
      Serial.println();
      delay(10000);
      ESP.restart();
    } 

    Serial.println();
    Serial.println();

    //Serial.setDebugOutput(true);

    Serial.printf("Web server started, open %s in a web browser\n", WiFi.localIP().toString().c_str());

}

int loopCounter = 0;
int numberOfMeasure = 3;
void loop() {

  int actualMeasure = loopCounter % numberOfMeasure;
  loopCounter++;

  ///////////////////////////////////
  //
  // BMP180 - Pressure + Temperature
  //
  ///////////////////////////////////
  validSensorPressureValue = 0;
  if(actualMeasure == 0 && isSensorPressure){    
    struct BMP180_Struct bmp180Result;
    bmp180Result = getMovingAveragePressure(false);

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
      Serial.println();
    }
    
  }

  ///////////////////////////////////
  //
  // DHT - Temperature + Humidity
  //
  ///////////////////////////////////
  validSensorTempHumValue = 0;
  if(actualMeasure == 1 && isSensorTempHum){    
    struct DHT_Struct dhtResult;
    dhtResult = getMovingAverageTempHum(false);
    
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
      Serial.println();
    }
  }

  ///////////////////////////////////
  //
  // HCSR04 - Distance
  //
  ///////////////////////////////////
  validSensorDistanceValue = 0;
  if(actualMeasure == 2 && isSensorSonic){    
    double hcsrResult;
    hcsrResult = getMovingAverageDistance(false);

    if(hcsrResult != NULL){
      validSensorDistanceValue++;
      Serial.print("Distance: "); 
      Serial.print(hcsrResult);
      Serial.print(" cm ");
    }
    
    if(validSensorDistanceValue){
      Serial.println();
    }
  }

//  if(validSensorPressureValue || validSensorTempHumValue || validSensorDistanceValue){
//    Serial.println();
//  }



/*  if(!connectToAccessPoint(true)){
    Serial.println("!!! Must be restarted !!!");
    Serial.println();
    Serial.println();
    ESP.restart();
  }
*/



  server.handleClient();          //Handle client requests









  
  //delay(10);
}
