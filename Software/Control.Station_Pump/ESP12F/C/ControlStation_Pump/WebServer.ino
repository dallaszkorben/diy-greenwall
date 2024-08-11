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



void handlePumpOn() {
  fetchParameters("ON");
  server.send(200, "application/json", message);
  turnPumpOn(lengthInSec);

  Serial.print("Request to Pump ON: URI: ");
  Serial.print(uri);
  Serial.print("; Method: ");
  Serial.print(method);
  Serial.print("; Parameters: ");
  Serial.print(args);
  Serial.println();
}

void handlePumpOff() {
  fetchParameters("OFF");
  server.send(200, "application/json", message);
  turnPumpOff();

  Serial.print("Request to Pump ON: URI: ");
  Serial.print(uri);
  Serial.print("; Method: ");
  Serial.print(method);
  Serial.print("; Parameters: ");
  Serial.print(args);
  Serial.println();  
}


void handlePumpStatus(){
  String st;
  int count_down = 0;
  float percentage = 0;
  long now_timestamp = now();

  if(pump_active){
    st = "on";
    count_down = pump_off_timestamp - now_timestamp;
    percentage = float(now_timestamp - pump_start_timestamp)/float(pump_off_timestamp - pump_start_timestamp);
  }else{
    st = "off";
  }



  DynamicJsonDocument doc(512);
  doc["success"] =  true;
  doc["status"] = st;
  doc["count-down"] = count_down;
  doc["percentage"] = percentage;
  String buf;
  serializeJson(doc, buf);
  server.send(200, "application/json", buf);
}
