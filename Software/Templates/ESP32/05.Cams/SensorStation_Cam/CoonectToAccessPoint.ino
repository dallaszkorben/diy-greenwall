void connectToAP(){
  if (WiFi.status() != WL_CONNECTED){
    // Tries to connect to the AP 10 times. If it was not successfull, restarts the module
    int loop = 0;
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED && loop <= 10) {
        delay(1000);
        Serial.print(".");
        loop++;
    }
    Serial.println();
    if(loop > 10){
      Serial.println("   !!! Connection failed -> reboot");
      ESP.restart();
    }
  }
}
