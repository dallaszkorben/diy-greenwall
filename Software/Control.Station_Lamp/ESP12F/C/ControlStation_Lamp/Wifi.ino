
void connectToWiFi() {
  ledSignalCommunicate();

  WiFi.begin(essid, password);

  WiFi.setAutoReconnect(true);
  WiFi.persistent(true);

  Serial.println();
  Serial.print("Connecting to WiFi First time");
  int maxWaitingTime = now() + 30; //Max 30 seconds to wait for the connection
  while (WiFi.status() != WL_CONNECTED && now() <= maxWaitingTime){
    Serial.print(".");
    WiFi.reconnect();
    delay(5000);
  }
  if(WiFi.status() != WL_CONNECTED){
    Serial.println("Failure!");
    Serial.print("Could not connect to the WiFi\n\n");

    Serial.println("===================================");
    Serial.println("===       !!!  RESET  !!!       ===");
    Serial.println("===  Failed to connect to WiFi  ===");
    Serial.println("===================================");
    ESP.restart();    
  
  }else{
    Serial.println("success!");
    Serial.print("Local IP Address is: ");
    Serial.println(WiFi.localIP());

    ledSignalHealthy();
    return;
  }
}

void connectToWiFiIfNotConnected(){
  ledSignalCommunicate();

  Serial.print("\nReconnecting to WiFi ");
  int maxWaitingTime = now() + 30; //Max 30 seconds to wait for the connection
  while ( (!WiFi.localIP().isSet() || !WiFi.isConnected() ) && now() <= maxWaitingTime){
    Serial.print(".");
    WiFi.reconnect();
    delay(5000);
  }

  if( !WiFi.localIP().isSet() || !WiFi.isConnected() ){
    Serial.println("Failure!");
    Serial.print("Could not connect to the WiFi");
    
    Serial.println("======================================");
    Serial.println("===        !!!  RESET  !!!         ===");
    Serial.println("===  Failed to re-connect to WiFi  ===");
    Serial.println("======================================");
    ESP.restart();
    
  }else{
    Serial.print(" OK. Local IP: ");
    Serial.println(WiFi.localIP());
    Serial.println("");

    ledSignalHealthy();
  
    return;
  }
}
