bool connectToApIfNotConnected() {
  bool ret = false;

  // Tries to connect to the AP 10 times. If it was not successfull, restarts the module
  Serial.printf("Try to connect to Access Point %s ", ssid);
    
  int loop = 0;
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED && loop <= 10) {
    delay(1000);
    Serial.print(".");
    loop++;
  }

  Serial.println("");
  if(WiFi.status() == WL_CONNECTED){
    Serial.println("    WiFi connected");
    Serial.print("    IP: ");
    Serial.println(WiFi.localIP());

    Serial.print("    RSSI: ");
    Serial.println(WiFi.RSSI());
    
    ret = true;
  }

  return ret;
}
