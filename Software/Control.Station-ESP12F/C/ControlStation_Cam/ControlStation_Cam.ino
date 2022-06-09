#include "esp_camera.h"
#include <WiFi.h>

//
// WARNING!!! PSRAM IC required for UXGA resolution and high JPEG quality
//            Ensure ESP32 Wrover Module or other board with PSRAM is selected
//            Partial images will be transmitted if image exceeds buffer size
//

// Select camera model
#define CAMERA_MODEL_WROVER_KIT         // Has PSRAM
//#define CAMERA_MODEL_ESP_EYE          // Has PSRAM
//#define CAMERA_MODEL_M5STACK_PSRAM    // Has PSRAM
//#define CAMERA_MODEL_M5STACK_V2_PSRAM // M5Camera version B Has PSRAM
//#define CAMERA_MODEL_M5STACK_WIDE     // Has PSRAM
//#define CAMERA_MODEL_M5STACK_ESP32CAM // No PSRAM
//#define CAMERA_MODEL_AI_THINKER       // Has PSRAM
//#define CAMERA_MODEL_TTGO_T_JOURNAL   // No PSRAM
#include "camera_pins.h"

//const char* ssid = "Central-Station-006";
//const char* password = "viragfal";
const char* ssid = "blabla2.4";
const char* password = "Elmebetegek Almaiban";

//const String serverIp = "192.168.50.3";                         // REPLACE WITH YOUR Raspberry Pi IP ADDRESS
const String serverIp = "192.168.0.104";                        // REPLACE WITH YOUR Raspberry Pi IP ADDRESS

const String camId = "5";
const int serverPort = 80;
const String serverPathToCamFrameSave = "cam/frame/save/camId/" + camId + "/timestamp/"; // The default serverPath should be upload.php
const String serverPathToCamRegister = "cam/register";
const String serverPathToInfoTimestamp = "info/timeStamp";

#include <HTTPClient.h>
HTTPClient http;
WiFiClient wifiClient;

  
void startCameraServer();

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

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
  
  // if PSRAM IC present, init with UXGA resolution and higher JPEG quality
  //                      for larger pre-allocated frame buffer.
  //FRAMESIZE_96X96,    // 96x96
  //FRAMESIZE_QQVGA,    // 160x120
  //FRAMESIZE_QCIF,     // 176x144
  //FRAMESIZE_HQVGA,    // 240x176
  //FRAMESIZE_240X240,  // 240x240
  //FRAMESIZE_QVGA,     // 320x240
  //FRAMESIZE_CIF,      // 400x296
  //FRAMESIZE_HVGA,     // 480x320
  //FRAMESIZE_VGA,      // 640x480
  //FRAMESIZE_SVGA,     // 800x600
  //FRAMESIZE_XGA,      // 1024x768
  //FRAMESIZE_HD,       // 1280x720
  //FRAMESIZE_SXGA,     // 1280x1024
  //FRAMESIZE_UXGA,     // 1600x1200
  //// 3MP Sensors
  //FRAMESIZE_FHD,      // 1920x1080
  //FRAMESIZE_P_HD,     //  720x1280
  //FRAMESIZE_P_3MP,    //  864x1536
  //FRAMESIZE_QXGA,     // 2048x1536
  //// 5MP Sensors
  //FRAMESIZE_QHD,      // 2560x1440
  //FRAMESIZE_WQXGA,    // 2560x1600
  //FRAMESIZE_P_FHD,    // 1080x1920
  //FRAMESIZE_QSXGA,    // 2560x1920
  
  if(psramFound()){
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }
  
#if defined(CAMERA_MODEL_ESP_EYE)
  pinMode(13, INPUT_PULLUP);
  pinMode(14, INPUT_PULLUP);
#endif

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t * s = esp_camera_sensor_get();
  // initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1); // flip it back
    s->set_brightness(s, 1); // up the brightness just a bit
    s->set_saturation(s, -2); // lower the saturation
  }
  // drop down frame size for higher initial frame rate
  //s->set_framesize(s, FRAMESIZE_QVGA);

#if defined(CAMERA_MODEL_M5STACK_WIDE) || defined(CAMERA_MODEL_M5STACK_ESP32CAM)
  s->set_vflip(s, 1);
  s->set_hmirror(s, 1);
#endif

  Serial.println();
  Serial.print("MAC: ");
  Serial.println(WiFi.macAddress());

//  Serial.printf("Try to connect to Access Point %s ", ssid);

  // --- Connect to Access Point --- //  
  if (!connectToApIfNotConnected()){
    Serial.println("    !!! Connection failed -> reboot !!!");
    //delay(10000);
    ESP.restart();
  }

  // --- Sync Time --- //
  if( !syncTime() ){
    Serial.println("    !!! Sync Time failed -> reboot !!!");   
    ESP.restart();
  }

  // --- Register Camera Stream --- //
  if ( !registerCam() ){
    Serial.println("    !!! Cam register failed -> reboot !!!");   
    ESP.restart();    
  }
   
  // --- Start Camera Server --- //
  startCameraServer();

  Serial.print("    GET http://");
  Serial.print(WiFi.localIP());
  Serial.println(":80/capture");

  Serial.print("    GET http://");
  Serial.print(WiFi.localIP());
  Serial.println(":81/stream");

}

void loop() {
/*
  if(connectToApIfNotConnected()){
    syncTime();
  }
  Serial.println("");
  // put your main code here, to run repeatedly:
  //WiFi.reconnect();
  delay(2000);
  //Serial.println(WiFi.localIP());
*/  
}
