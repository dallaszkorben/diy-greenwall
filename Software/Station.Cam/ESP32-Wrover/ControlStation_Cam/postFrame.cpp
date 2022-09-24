#include <HTTPClient.h>
#include <base64.h>
#include <ArduinoJson.h>
#include <TimeLib.h>
#include "esp_camera.h"

//HTTPC_ERROR_CONNECTION_REFUSED (-1)
//HTTPC_ERROR_SEND_HEADER_FAILED (-2)
//HTTPC_ERROR_SEND_PAYLOAD_FAILED (-3)
//HTTPC_ERROR_NOT_CONNECTED (-4)
//HTTPC_ERROR_CONNECTION_LOST (-5)
//HTTPC_ERROR_NO_STREAM (-6)
//HTTPC_ERROR_NO_HTTP_SERVER (-7)
//HTTPC_ERROR_TOO_LESS_RAM (-8)
//HTTPC_ERROR_ENCODING (-9)
//HTTPC_ERROR_STREAM_WRITE (-10)
//HTTPC_ERROR_READ_TIMEOUT (-11)
//To get the meaning of code use: htt.errorToString(responseCode)

extern String camRotate;

camera_fb_t* takePhoto();

boolean postFrame(WiFiClient client, String clientIp, String clientPort, String clientPathToCamFrameSave){
  String getAll;
  String payload;
  String boundary = "XmyOwnBoundryX";

  Serial.println("Tries to send POST " + clientPathToCamFrameSave);

  camera_fb_t * fb = NULL;
  fb = esp_camera_fb_get();
  if(!fb) {
    Serial.println("   Camera capture failed");
    return false;
  }
  Serial.println("   Image was taken...");
  
  if (client.connect(clientIp.c_str(), clientPort.toInt())) {
    Serial.println("   Connection successful!");    
    String head = "--" + boundary + "\r\nContent-Disposition: form-data; name=\"frameFile\"; filename=\"esp32-cam.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n";
    String tail = "\r\n--" + boundary + "--\r\n";

    uint32_t imageLen = fb->len;
    uint32_t extraLen = head.length() + tail.length();
    uint32_t totalLen = imageLen + extraLen;
  
    client.println("POST /" + clientPathToCamFrameSave + " HTTP/1.1");
    client.println("Host: " + clientIp);
    client.println("Content-Length: " + String(totalLen));
    //client.println("X-camRotate: " + camRotate);
    client.println("Content-Type: multipart/form-data; boundary=" + boundary);
    client.println();
    client.print(head);
  
    uint8_t *fbBuf = fb->buf;
    size_t fbLen = fb->len;
    for (size_t n=0; n<fbLen; n=n+1024) {
      if (n+1024 < fbLen) {
        client.write(fbBuf, 1024);
        fbBuf += 1024;
      }
      else if (fbLen%1024>0) {
        size_t remainder = fbLen%1024;
        client.write(fbBuf, remainder);
      }
    }   
    client.print(tail);
    
    esp_camera_fb_return(fb);
    
    int timoutTimer = 4000;
    long startTimer = millis();
    boolean state = false;

    Serial.print("   Waiting for the response: ");
    while ((startTimer + timoutTimer) > millis()) {
      Serial.print("+");
      delay(500);      
      while (client.available()) {
        char c = client.read();
        if (c == '\n') {
          if (getAll.length()==0) { state=true; }
          getAll = "";
        }
        else if (c != '\r') { getAll += String(c); }
        if (state==true) { payload += String(c); }
        startTimer = millis();
      }
      if (payload.length()>0) { break; }
    }
    Serial.println();
    client.stop();

    //pharse the response
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, payload);

    if (error) {
      Serial.println(F("   !!! Response parsing failed!"));      
      return false;
    }
    String result = doc["result"];      
    payload.trim();      
    Serial.println("   Payload: " + payload );

    if(result == "OK"){    
      return true;
    }else{
      return false;
    }
  }else {
    Serial.println("   !!! Connection to " + clientIp + " FAILED !!!");
    return false;
  }
}
