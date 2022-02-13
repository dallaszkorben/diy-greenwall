#include <Arduino.h>
#include <StreamUtils.h>
#include <ArduinoJson.h>
#include "FS.h"

#define FILE_NAME "/config.json"

bool    spiffsActive = false;

const size_t capacity = JSON_ARRAY_SIZE(16) + JSON_OBJECT_SIZE(1) + 16*JSON_OBJECT_SIZE(9);
DynamicJsonBuffer jsonBuffer(capacity);

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("");

  // Read the File -> json
  String json = "";
  if (SPIFFS.begin() && SPIFFS.exists(FILE_NAME)) {

    File f = SPIFFS.open(FILE_NAME, "r");
    if(f){
      while(f.position() < f.size()){
        json += f.readStringUntil('\n');
        json += "\n";
      }
      f.close();
    }
    Serial.println("Content of the file: " + json);
  }

  JsonObject& root = jsonBuffer.parseObject( json );
  if (root.success()){
    long value = root["value"];
    String type = root["type"];
    Serial.println("Value: " + String(value));
    Serial.println("Type: " + type);
  }else{
    Serial.println("Parsing failed !!!");
  }  
}

void loop() {
  delay(3000);
}
