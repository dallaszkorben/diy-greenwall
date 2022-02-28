
bool connectToWiFi() {
  WiFi.begin(essid, password);

  Serial.println();
  Serial.print("Connecting to WiFi ");
  while (WiFi.status() != WL_CONNECTED){
    delay(1000);
    Serial.print(".");
  }

  Serial.println("success!");
  Serial.print("Local IP Address is: ");
  Serial.println(WiFi.localIP());

  return true;
}

void connectToWiFiIfNotConnected(){
  Serial.print("Connection ");
  while ( !WiFi.localIP().isSet() || !WiFi.isConnected() ){

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

/*  
  if( !WiFi.localIP().isSet() || !WiFi.isConnected() ){
    Serial.println("Reconnecting to WiFi...");
    //WiFi.disconnect();
    WiFi.reconnect();
  }else{
    Serial.print("Connection is OK. LocalIP: ");
    Serial.println(WiFi.localIP());   
  }
*/  
/*  
  // if WiFi is down, try reconnecting every CHECK_WIFI_TIME seconds
  if (WiFi.status() != WL_CONNECTED && WiFi.status() != 7) {// && (currentMillis - previousMillis >=interval)) {
    //Serial.print(millis());
    Serial.println("Reconnecting to WiFi...");
    //WiFi.disconnect();
    WiFi.reconnect();
    //previousMillis = currentMillis;
  }else{
    Serial.print("Connection is OK. LocalIP: ");
    Serial.println(WiFi.localIP());
  }
*/  
}
