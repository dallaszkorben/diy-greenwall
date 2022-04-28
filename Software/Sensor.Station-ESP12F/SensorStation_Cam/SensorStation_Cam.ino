#include <Arduino.h>
#include <WiFi.h>
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "esp_camera.h"
#include <TimeLib.h>
#include <esp_task_wdt.h>

#define BUFF_SIZE 1024

#define uS_TO_S_FACTOR 1000000
#define TIME_TO_SLEEP  10

#define CAMERA_MODEL_WROVER_KIT 
//#define CAMERA_MODEL_AI_THINKER

#include "pins.h"

WiFiClient client;

const char* ssid = "Central-Station-006";
const char* password = "viragfal";
const String serverIp = "192.168.50.3";                         // REPLACE WITH YOUR Raspberry Pi IP ADDRESS
const int serverPort = 5000;
const String serverPathToCamAdd = "cam/add/camId/5/timestamp/"; // The default serverPath should be upload.php
const String serverPathToCamRegister = "cam/register";
const String serverPathToInfoTimestamp = "info/timeStamp";
const String serverPathToInfoIsAlive = "info/isAlive";

const int timerInterval = 10000;    // 10s - time between each HTTP POST image
unsigned long previousMillis = 0;   // last time image was sent

void setup() {
  
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); //disable brownout detector

  Serial.begin(115200);
  WiFi.mode(WIFI_STA);

  Serial.print("MAC: ");
  Serial.println(WiFi.macAddress());

  Serial.print("Connecting to ");
  Serial.print(ssid);
  Serial.print(" ");
  int status = -1;
  //WL_IDLE_STATUS      = 0,
  //WL_NO_SSID_AVAIL    = 1,
  //WL_SCAN_COMPLETED   = 2,
  //WL_CONNECTED        = 3,
  //WL_CONNECT_FAILED   = 4,
  //WL_CONNECTION_LOST  = 5,
  //WL_DISCONNECTED     = 6

  connectToAP();
  
  Serial.print("   ESP32-CAM IP Address: ");
  Serial.println(WiFi.localIP());

  // --- Sync Time --- //
  if( !syncTime() ){
    Serial.println("   !!! Sync Time failed -> reboot !!!");
    //delay(10000);
    ESP.restart();
  }

//  // --- Camera Init --- //
/*  if( !initCam() ){
    Serial.println("   !!! Init Cam failed -> reboot !!!");
    ESP.restart();
  }else{
    Serial.println("   Camera init Passed");
    Serial.println();
  }
*/
}

void loop() {

  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= timerInterval) {
    previousMillis = currentMillis;

    sendPhoto();
  }
}


String sendPhoto() {
  String getAll;
  String getBody;

  connectToAP();

  initCam();

  camera_fb_t * fb = NULL;

  pinMode(ONBOARD_LED, OUTPUT);
  digitalWrite(ONBOARD_LED, HIGH);
  Serial.println("\n===");
  Serial.println("Takes photo ...");
  fb = esp_camera_fb_get();
  digitalWrite(ONBOARD_LED, LOW);

//  rtc_gpio_hold_en(GPIO_NUM_4);
  
  if (!fb) {
    Serial.println("   !!! Camera capture failed -> reboot");
    //ESP.restart();
    return "";
  }else{
    Serial.println("   Camera capture successful");
  }

  Serial.print("   Connecting to server: " + serverIp + " ");

  

  int attempt = 0;
  bool ok = false;
  while (!ok && attempt <= 10){

    attempt++;
    
    if (client.connect(serverIp.c_str(), serverPort)) {
     
      Serial.println("\n      Connection successful!");
      String head = "--RandomNerdTutorials\r\nContent-Disposition: form-data; name=\"imageFile\"; filename=\"esp32-cam.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n";
      String tail = "\r\n--RandomNerdTutorials--\r\n";

      uint16_t imageLen = fb->len;
      uint16_t extraLen = head.length() + tail.length();
      uint16_t totalLen = imageLen + extraLen;

      client.println("POST " + serverPathToCamAdd + "" + getOffsetDateString() + " HTTP/1.1");
      client.println("Host: " + serverIp);
      client.println("Content-Length: " + String(totalLen));
      client.println("Content-Type: multipart/form-data; boundary=RandomNerdTutorials");
      client.println();
      client.print(head);

      uint8_t *fbBuf = fb->buf;
      size_t fbLen = fb->len;
      for (size_t n = 0; n < fbLen; n = n + 1024) {
        if (n + 1024 < fbLen) {
          client.write(fbBuf, 1024);
          fbBuf += 1024;
        }
        else if (fbLen % 1024 > 0) {
          size_t remainder = fbLen % 1024;
          client.write(fbBuf, remainder);
        }
      }
      client.print(tail);
      client.flush();
    
      esp_camera_fb_return(fb);

      int timoutTimer = 5000;
      long startTimer = millis();
      boolean state = false;

      Serial.print("   ");
      
      // waiting for response
      while ((startTimer + timoutTimer) > millis()) {
        Serial.print(",");
        delay(1000);
        while (client.available()) {
          char c = client.read();
          if (c == '\n') {
            if (getAll.length() == 0) {
              state = true;
            }
            getAll = "";
          } else if (c != '\r') {
            getAll += String(c);
          }
          if (state == true) {
            getBody += String(c);
          }
          startTimer = millis();
        }
        if (getBody.length() > 0) {
          break;
        }
      }
      Serial.println();
      client.stop();
      Serial.println(getBody);

      ok=true;

    } else {
      getBody = "    Connection to " + serverIp +  " failed:";
      delay(1000);
      //Serial.println(getBody);
      //return "";
      //ESP.restart();
      Serial.print(".");      
    }
  }

  //ESP.restart();
//  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
//  esp_deep_sleep_start();
   
  return getBody;
}
