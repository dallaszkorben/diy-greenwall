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

void handleLamp() {
  String message = "{\"success\": True, \"data\": \"\"}";
  String uri = server.uri();
  String method = (server.method() == HTTP_GET) ? String("GET") : String("POST");
  String args = String(" args: ");

  lengthInSec = 0;
  for (uint8_t i = 0; i < server.args(); i++) {
    if (server.argName(i).equals(String("lengthInSec"))) {
      lengthInSec = server.arg(i).toInt();
      args += server.argName(i) + ": " + server.arg(i) + " ";
    }
  }

  server.send(200, "application/json", message);

  Serial.print("Request to LampOn: URI: ");
  Serial.print(uri);
  Serial.print("; Method: ");
  Serial.print(method);
  Serial.print("; Parameters: ");
  Serial.print(args);
  Serial.println();
}

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
  handleLamp();
  turnLampOn(lengthInSec);
}

void handleLampOff() {
  handleLamp();
  turnLampOff(lengthInSec);
}
