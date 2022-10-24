#include <ArduinoJson.h>

//--- define functions ---
double getAvgTemp();
boolean isDecimal(String str);
boolean isInteger(String str);
void persistVariables();

void handleNotFound(){
  
  server.send(404, "text/plain", "404: Not found");

  Serial.println("!!! HTTP request was not found !!!");
  Serial.println();
}

void handleGetConfigure(){
  Serial.print("'GET /configure' request - ");

  String contentJson = 
    String("{") +
      "\"stationId\": \"" + stationId + "\"," + 
      
      "\"sensorTempHumOutGPIO\": \"" + sensorTempHumOutGPIO + "\"," + 
      "\"sensorDistanceTrigGPIO\": \"" + sensorDistanceTrigGPIO + "\"," + 
      "\"sensorDistanceEchoGPIO\": \"" + sensorDistanceEchoGPIO + "\"," + 

     "\"intervalReportMillis\": \"" + intervalReportMillis + "\"," + 
     "\"intervalRegisterMillis\": \"" + intervalRegisterMillis + "\"," +
     "\"intervalResetMillis\": \"" + intervalResetMillis + "\"," + 
     "\"intervalConnectionMillis\": \"" + intervalConnectionMillis + "\"," +     

    "}";
  
  server.send(200, "application/json", contentJson);
  
  Serial.println("Served");
  //Serial.println();
}

/*
 * Receives configuration data and updates the config if the data is correct
 * Retur:
 *    status code 201:
 *      {
 *        "success": true,
 *        "message": "OK"
 *      }
 *      
 *    status code 400:
 *      {
 *        "success": false,
 *        "message": "...~parsing json failed~..."
 *      }
 *      
 *    status code 400:
 *      {
 *        "success": false,
 *        "message": "Wrong parameter(s) privided",
 *        "data": 
 *          {
 *            "stationId": "Contains space",
 *            "sensorTempHumOutGPIO": "Wrong value. >15 or < 0 or not a number",
 *            "sensorDistanceTrigGPIO": "Wrong value. >15 or < 0 or not a number",
 *            "sensorDistanceEchoGPIO": "Wrong value. >15 or < 0 or not a number",
 *            "intervalReportMillis": "Wrong value. < 60000 or not a number",
 *            "intervalRegisterMillis": "Wrong value. < 60000 or not a number",
 *            "intervalResetMillis": "Wrong value. < 60000 or not a number",
 *            "intervalConnectionMillis": "Wrong value. < 60000 or not a number",
 *          }
 *      }
 */
