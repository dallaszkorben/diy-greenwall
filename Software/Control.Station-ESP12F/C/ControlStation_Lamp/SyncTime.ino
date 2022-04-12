void syncTime(){
  connectToWiFiIfNotConnected();

  Serial.println("Try to sync Time ...");

  HTTPClient http;
  String url = "http://" + webserver_ip + "/" + webserver_path_info_timestamp + String("/epocDate/1970.01.01");
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
  sprintf(date, "%4d-%02d-%02dT%02d:%02d:%02d+01:00", year(), month(), day(), hour(), minute(), second());
  return String(date);
}
