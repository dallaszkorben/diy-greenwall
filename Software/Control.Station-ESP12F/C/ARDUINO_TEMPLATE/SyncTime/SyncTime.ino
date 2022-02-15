
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

#include <TimeLib.h>

const char* ssid = "Central-Station-006";
const char* password = "viragfal";

WiFiClient wifiClient;

void setup() {
  delay(1000);
  Serial.begin(115200);
  delay(1000);
 
  WiFi.begin(ssid, password);

  Serial.print("\n\nConnecting");
  while (WiFi.status() != WL_CONNECTED){
    delay(1000);
    Serial.print(".");
  }

  Serial.println("success!");
  Serial.print("  IP Address is: ");
  Serial.println(WiFi.localIP());

  syncTime();

}

void connectIfNotConnected(){
  Serial.print("Check if it is connected... ");
  // if WiFi is down, try reconnecting every CHECK_WIFI_TIME seconds
  if (WiFi.status() != WL_CONNECTED && WiFi.status() != 7) {// && (currentMillis - previousMillis >=interval)) {
    Serial.println("Reconnecting to WiFi...");
    WiFi.reconnect();
    
  }else{
    Serial.println("Connection is OK");
  }
}

void syncTime(){
  connectIfNotConnected();

  Serial.println("Try to sync Time ...");

  HTTPClient http;
  String url = String("http://192.168.50.3:5000/info/timeStamp/epocDate/1970.01.01");
  http.begin(wifiClient, url);    
  int responseCode = http.GET();                                

  Serial.println(String("  URL: ") + url);
  
  if (responseCode > 0) {
 
    String payload = http.getString();   //Get the request response payload

    Serial.print("  Response Code: ");
    Serial.println(responseCode);
    Serial.print("  Payload: ");
    Serial.println(payload);             //Print the response payload

    // Handle JSON
    const size_t capacity = JSON_OBJECT_SIZE(3) + JSON_ARRAY_SIZE(2) + 60;
    DynamicJsonBuffer jsonBuffer(capacity);
    JsonObject& root = jsonBuffer.parseObject(payload);
    if (root.success()) {
      long timeStamp = root["timeStamp"];
      setTime(timeStamp);
    }else{
      Serial.println(F("  Parsing failed!"));
    } 
  }else{
    Serial.println("!!! No GET response !!!");
  }
  Serial.println("\n\n\n");
  http.end();   //Close connection
}

String getOffsetDateString(){
  char date[26]; //19 + 6 digits plus the null char
  sprintf(date, "%4d-%02d-%02dT%d:%02d:%02d+01:00", year(), month(), day(), hour(), minute(), second());
  return String(date);
}

void loop() {

  Serial.println(getOffsetDateString());

  delay(30000);
  
}