void handlePostConfigure(){
  Serial.print("'POST /configure' request - ");

/*  String contentJson = 
    String("{") +
      "\"stationId\": \"" + stationId + "\"," + 
      
      "\"sensorTempHumOutGPIO\": \"" + sensorTempHumOutGPIO + "\"," + 
      "\"sensorDistanceTrigGPIO\": \"" + sensorDistanceTrigGPIO + "\"," + 
      "\"sensorDistanceEchoGPIO\": \"" + sensorDistanceEchoGPIO + "\"," + 

     "\"intervalReportMillis\": \"" + intervalReportMillis + "\"," + 
     "\"intervalRegisterMillis\": \"" + intervalRegisterMillis + "\"," + 

    "}";
  
  server.send(200, "application/json", contentJson);
  
  Serial.println("Served");
  //Serial.println();  
*/

  String resultJson; 
  String postBody = server.arg("plain");
  Serial.println(postBody);

  DynamicJsonDocument result(512);
  String buf;
  DynamicJsonDocument doc(512);
  DeserializationError error = deserializeJson(doc, postBody);
  if (error) {

    // if the file didn't open, print an error:
    String msg = error.c_str();
    Serial.print("Error parsing JSON: ");    
    Serial.println(msg); 

    result["success"] =  false;
    result["message"] = msg;
    serializeJson(result, buf);
    server.send(400, "application/json", buf);
 
  } else {

    int resultCode;
    boolean updateNeeded = false;
    
    String errorStationId = "";
    String errorSensorTempHumOutGPIO = "";
    String errorSensorDistanceTrigGPIO = "";
    String errorSensorDistanceEchoGPIO = "";
    String errorIntervalReportMillis = "";
    String errorIntervalRegisterMillis = "";
    String errorIntervalResetMillis = "";
    String errorIntervalConnectionMillis = "";
        
    JsonObject postObj = doc.as<JsonObject>();
    Serial.println("Json parameters are successfully parsed");

    //
    // stationId
    //
    const char* myStationId = postObj["stationId"];        
    if(myStationId){
      String strStationId = String(myStationId);
      strStationId.trim();
      if(strStationId.length() == 0 || strStationId.indexOf(" ") >= 0){
        errorStationId = "Wrong value: '" + strStationId + "'. " + ((strStationId.length() == 0) ? "Empty" : "Contains space");
        Serial.println(errorStationId);
      }else{
        stationId = strStationId;        
        updateNeeded = true;
      }
    }else{
      Serial.println("NO stationId modified");
    }

    //
    // sensorTempHumOutGPIO
    //
    const char* mySensorTempHumOutGPIO = postObj["sensorTempHumOutGPIO"];        
    if(mySensorTempHumOutGPIO){
      if(isInteger(String(mySensorTempHumOutGPIO))){
        int intSensorTempHumOutGPIO = atoi(mySensorTempHumOutGPIO);      
        if(intSensorTempHumOutGPIO < 0 || intSensorTempHumOutGPIO >= 15){
          errorSensorTempHumOutGPIO = "Wrong value: '" + String(mySensorTempHumOutGPIO) + "'. " + ((intSensorTempHumOutGPIO <= 0) ? " < 0" : " > 15");
          Serial.println(errorSensorTempHumOutGPIO);
        }else{
          sensorTempHumOutGPIO = intSensorTempHumOutGPIO;        
          updateNeeded = true;
        }
      }else{
        errorSensorTempHumOutGPIO = "Wrong value in 'sensorTempHumOutGPIO': '" + String(mySensorTempHumOutGPIO) + "' is NOT an Integer.";
        Serial.println(errorSensorTempHumOutGPIO);
      }
    }else{
      Serial.println("NO sensorTempHumOutGPIO modified");
    }

    //
    // sensorDistanceTrigGPIO
    //
    const char* mySensorDistanceTrigGPIO = postObj["sensorDistanceTrigGPIO"];        
    if(mySensorDistanceTrigGPIO){
      if(isInteger(String(mySensorDistanceTrigGPIO))){
        int intSensorDistanceTrigGPIO = atoi(mySensorDistanceTrigGPIO);      
        if(intSensorDistanceTrigGPIO < 0 || intSensorDistanceTrigGPIO >= 15){
          errorSensorDistanceTrigGPIO = "Wrong value: '" + String(mySensorDistanceTrigGPIO) + "'. " + ((intSensorDistanceTrigGPIO <= 0) ? " < 0" : " > 15");
          Serial.println(errorSensorDistanceTrigGPIO);
        }else{
          sensorDistanceTrigGPIO = intSensorDistanceTrigGPIO;        
          updateNeeded = true;
        }
      }else{
        errorSensorDistanceTrigGPIO = "Wrong value in 'sensorDistanceTrigGPIO': '" + String(mySensorDistanceTrigGPIO) + "' is NOT an Integer.";
        Serial.println(errorSensorDistanceTrigGPIO);
      }
    }else{
      Serial.println("NO sensorDistanceTrigGPIO modified");
    }

    //
    // sensorDistanceTrigGPIO
    //
    const char* mySensorDistanceEchoGPIO = postObj["sensorDistanceEchoGPIO"];        
    if(mySensorDistanceEchoGPIO){
      if(isInteger(String(mySensorDistanceEchoGPIO))){
        int intSensorDistanceEchoGPIO = atoi(mySensorDistanceEchoGPIO);      
        if(intSensorDistanceEchoGPIO < 0 || intSensorDistanceEchoGPIO >= 15){
          errorSensorDistanceEchoGPIO = "Wrong value: '" + String(mySensorDistanceEchoGPIO) + "'. " + ((intSensorDistanceEchoGPIO <= 0) ? " < 0" : " > 15");
          Serial.println(errorSensorDistanceEchoGPIO);
        }else{
          sensorDistanceEchoGPIO = intSensorDistanceEchoGPIO;        
          updateNeeded = true;
        }
      }else{
        errorSensorDistanceTrigGPIO = "Wrong value in 'sensorDistanceEchoGPIO': '" + String(mySensorDistanceEchoGPIO) + "' is NOT an Integer.";
        Serial.println(errorSensorDistanceEchoGPIO);
      }
    }else{
      Serial.println("NO sensorDistanceEchoGPIO modified");
    }

    //
    // intervalReportMillis
    //
    const char* myIntervalReportMillis = postObj["intervalReportMillis"];        
    if(myIntervalReportMillis){
      if(isInteger(String(myIntervalReportMillis))){
        unsigned long ulIntervalReportMillis = strtoul(myIntervalReportMillis, NULL, 0);      
        if(ulIntervalReportMillis < 60000){
          errorIntervalReportMillis = "Wrong value: '" + String(myIntervalReportMillis) + "'. " + " < 60000 (1 minute)";
          Serial.println(errorIntervalReportMillis);
        }else{
          intervalReportMillis = ulIntervalReportMillis;        
          updateNeeded = true;
        }
      }else{
        errorIntervalReportMillis = "Wrong value in 'intervalReportMillis': '" + String(myIntervalReportMillis) + "' is NOT a Long.";
        Serial.println(errorIntervalReportMillis);
      }
    }else{
      Serial.println("NO intervalReportMillis modified");
    }

    //
    // intervalRegisterMillis
    //
    const char* myIntervalRegisterMillis = postObj["intervalRegisterMillis"];        
    if(myIntervalRegisterMillis){
      if(isInteger(String(myIntervalRegisterMillis))){
        unsigned long ulIntervalRegisterMillis = strtoul(myIntervalRegisterMillis, NULL, 0);      
        if(ulIntervalRegisterMillis < 60000){
          errorIntervalRegisterMillis = "Wrong value: '" + String(myIntervalRegisterMillis) + "'. " + " < 60000 (1 minute)";
          Serial.println(errorIntervalRegisterMillis);
        }else{
          intervalRegisterMillis = ulIntervalRegisterMillis;        
          updateNeeded = true;
        }
      }else{
        errorIntervalRegisterMillis = "Wrong value in 'intervalRegisterMillis': '" + String(myIntervalRegisterMillis) + "' is NOT a Long.";
        Serial.println(errorIntervalRegisterMillis);
      }
    }else{
      Serial.println("NO intervalRegisterMillis modified");
    }

    //
    // intervalResetMillis
    //
    const char* myIntervalResetMillis = postObj["intervalResetMillis"];        
    if(myIntervalResetMillis){
      if(isInteger(String(myIntervalResetMillis))){
        unsigned long ulIntervalResetMillis = strtoul(myIntervalResetMillis, NULL, 0);      
        if(ulIntervalResetMillis < 60000){
          errorIntervalResetMillis = "Wrong value: '" + String(myIntervalResetMillis) + "'. " + " < 60000 (1 minute)";
          Serial.println(errorIntervalResetMillis);
        }else{
          intervalResetMillis = ulIntervalResetMillis;        
          updateNeeded = true;
        }
      }else{
        errorIntervalResetMillis = "Wrong value in 'intervalResetMillis': '" + String(myIntervalResetMillis) + "' is NOT a Long.";
        Serial.println(errorIntervalResetMillis);
      }
    }else{
      Serial.println("NO intervalResetMillis modified");
    }

    //
    // intervalConnectionMillis
    //
    const char* myIntervalConnectionMillis = postObj["intervalConnectionMillis"];        
    if(myIntervalConnectionMillis){
      if(isInteger(String(myIntervalConnectionMillis))){
        unsigned long ulIntervalConnectionMillis = strtoul(myIntervalConnectionMillis, NULL, 0);      
        if(ulIntervalConnectionMillis < 60000){
          errorIntervalConnectionMillis = "Wrong value: '" + String(myIntervalConnectionMillis) + "'. " + " < 60000 (1 minute)";
          Serial.println(errorIntervalConnectionMillis);
        }else{
          intervalConnectionMillis = ulIntervalConnectionMillis;        
          updateNeeded = true;
        }
      }else{
        errorIntervalConnectionMillis = "Wrong value in 'intervalConnectionMillis': '" + String(myIntervalConnectionMillis) + "' is NOT a Long.";
        Serial.println(errorIntervalConnectionMillis);
      }
    }else{
      Serial.println("NO intervalConnectionMillis modified");
    }

    // If there was at least 1 wrong (existing) parameter
    if(errorStationId.length()!=0 || errorSensorTempHumOutGPIO.length() != 0 || errorSensorDistanceTrigGPIO.length() != 0 || errorIntervalReportMillis.length() != 0 || errorIntervalRegisterMillis.length() != 0 || errorIntervalResetMillis.length() != 0 || errorIntervalConnectionMillis.length() != 0){
      resultCode = 400;    
      if(errorStationId.length()!=0){
        result["success"] =  false;
        result["message"] = "Wrong parameter(s) provided";
        result["data"]["stationId"] = errorStationId;      
      }
      if(errorSensorTempHumOutGPIO.length() != 0){
        result["success"] =  false;
        result["message"] = "Wrong parameter(s) provided";
        result["data"]["sensorTempHumOutGPIO"] = errorSensorTempHumOutGPIO;      
      }
      if(errorSensorDistanceTrigGPIO.length() != 0){
        result["success"] =  false;
        result["message"] = "Wrong parameter(s) provided";
        result["data"]["sensorDistanceTrigGPIO"] = errorSensorDistanceTrigGPIO;      
      }
      if(errorIntervalReportMillis.length() != 0){
        result["success"] =  false;
        result["message"] = "Wrong parameter(s) provided";
        result["data"]["intervalReportMillis"] = errorIntervalReportMillis;      
      }
      if(errorIntervalRegisterMillis.length() != 0){
        result["success"] =  false;
        result["message"] = "Wrong parameter(s) provided";
        result["data"]["intervalRegisterMillis"] = errorIntervalRegisterMillis;      
      }
      if(errorIntervalResetMillis.length() != 0){
        result["success"] =  false;
        result["message"] = "Wrong parameter(s) provided";
        result["data"]["intervalResetMillis"] = errorIntervalResetMillis;      
      }      
      if(errorIntervalConnectionMillis.length() != 0){
        result["success"] =  false;
        result["message"] = "Wrong parameter(s) provided";
        result["data"]["intervalConnectionMillis"] = errorIntervalConnectionMillis;      
      }        

    // No error in the existing provided parameters
    }else if(updateNeeded){
      resultCode = 201;    
      result["success"] =  true;
      result["message"] = "OK";

      persistVariables();

    // No existing parameter was provided
    }else{
      resultCode = 400;
      result["success"] =  false;
      result["message"] = "No existing parameter was provided";
    }
    
    serializeJson(result, buf);
    server.send(resultCode, "application/json", buf);  
  }
  Serial.println("Served");
  
}

