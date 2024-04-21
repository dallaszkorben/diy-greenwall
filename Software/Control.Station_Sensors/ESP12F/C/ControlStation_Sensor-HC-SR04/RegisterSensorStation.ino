#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

bool registerSensorStation(bool needToPrint){
  String url = "http://" + clientIp + ":" + clientPort + "/" + clientPathToRegister;
  
  //Connect if it was not connected
  connectToAccessPoint(needToPrint);

  http.begin(client, url);
  http.setTimeout(20000);
  http.addHeader("Content-Type", "application/json");    

  // Construct the payload
  StaticJsonDocument<1024> doc;
  doc["stationId"] = stationId;
  doc["configureUrl"] = "http://" + WiFi.localIP().toString() + ":80/configure";
  doc["measureActualUrl"] = "http://" + WiFi.localIP().toString() + ":80/all/actual";
  doc["collectAverageUrl"] = "http://" + WiFi.localIP().toString() + ":80/all/aggregated";
  doc["triggerReportUrl"] = "http://" + WiFi.localIP().toString() + ":80/trigger/report";  
  doc["dateString"] = getOffsetDateString();
  String requestBody;
  serializeJson(doc, requestBody);

  int responseCode = http.POST(requestBody);

  if(needToPrint){    
    Serial.println(String("   POST: ") + url);
    Serial.print(String("         "));
    Serial.println(requestBody);
    Serial.print("   Response Code: ");
    Serial.println(responseCode);
  }

  bool result = true;
  if (responseCode == HTTP_CODE_OK) {

    String payload = http.getString();   //Get the request response payload

    if(needToPrint){
      Serial.print("   Payload: ");
      Serial.println(payload);             //Print the response payload
      Serial.println("Sensor Station was registered"); 
    }

  } else {
    Serial.print("   !!! Error on HTTP POST request. Error code: ");
    Serial.println(responseCode);
    result = false;
  }

  //Serial.println("\n\n\n");
  http.end();   //Close connection

  return result;
}
