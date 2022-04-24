#include <Arduino.h>
#include <WiFi.h>
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "esp_camera.h"
#include <TimeLib.h>

#define BUFF_SIZE 1024

#define uS_TO_S_FACTOR 1000000
#define TIME_TO_SLEEP  10

#include <esp_task_wdt.h>

const char* ssid = "Central-Station-006";
const char* password = "viragfal";
const String serverIp = "192.168.50.3";   // REPLACE WITH YOUR Raspberry Pi IP ADDRESS
const String serverPathToCamAdd = "cam/add/camId/5/timestamp/";     // The default serverPath should be upload.php
const String serverPathToCamRegister = "cam/register";
const String serverPathToInfoTimestamp = "info/timeStamp";
const String serverPathToInfoIsAlive = "info/isAlive";
const int serverPort = 5000;


//
//String cam_id;
////int lamp_gpio;
////int pump_gpio;
//int led_status_gpio;
//int led_status_inverse;
//int register_interval_sec;
//int reset_hours;


//WiFiClient client;

// CAMERA_MODEL_AI_THINKER
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

const int timerInterval = 30000;    // time between each HTTP POST image
unsigned long previousMillis = 0;   // last time image was sent

void setup() {
  
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); //disable brownout detector

  // Watchdog
  //esp_task_wdt_init(30, true);
  //esp_task_wdt_add(NULL);
  
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);





  
  Serial.println();
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



  //WiFi.begin(ssid, password);
  //while (WiFi.status() != WL_CONNECTED) {
  //      delay(1000);
  //      Serial.print(".");
  //}

  int loop = 0;
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED && loop <= 10) {
      delay(1000);
      Serial.print(".");
      loop++;
  }
  if(loop > 20){
     ESP.restart();
  }
  
  Serial.println();
  Serial.print("   ESP32-CAM IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  // --- Sync Time --- //
  if( !syncTime() ){
    Serial.println("!!! Wait 1 minute and then restart !!!");
    delay(10000);
    ESP.restart();
  }

  // --- Camera Init --- //
  Serial.println("Camera Initialization");
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  // init with high specs to pre-allocate larger buffers
  if (psramFound()) {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 10;  //0-63 lower number means higher quality
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_CIF;
    config.jpeg_quality = 12;  //0-63 lower number means higher quality
    config.fb_count = 1;
  }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("   Camera init failed with error 0x%x", err);
    delay(1000);
    ESP.restart();
  }else{
    Serial.println("   Camera init Passed");
  }

  sendPhoto();
}

void loop() {
}
/*  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= timerInterval) {
    sendPhoto();
    previousMillis = currentMillis;


    Serial.println("!!! Restart !!!");
    ESP.restart();
  }
}
*/
String sendPhoto() {
  String getAll;
  String getBody;

  camera_fb_t * fb = NULL;

//  pinMode(4, OUTPUT);
//  digitalWrite(4, HIGH);

  pinMode(33, OUTPUT);
  digitalWrite(33, LOW);

  fb = esp_camera_fb_get();

  digitalWrite(33, HIGH);

  //digitalWrite(4, LOW);
  ////rtc_gpio_hold_en(GPIO_NUM_4);

  Serial.println();
  Serial.println("===");
  if (!fb) {
    Serial.println("   !!! Camera capture failed");
    delay(1000);
    ESP.restart();
  }else{
    Serial.println("   Camera capture successful");
  }

  Serial.println("   Connecting to server: " + serverIp);

  WiFiClient client;


  int connection = 1;
  while (connection == 1){

    Serial.print("      Connected: ");
    Serial.println(client.connected());

    Serial.print("      WiFi status: ");
    Serial.println(WiFi.status());

    
    if (client.connect(serverIp.c_str(), serverPort)) {
     
      Serial.println("      Connection successful!");
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
      connection = 0;
    
    
      esp_camera_fb_return(fb);

      int timoutTimer = 10000;
      long startTimer = millis();
      boolean state = false;

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

      delay(10000);

    } else {
      getBody = "Connection to " + serverIp +  " failed:";
      Serial.println(getBody);
      
    }
    connection = 0;
  }

  //ESP.restart();

  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  esp_deep_sleep_start();
   
  return getBody;
}
