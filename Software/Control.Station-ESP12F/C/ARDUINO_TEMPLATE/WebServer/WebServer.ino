#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "Central-Station-006";
const char* password = "viragfal";

ESP8266WebServer server(80);

void handleNotFound() {
  String message = "{\"success\": False, \"data\": \"\"}";
  String uri = server.uri();  
  String method = (server.method() == HTTP_GET) ? String("GET") : String("POST");
  String args = String(" args: ");
  for (uint8_t i = 0; i < server.args(); i++) {
     args += server.argName(i) + ": " + server.arg(i) + ", ";
  }
  
  Serial.print("Bad request: URI: ");
  Serial.print(uri);
  Serial.print("; Method: ");
  Serial.print(method);
  Serial.print("; Parameters: ");
  Serial.print(args);
  Serial.println();
  
  server.send(404, "application/json", message);
}

void handleLampOn() {
  String message = "{\"success\": True, \"data\": \"\"}";
  String uri = server.uri();  
  String method = (server.method() == HTTP_GET) ? String("GET") : String("POST");
  String args = String(" args: ");
  for (uint8_t i = 0; i < server.args(); i++) {
    
    //if(strcmp(server.argName(i), "lengthInSec") == 0){
    if(server.argName(i).equals(String("lengthInSec"))){
      args += server.argName(i) + ": " + server.arg(i) + " ";
    }
  }
  
  Serial.print("Request to LampOn: URI: ");
  Serial.print(uri);
  Serial.print("; Method: ");
  Serial.print(method);
  Serial.print("; Parameters: ");
  Serial.print(args);
  Serial.println();

  server.send(200, "application/json", message);
}

void handleIsAlive() {
  server.send(200, "text/plain", "Alive\r\n");
}

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
  Serial.print("IP Address is: ");
  Serial.println(WiFi.localIP());

  //
  // WEB server
  //

  server.on("/isAlive", handleIsAlive);
  server.on("/lamp/on", HTTP_POST, handleLampOn);
  
  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");

}

void connectIfNotConnected(){

  Serial.print("Check if it is connected... ");
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

  //delay(30000);
  //connectIfNotConnected();
  //Serial.println(WiFi.status());
  //delay(1000);

  server.handleClient();
  
}
