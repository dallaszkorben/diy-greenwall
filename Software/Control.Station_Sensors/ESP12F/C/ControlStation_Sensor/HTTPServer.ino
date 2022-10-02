
void handleNotFound(){
  
  server.send(404, "text/plain", "404: Not found");

  Serial.println("!!! HTTP request was not found !!!");
  Serial.println();
}

void handleGetConfigure(){
  Serial.println("'GET /configure' request");

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
  
  Serial.println("   Request 'GET /configure' was served");
  Serial.println();
}

void handleGetPressure(){
  Serial.println("'GET /pressure' request");

  struct BMP180_Struct bmp180Result = getAveragePressure(1);
  double pressure = bmp180Result.pressure;
  
  String contentJson = 
    String("{") +
      "\"pressure\": \"" + String(pressure) + "\"" + 
    "}";
  
  server.send(200, "application/json", contentJson);
  
  Serial.println("   Request 'GET /pressure' was served");
  Serial.println();
}

void handleGetTemperature(){
  Serial.println("'GET /tepmerature' request");

  struct BMP180_Struct bmp180Result = getAveragePressure(1);
  double temp1 = bmp180Result.temperature;

  struct DHT_Struct dhtResult = getAverageTempHum(1);
  double temp2 = dhtResult.temperature;

  double temperature = (temp1 + temp2) / 2;
  
  String contentJson = 
    String("{") +
      "\"temperature\": \"" + String(temperature) + "\"" + 
    "}";
  
  server.send(200, "application/json", contentJson);
  
  Serial.println("   Request 'GET /temperature' was served");
  Serial.println();
}

void handleGetHumidity(){
  Serial.println("'GET /humidity' request");

  struct DHT_Struct dhtResult = getAverageTempHum(1);

  String contentJson = 
    String("{") +
      "\"humidity\": \"" + String(dhtResult.humidity) + "\"" + 
    "}";
  
  server.send(200, "application/json", contentJson);
  
  Serial.println("   Request 'GET /humidity' was served");
  Serial.println();
}

void handleGetDistance(){
  Serial.println("'GET /distance' request");

  double distance = getAverageDistance(1);

  String contentJson = 
    String("{") +
      "\"distance\": \"" + String(distance) + "\"" + 
    "}";
  
  server.send(200, "application/json", contentJson);
  
  Serial.println("   Request 'GET /distance' was served");
  Serial.println();
}

bool configureHttpServer(){
  bool ret = true;
  
  server.on("/configure", HTTP_GET, handleGetConfigure);
  server.on("/pressure", HTTP_GET, handleGetPressure);
  server.on("/temperature", HTTP_GET, handleGetTemperature);
  server.on("/humidity", HTTP_GET, handleGetHumidity);
  server.on("/distance", HTTP_GET, handleGetDistance);  

  server.onNotFound(handleNotFound);
  
  server.begin();                  //Start server

  Serial.println("HTTP server started");
  
  return ret;
}
