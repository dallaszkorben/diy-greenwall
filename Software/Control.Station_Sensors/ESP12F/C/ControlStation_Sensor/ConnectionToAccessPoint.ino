bool connectToAccessPoint(bool needToPrint){
  bool ret = true;
  int loop = 0;
  while ((WiFi.status() != WL_CONNECTED || !WiFi.localIP().isSet()) && loop <= MAX_RECONNECTION_LOOP) {
    if(loop == 0){
      if(needToPrint){
        Serial.print("   Restore the connection ");
      }
      //WiFi.reconnect();
    }
    loop++;
    Serial.print(".");
    delay(500);    
  }
  
  if(loop > 0 && needToPrint){
    Serial.println();
    Serial.println();
  }  
  if(loop >= MAX_RECONNECTION_LOOP){
    if(needToPrint){
      Serial.println();
      Serial.println();
      Serial.println("!!! It was not possible to restore connection !!!");
      Serial.println();
      Serial.println();
    }
    ret = false;
  }
  return ret;
}

void wifiEvent(WiFiEvent_t event) {
/*    Serial.println();
    Serial.println("=== Event ===");
    
    switch(event) {
      case WIFI_EVENT_STAMODE_CONNECTED:
            Serial.println("WiFi got connected");
            break;
        case WIFI_EVENT_STAMODE_GOT_IP:
            Serial.println("WiFi got IP");
            Serial.print("IP address: ");
            Serial.println(WiFi.localIP());
            break;
        case WIFI_EVENT_STAMODE_DISCONNECTED:
            Serial.println("WiFi lost connection");            
            break;
        case WIFI_EVENT_ANY:
            Serial.println("other Event happend");
            break;
    }
    Serial.println("=============");
    Serial.println();
*/    
}