void handleGetPressure(){
  Serial.print("'GET /pressure' request - ");

  struct BMP180_Struct bmp180Result = getPressTemp(false); //getSampleOfPressTemp(1);
  double pressure = bmp180Result.pressure;
  
  String contentJson = 
    String("{") +
      "\"pressure\": \"" + String(pressure) + "\"" + 
    "}";
  
  server.send(200, "application/json", contentJson);
  
  Serial.println("Served");
}

void handleGetTemperature(){
  Serial.print("'GET /tepmerature' request - ");

  struct BMP180_Struct bmp180Result = getSampleOfPressTemp(1); //getPressTemp(false);
  double temp1 = bmp180Result.temperature;

  struct DHT_Struct dhtResult = getSampleOfTempHum(1);
  double temp2 = dhtResult.temperature;

  double temperature = getAvgTemp(temp1, temp2);
  
  String contentJson = 
    String("{") +
      "\"temperature\": \"" + String(temperature) + "\"" + 
    "}";
  
  server.send(200, "application/json", contentJson);
  
  Serial.println("Served");
}

void handleGetHumidity(){
  Serial.print("'GET /humidity' request - ");

  struct DHT_Struct dhtResult = getTempHum(false); //getSampleOfTempHum(1);

  String contentJson = 
    String("{") +
      "\"humidity\": \"" + String(dhtResult.humidity) + "\"" + 
    "}";
  
  server.send(200, "application/json", contentJson);
  
  Serial.println("Served");
  Serial.println();
}

