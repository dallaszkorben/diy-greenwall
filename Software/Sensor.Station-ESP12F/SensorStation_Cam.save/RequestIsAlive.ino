bool isAlive(){
  HTTPClient http;
  WiFiClient wifiClient;

  bool ret = false;
  
  connectToWiFiIfNotConnected();

  Serial.println("Request 'isAlive()'");

  //HTTPClient http;
  String url = "http://" + String(webserver_ip) + "/" + String(webserver_path_info_is_alive);
  //http.setReuse(true);
  http.begin(wifiClient, url);    
  int responseCode = http.GET();                                

  Serial.println(String("  URL: ") + url);
  Serial.print("  Wifi status: ");
  Serial.println(WiFi.status());
  
  if (responseCode > 0) {
 
    String payload = http.getString();

    Serial.print("  Response Code: ");
    Serial.println(responseCode);
    Serial.print("  Payload: ");
    Serial.println(payload);             //Print the response payload

    ret = true;
  }else{
    Serial.printf("   [HTTP] GET... failed, error: %s\n", http.errorToString(responseCode).c_str());
  }
  http.end();         //Close connection
  Serial.println();

  return true;
}
