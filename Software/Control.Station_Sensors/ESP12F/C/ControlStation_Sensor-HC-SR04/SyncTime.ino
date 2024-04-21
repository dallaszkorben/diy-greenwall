#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
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

  String url = "http://" + clientIp + ":" + clientPort + "/" + clientPathToInfoTimestamp + String("/epocDate/1970-01-01T00:00:00+00:00");

  Serial.println("============= Sync Time ============");
  
  http.begin(client, url);
  http.setTimeout(20000);

  Serial.println(String("    GET: ") + url);
  int responseCode = http.GET();

  Serial.print("    Response Code: ");
  Serial.println(responseCode);

  bool result = false;
  
  if (responseCode == HTTP_CODE_OK) {

    String payload = http.getString();   //Get the request response payload

    Serial.print("    Payload: ");
    Serial.println(payload);             //Print the response payload

    // Handle JSON
    const size_t capacity = JSON_OBJECT_SIZE(3) + JSON_ARRAY_SIZE(2) + 60;

    DynamicJsonDocument doc(capacity);
    DeserializationError error = deserializeJson(doc, payload);
    if (error) {
      Serial.println(F("    !!! Parsing failed!"));
    } else {
      long timeStamp = doc["timeStamp"];
      timeOffsetInt = doc["offsetInt"];
      String offsetString = doc["offsetString"];
      timeOffsetString = offsetString;
      setTime(timeStamp);
      adjustTime(timeOffsetInt);
      
      Serial.print("Time: ");
      Serial.print(timeStamp);
      Serial.print(" - ");
      Serial.println(getOffsetDateString());
      result = true;
    }
    Serial.print("    Time: ");
    Serial.println(getOffsetDateString());

  } else {
    Serial.print("   !!! Error on HTTP GET request. Error code: ");
    Serial.println(responseCode);
  }
  http.end();
  return result;
}

String getOffsetDateString(){
  char date[26]; //19 + 6 digits plus the null char
  sprintf(date, "%4d-%02d-%02dT%02d:%02d:%02d%s", year(), month(), day(), hour(), minute(), second(), timeOffsetString);
  return String(date);
}
