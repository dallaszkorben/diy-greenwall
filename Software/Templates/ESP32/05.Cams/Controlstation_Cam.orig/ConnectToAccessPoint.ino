bool connectToApIfNotConnected() {

  bool ret = false;
//  if (WiFi.status() != WL_CONNECTED) {

    // Tries to connect to the AP 10 times. If it was not successfull, restarts the module
    Serial.printf("Try to connect to Access Point %s ", ssid);
    
    int loop = 0;
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
      ret = true;
    }
//  }else{
//    ret = true;
//  }

  return ret;
}