void handleGetDistance(){
  Serial.print("'GET /distance' request - ");

  double distance = getDistanceByDuration(getDuration(false)); //getSampleOfDistance(1);

  String contentJson = 
    String("{") +
      "\"distance\": \"" + String(distance) + "\"" + 
    "}";
  
  server.send(200, "application/json", contentJson);
  
  Serial.println("Served");
}

void handleGetAllActual(){
  Serial.print("'GET /all/actual' request - ");

  //===
  struct BMP180_Struct bmp180Result = getPressTemp(false); //getSampleOfPressTemp(1);
  double pressure = bmp180Result.pressure;
  //---  
  double temp1 = bmp180Result.temperature;

  struct DHT_Struct dhtResult = getTempHum(false);
  double temp2 = dhtResult.temperature;

  double temperature = getAvgTemp(temp1, temp2);
  //---
  double humidity = dhtResult.humidity;
  //---
  double distance = getDistanceByDuration(getDuration(false));
  //===
  
  String contentJson = 
    String("{") +
      "\"temperature\": \"" + String(temperature) + "\"," + 
      "\"humidity\": \"" + String(humidity) + "\"," + 
      "\"pressure\": \"" + String(pressure) + "\"," + 
      "\"distance\": \"" + String(distance) + "\"," + 
    "}";
  
  server.send(200, "application/json", contentJson);
  
  Serial.println("Served");
}

