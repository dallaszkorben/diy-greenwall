
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

    "}";
  
  server.send(200, "application/json", contentJson);
  
  Serial.println("Served");
  //Serial.println();
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

  struct BMP180_Struct bmp180Result = getPressTemp(false); //getSampleOfPressTemp(1);
  double temp1 = bmp180Result.temperature;

  struct DHT_Struct dhtResult = getSampleOfTempHum(1);
  double temp2 = dhtResult.temperature;

  double temperature = (temp1 + temp2) / 2;
  
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

  double temperature = (temp1 + temp2) / 2;
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

//  double avgTemp = NULL;
//  if(avgBmpTemp != NULL && avgDhtTemp != NULL){
//    avgTemp = (avgBmpTemp + avgDhtTemp) / 2;
//  }else if(avgBmpTemp != NULL){
//    avgTemp = avgBmpTemp;
//  }else if(avgDhtTemp != NULL){
//    avgTemp = avgDhtTemp;
//  }

  double avgTemp = getAvgTemp();
  
  String contentJson = 
    String("{") +
      "\"temperature\": \"" + String(avgTemp) + "\"," + 
      "\"humidity\": \"" + String(avgDhtHum) + "\"," + 
      "\"pressure\": \"" + String(avgBmpPress) + "\"," + 
      "\"distance\": \"" + String(avgHcsrDist) + "\"," + 
    "}";
  
  server.send(200, "application/json", contentJson);
  
  Serial.println("Served");
}

bool configureHttpServer(){
  bool ret = true;
  
  server.on("/configure", HTTP_GET, handleGetConfigure);
  server.on("/pressure", HTTP_GET, handleGetPressure);
  server.on("/temperature", HTTP_GET, handleGetTemperature);
  server.on("/humidity", HTTP_GET, handleGetHumidity);
  server.on("/distance", HTTP_GET, handleGetDistance);

  server.on("/all/actual", HTTP_GET, handleGetAllActual);
  server.on("/all/aggregated", HTTP_GET, handleGetAllAggregated);
  
//  server.on("/configure", HTTP_POST, handlePostConfigure);

  server.onNotFound(handleNotFound);
  
  server.begin();                  //Start server

  Serial.println("HTTP server started");
  
  return ret;
}
