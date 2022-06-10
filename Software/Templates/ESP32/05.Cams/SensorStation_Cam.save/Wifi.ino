
bool connectToWiFi() {
  
  Serial.println();
  Serial.print("Connecting to WiFi: ");
  Serial.println(String(essid));

  WiFi.begin(essid.c_str(), password.c_str());

  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }

  Serial.println("success!");
  Serial.print("Local IP Address is: ");
  Serial.println(WiFi.localIP());

  return true;
}

void connectToWiFiIfNotConnected(){
  Serial.print("Connection ");
//  while ( !WiFi.localIP().isSet() || !WiFi.isConnected() ){
  while ( !WiFi.isConnected() ){

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
}
