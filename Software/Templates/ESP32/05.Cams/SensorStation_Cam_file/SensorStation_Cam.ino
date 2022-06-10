
#define CAMERA_MODEL_AI_THINKER
#define FILE_PHOTO "/photo.jpg"

//ESP8266WebServer server(80);
#include "soc/soc.h"           // Disable brownour problems
#include "soc/rtc_cntl_reg.h"  // Disable brownour problems

#include <HTTPClient.h>
#include "esp_camera.h"
#include <WiFi.h>
#include "camera_pins.h"
#include "FS.h"
#include "SPIFFS.h"
#include <ArduinoJson.h>
#include <TimeLib.h>
#include "img_converters.h"



HTTPClient http;
WiFiClient wifiClient;

// --- Config file ---
String essid;
String password;
String webserver_ip;
String webserver_path_info_timestamp;
String webserver_path_cam_register;
String webserver_path_info_is_alive;

String cam_id;
int led_status_gpio;
int led_status_inverse;
int register_interval_sec;
int reset_hours;
// -------------------

// OV2640 camera module
camera_config_t config;

void setup() {
  Serial.begin(115200);
  Serial.println("\n");
  delay(2000);

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

  // Turn-off the 'brownout detector'
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
  
  // --- Config --- //
  Serial.println("========== Setup ==========");
  Serial.println("vvv Reading Config file vvv");

  if(!SPIFFS.begin(true)){
    Serial.println("Failed to mount file system");
    delay(5000);
    ESP.restart();    
  }else{
    Serial.println("SPIFFS mounted successfully");
  }

  if(!loadConfig()){
    Serial.println("Failed to load config");
    delay(5000);
    ESP.restart();
  }else{
    Serial.println("^^^    Config loaded    ^^^\n");    
  }

  // --- Connect to WiFi --- //
  if (!connectToWiFi()){
    Serial.println("Failed to connect to WiFi");
    delay(5000);
    ESP.restart();
  }

  Serial.println("\n");

  // --- Sync Time --- //
  syncTime();

  // --- Configure Cam --- //
  if(!configureCam()){
    Serial.println("Failed to config camera");
    delay(5000);
    ESP.restart();
  }else{
    Serial.println("Camera configured successfully");
  }

  // --- Register Cam --- //
//  registerCam();

//  // --- Web Server --- //
//  server.on("/isAlive", HTTP_GET, handleIsAlive );
//  server.on("/lamp/on", HTTP_POST, handleLampOn);
//  server.on("/lamp/off", HTTP_POST, handleLampOff);
//  server.onNotFound(handleNotFound);
//  server.begin();
//  Serial.println("HTTP server started");

  Serial.println("===========================\n");

  
 
}

int cycle = 0;
void loop() {

//  server.handleClient();
  
//  if(cycle%60 == 0){
//    connectToWiFiIfNotConnected();
//    //isAlive();
//  }
//
//  cycle++;

  capturePhoto();


  String webserver_path_reg_picture = "/reg/picture/";
  String url = "http://" + webserver_ip + "/" + webserver_path_reg_picture;

  Serial.print("Try to send picture: POST ");
  Serial.println(url);
  
  http.begin(wifiClient, url);
  http.addHeader("Content-Type", "image/jpeg");
  String httpRequestData = "";
  int httpREsponseCode = http.POST(httpRequestData);
  if (httpREsponseCode > 0) {
    String payload = http.getString();   //Get the request response payload
    Serial.print("Successfully sent: ");
    Serial.print(httpREsponseCode);
    Serial.print(". Response: ");
    Serial.println(payload);
  }else{
    Serial.print("Failed to send: ");
    Serial.print(httpREsponseCode);    
  }

  
  delay(10000);
}