void handleGetAllAggregated(){
  Serial.print("'GET /all/aggregated' request - ");

  String levelValue = (avgHcsrDist != NULL) ? String(avgHcsrDist) : "";
  String pressureValue = (avgBmpPress != NULL) ? String(avgBmpPress) : "";
  String humidityValue = (avgDhtHum != NULL) ? String(avgDhtHum) : "";

  double temp1 = avgBmpTemp;
  double temp2 = avgDhtTemp;   
  double avgTemp = getAvgTemp(temp1, temp2);
  
  String temperatureValue = (avgTemp != NULL) ? String(avgTemp) : "";
  
  String contentJson = 
    String("{") +
      "\"temperature\": \"" + temperatureValue + "\"," + 
      "\"humidity\": \"" + humidityValue + "\"," + 
      "\"pressure\": \"" + pressureValue + "\"," + 
      "\"distance\": \"" + levelValue + "\"," + 
    "}";
  
  server.send(200, "application/json", contentJson);
  
  Serial.println("Served");
}

bool configureHttpServer(){
  bool ret = true;
  
  server.on("/configure", HTTP_GET, handleGetConfigure);
  server.on("/configure", HTTP_POST, handlePostConfigure);

  server.on("/pressure", HTTP_GET, handleGetPressure);
  server.on("/temperature", HTTP_GET, handleGetTemperature);
  server.on("/humidity", HTTP_GET, handleGetHumidity);
  server.on("/distance", HTTP_GET, handleGetDistance);

  server.on("/all/actual", HTTP_GET, handleGetAllActual);
  server.on("/all/aggregated", HTTP_GET, handleGetAllAggregated);

  server.onNotFound(handleNotFound);
  
  server.begin();                  //Start server

  Serial.println("HTTP server started");
  
  return ret;
}
