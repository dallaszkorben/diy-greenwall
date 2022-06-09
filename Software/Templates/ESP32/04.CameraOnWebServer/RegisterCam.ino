#include <ArduinoJson.h>

bool registerCam() {

  String url = "http://" + clientIp + ":" + clientPort + "/" + clientPathToCamRegister;

  Serial.println("Register Camera ...");

  http.begin(wifiClient, url);
  http.setTimeout(20000);
  http.addHeader("Content-Type", "application/json");    

  // Construct the payload
  StaticJsonDocument<1024> doc;
  doc["camId"] = camId;
  doc["streamUrl"] = "http://" + WiFi.localIP().toString() + ":81/stream";
  doc["captureUrl"] = "http://" + WiFi.localIP().toString() + ":80/capture";
  doc["dateString"] = getOffsetDateString();
  String requestBody;
  serializeJson(doc, requestBody);

  Serial.println(String("    POST: ") + url);
  int responseCode = http.POST(requestBody);
  Serial.print("    Response Code: ");
  Serial.println(responseCode);

  bool result = true;
  if (responseCode == HTTP_CODE_OK) {

    String payload = http.getString();   //Get the request response payload

    //Serial.print("    Response Code: ");
    //Serial.println(responseCode);
    Serial.print("    Payload: ");
    Serial.println(payload);             //Print the response payload

  } else {
    Serial.println("    !!! No GET response !!!");
    result = false;
  }

  //Serial.println("\n\n\n");
  http.end();   //Close connection

  return result;

  return true;
}
