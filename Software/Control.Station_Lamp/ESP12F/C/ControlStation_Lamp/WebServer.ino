long lengthInSec;

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

String args;
String message;
String uri;
String method;

void fetchParameters(String operation){
  args = String(" args: ");
  message = "{\"success\": True, \"data\": \"" + operation + "\"}";
  uri = server.uri();
  method = (server.method() == HTTP_GET) ? String("GET") : String("POST");

  lengthInSec = 0;
  for (uint8_t i = 0; i < server.args(); i++) {
    if (server.argName(i).equals(String("lengthInSec"))) {
      lengthInSec = server.arg(i).toInt();
      args += server.argName(i) + ": " + server.arg(i) + " ";
    }
  }  
}

//---

void handleIsAlive() {
  String message = "{\"success\": True, \"data\": \"\"}";
  String uri = server.uri();
  String method = (server.method() == HTTP_GET) ? String("GET") : String("POST");
  String args = String(" args: ");

  server.send(200, "application/json", message);

  Serial.print(" Received IsAlive Request: URI: ");
  Serial.print(uri);
  Serial.print("; Method: ");
  Serial.print(method);
  Serial.println();

}

void handleLampOn() {
  fetchParameters("ON");
  server.send(200, "application/json", message);
  turnLampOn(lengthInSec);
  
  Serial.print("Request to Lamp ON: URI: ");
  Serial.print(uri);
  Serial.print("; Method: ");
  Serial.print(method);
  Serial.print("; Parameters: ");
  Serial.print(args);
  Serial.println();  
}

void handleLampOff() {
  fetchParameters("OFF");
  server.send(200, "application/json", message);
  turnLampOff(lengthInSec);
  
  Serial.print("Request to Lamp OFF: URI: ");
  Serial.print(uri);
  Serial.print("; Method: ");
  Serial.print(method);
  Serial.print("; Parameters: ");
  Serial.print(args);
  Serial.println();  
}

void handleLampStatus(){
  String st;
  if(lampActive){
    st = "on";
  }else{
    st = "off";
  }

  DynamicJsonDocument doc(512);
  doc["success"] =  true;
  doc["status"] = st;
  String buf;
  serializeJson(doc, buf);
  server.send(200, "application/json", buf);
  
}
