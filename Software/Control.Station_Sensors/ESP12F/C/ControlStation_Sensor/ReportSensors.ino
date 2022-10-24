#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

WiFiClient client;
HTTPClient http;
  
bool reportSensors(bool needToPrint){
  bool res = true;

  // Collects the values only if they were measured 
  String levelValue = (avgHcsrDist != NULL) ? String(avgHcsrDist) : "";
  String pressureValue = (avgBmpPress != NULL) ? String(avgBmpPress) : "";
  String humidityValue = (avgDhtHum != NULL) ? String(avgDhtHum) : "";
  double avgTemp = getAvgTemp(avgBmpTemp, avgDhtTemp);
  String temperatureValue = (avgTemp != NULL) ? String(avgTemp) : "";

  // !!! You can not send the parameters in the URL !!!
  //     Because if there is NO value for a sensore (no sensore connected), then the value is EMPTY
  //     so the URL will look like for example  /stationId/3/levelValue//temperatureValue/32.2
  //String url = "http://" + clientIp + ":" + clientPort + "/" + clientPathToReport + "/stationId/" + stationId + "/levelValue/" + levelValue + "/temperatureValue/" + temperatureValue + "/humidityValue/" + humidityValue + "/pressureValue/" + pressureValue;

  String url = "http://" + clientIp + ":" + clientPort + "/" + clientPathToReport;
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
  int responseCode = http.POST(json);
  //As I explained before, you have to send data in json instead of in the url
  //int responseCode = http.POST("");

  if (responseCode == 200) {

    //As the report was successfull, we do not need the moving average value anymore
    //So the average values must be cleared and the first measurement should be taken

    // Clears the moving average of Temperature/Humidity and takes one now measurement
    struct DHT_Struct dhtResult = add1SampleToMovingAverageTempHum(true);

    // Clears the moving average of Pressure/Temperature and takes one now measurement
    struct BMP180_Struct bmp180Result = add1SampleToMovingAveragePressTemp(true);

    // Clears the moving average of distance and takes one now measurement
    avgHcsrDist = add1SampleToMovingAverageDistance(true);
    
  }else{
    res = false;
  }

  http.end();
  
  return res;
}
