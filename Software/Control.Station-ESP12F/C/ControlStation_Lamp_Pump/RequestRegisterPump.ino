bool registerPump() {
  connectToWiFiIfNotConnected();

  Serial.println("Register pump ...");

  String url = "http://" + webserver_ip + "/" + webserver_path_pump_register + "/dateString/" + getOffsetDateString() + "/pumpId/" + pump_id;
  http.begin(wifiClient, url);
  int responseCode = http.POST("");

  Serial.println(String("  URL: ") + url);

  bool result = true;
  if (responseCode > 0) {

    String payload = http.getString();   //Get the request response payload

    Serial.print("  Response Code: ");
    Serial.println(responseCode);
    Serial.print("  Payload: ");
    Serial.println(payload);             //Print the response payload

  } else {
    Serial.println("!!! No GET response !!!");
    result = false;
  }

  //Serial.println("\n\n\n");
  http.end();   //Close connection

  return result;
}
