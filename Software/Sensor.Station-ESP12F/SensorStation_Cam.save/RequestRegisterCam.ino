void registerCam() {
  HTTPClient http;
  WiFiClient wifiClient;
  
  connectToWiFiIfNotConnected();

  Serial.println("Register CAM ...");

  //HTTPClient http;
  String url = "http://" + String(webserver_ip) + "/" + String(webserver_path_cam_register) + "/dateString/" + getOffsetDateString() + "/camId/" + String(cam_id);
  http.begin(wifiClient, url);
  int responseCode = http.POST("");

  Serial.println(String("  URL: ") + url);

  if (responseCode > 0) {

    String payload = http.getString();   //Get the request response payload

    Serial.print("  Response Code: ");
    Serial.println(responseCode);
    Serial.print("  Payload: ");
    Serial.println(payload);             //Print the response payload

  } else {
    Serial.println("!!! No GET response !!!");
  }

  Serial.println("\n\n\n");
  http.end();   //Close connection
}
