#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

WiFiClient client;
HTTPClient http;
  
bool reportSensors(bool needToPrint){
  bool res = true;

  String levelValue = (avgHcsrDist != NULL) ? String(avgHcsrDist) : "";
  String pressureValue = (avgBmpPress != NULL) ? String(avgBmpPress) : "";
  String humidityValue = (avgDhtHum != NULL) ? String(avgDhtHum) : "";
  double avgTemp = getAvgTemp();
  String temperatureValue = (avgTemp != NULL) ? String(avgTemp) : "";

  String url = "http://" + clientIp + ":" + clientPort + "/" + clientPathToReport + "/stationId/" + stationId + "/levelValue/" + levelValue + "/temperatureValue/" + temperatureValue + "/humidityValue/" + humidityValue + "/pressureValue/" + pressureValue;

  //String url = "http://" + clientIp + ":" + clientPort + "/" + clientPathToReport;
  String json = String("{") + 
    "\"stationId\": \"" + stationId + "\"," + 
    "\"levelValue\": \"" + levelValue + "\"," +
    "\"temperatureValue\": \"" + temperatureValue + "\"," +
    "\"humidityValue\": \"" + humidityValue + "\"," +
    "\"pressureValue\": \"" + pressureValue + "\"" +
  "}";

  //Connect if it was not connected
  connectToAccessPoint(needToPrint);
  
  http.begin(client, url);
  http.addHeader("Content-Type", "application/json");
  //int responseCode = http.POST(json);
  int responseCode = http.POST("");

  if (responseCode == 200) {

    //As the report was successfull, we do not need the moving average value anymore
    //So it takes the avg values as the next first measurement
    
    //avgDhtTemp = NULL;
    //avgDhtHum = NULL;
    avgDhtCounter = 1;
    
    //avgBmpTemp = NULL;
    //avgBmpPress = NULL;
    avgBmpCounter = 1;
    
    //avgHcsrDist = NULL;
    avgHcsrCounter = 1;
    
  }else{
    res = false;
  }

  http.end();
  
  return res;
}
