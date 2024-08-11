bool syncTime(){
  connectToWiFiIfNotConnected();

  Serial.println("Try to sync Time ...");

  HTTPClient http;
  String url = "http://" + webserver_ip + "/" + webserver_path_info_timestamp + String("/epocDate/1970-01-01T00:00:00+00:00");
  http.begin(wifiClient, url);    
  int responseCode = http.GET();                                

  Serial.println(String("  URL: ") + url);

  bool result = false;

  if (responseCode > 0) {
 
    String payload = http.getString();   //Get the request response payload

    Serial.print("  Response Code: ");
    Serial.println(responseCode);
    Serial.print("  Payload: ");
    Serial.println(payload);             //Print the response payload

    // Handle JSON
    const size_t capacity = JSON_OBJECT_SIZE(3) + JSON_ARRAY_SIZE(2) + 60;
    DynamicJsonDocument jsonBuffer(capacity);
    DeserializationError error = deserializeJson(jsonBuffer, payload);

    if( error ){
      Serial.println(F("  Parsing failed!"));
    }else{
      long timeStamp = jsonBuffer["timeStamp"];
      timeOffsetInt = jsonBuffer["offsetInt"];
      String offsetString = jsonBuffer["offsetString"];
      timeOffsetString = offsetString;
      setTime(timeStamp);
      adjustTime(timeOffsetInt);
      
      Serial.print("Time: ");
      Serial.print(timeStamp);
      Serial.print(" - ");
      Serial.println(getOffsetDateString());
      result = true;
    } 
  }else{
    Serial.println("!!! No GET response !!!");
  }  
  http.end();   //Close connection
  return result;
}

String getOffsetDateString(){
  char date[26]; //19 + 6 digits plus the null char
  sprintf(date, "%4d-%02d-%02dT%02d:%02d:%02d%s", year(), month(), day(), hour(), minute(), second(), timeOffsetString);
  return String(date);
}
