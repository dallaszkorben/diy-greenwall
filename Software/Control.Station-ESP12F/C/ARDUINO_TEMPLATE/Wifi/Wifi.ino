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
  Serial.print("Connection ");
  while (WiFi.status() != WL_CONNECTED || WiFi.localIP() == IPAddress(0,0,0,0)) {
  //while ( !WiFi.localIP().isSet() || !WiFi.isConnected() ){

    //Serial.print(WiFi.localIP());
    //Serial.print(" - ");
    //Serial.println(WiFi.isConnected());
    
    Serial.print(".");
    WiFi.reconnect();
    delay(4000);
  }
  Serial.print(" OK. Local IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("");
  return;
}


/*
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
    Serial.print("Connection is OK - My IP: ");
    Serial.println(WiFi.localIP());
  }
}
*/

void loop() {

  delay(10000);
  connectIfNotConnected();
  //Serial.println(WiFi.status());
    
}
