#include <HTTPClient.h>
#include <base64.h>
#include <ArduinoJson.h>
#include <TimeLib.h>

//HTTPC_ERROR_CONNECTION_REFUSED (-1)
//HTTPC_ERROR_SEND_HEADER_FAILED (-2)
//HTTPC_ERROR_SEND_PAYLOAD_FAILED (-3)
//HTTPC_ERROR_NOT_CONNECTED (-4)
//HTTPC_ERROR_CONNECTION_LOST (-5)
//HTTPC_ERROR_NO_STREAM (-6)
//HTTPC_ERROR_NO_HTTP_SERVER (-7)
//HTTPC_ERROR_TOO_LESS_RAM (-8)
//HTTPC_ERROR_ENCODING (-9)
//HTTPC_ERROR_STREAM_WRITE (-10)
//HTTPC_ERROR_READ_TIMEOUT (-11)
//To get the meaning of code use: htt.errorToString(responseCode)


bool syncTime() {
//  HTTPClient http;
//  WiFiClient wifiClient;

  String url = "http://" + serverIp + ":" + serverPort + "/" + serverPathToInfoTimestamp + String("/epocDate/1970.01.01 ");

  Serial.println("Try to sync Time ");
  
  http.begin(wifiClient, url);
  http.setTimeout(20000);

  Serial.println(String("    GET: ") + url);
  int responseCode = http.GET();

  Serial.print("    Response Code: ");
  Serial.println(responseCode);
  
  if (responseCode == HTTP_CODE_OK) {

    String payload = http.getString();   //Get the request response payload

    //Serial.print("    Response Code: ");
    //Serial.println(responseCode);
    Serial.print("    Payload: ");
    Serial.println(payload);             //Print the response payload

    // Handle JSON
    const size_t capacity = JSON_OBJECT_SIZE(3) + JSON_ARRAY_SIZE(2) + 60;

    DynamicJsonDocument doc(capacity);
    DeserializationError error = deserializeJson(doc, payload);
    if (error) {
      Serial.println(F("    !!! Parsing failed!"));
      http.end();
      return false;
    } else {
      long timeStamp = doc["timeStamp"];
      setTime(timeStamp);
    }
    Serial.print("    Time: ");
    Serial.println(getOffsetDateString());

  } else {
    Serial.println("    !!! Error on HTTP request. !!!");
    //Serial.print(".");
    //delay(1000);
    //return false;
  }
  http.end();

  if (responseCode == HTTP_CODE_OK) {
    return true;
  } else {
    return false;
  }
}

String getOffsetDateString() {
  char date[26]; //19 + 6 digits plus the null char
  sprintf(date, "%4d-%02d-%02dT%02d:%02d:%02d+01:00", year(), month(), day(), hour(), minute(), second());
  return String(date);
}
