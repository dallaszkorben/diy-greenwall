#include <ESP8266WiFi.h>

const char* ssid = "Central-Station-006";
const char* password = "viragfal";

//unsigned long previousMillis = 0;
//unsigned long interval = 30000;

void setup() {
  delay(1000);
  Serial.begin(115200);
  delay(1000);
 
  WiFi.begin(ssid, password);

  Serial.println();
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }

  Serial.println("success!");
  Serial.print("IP Address is: ");
  Serial.println(WiFi.localIP());
}

void connectIfNotConnected(){
  //unsigned long currentMillis = millis();
  
  // if WiFi is down, try reconnecting every CHECK_WIFI_TIME seconds
  if (WiFi.status() != WL_CONNECTED && WiFi.status() != 7) {// && (currentMillis - previousMillis >=interval)) {
    //Serial.print(millis());
    Serial.println("Reconnecting to WiFi...");
    //WiFi.disconnect();
    WiFi.reconnect();
    //previousMillis = currentMillis;
  }else{
    Serial.println("Connection is OK");
  }
}


void loop() {

  delay(30000);
  connectIfNotConnected();
  //Serial.println(WiFi.status());
  //delay(1000);
  
  
}
