#include <ESP8266WiFi.h> 

void aaawifiEvent(WiFiEvent_t event) {

    switch(event) {
        case WIFI_EVENT_STAMODE_GOT_IP:
            Serial.println("WIFI is connected!");
            Serial.println("   IP address: ");
            Serial.println(WiFi.localIP());
            break;
        case WIFI_EVENT_STAMODE_DISCONNECTED:
            Serial.println("WiFi lost connection");
            Serial.println("   Reconnecting...");
            WiFi.reconnect();
            break;
        case WIFI_EVENT_STAMODE_CONNECTED:
            Serial.println("Successfully connected to Access Point");
            break;
    }
}


bool aaaconnectToAP(){
  WiFi.disconnect(true);
  delay(1000);

  WiFi.onEvent(aaawifiEvent);
  
  WiFi.begin(ssid, password);
  Serial.println("Waiting for WIFI network..."); 
}
