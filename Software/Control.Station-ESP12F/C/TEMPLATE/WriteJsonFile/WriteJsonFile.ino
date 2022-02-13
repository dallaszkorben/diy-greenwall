#include <ArduinoJson.h>
#include "FS.h"

#define FILE_NAME "/config.json"
#define BUFF_SIZE 512

bool loadConfig(){
  File configFile = SPIFFS.open(FILE_NAME, "r");
  if( !configFile){
    Serial.println("Failed to open config file for reading");
    return false;
  }

  size_t size = configFile.size();
  if(size > BUFF_SIZE){
    Serial.println("config file size is too large");
    return false;
  }

  std::unique_ptr<char[]> buf(new char[size]);
  configFile.readBytes(buf.get(), size);
  Serial.println(buf.get());

  StaticJsonBuffer<BUFF_SIZE> jsonBuffer;
  JsonObject& json = jsonBuffer.parseObject(buf.get());

  configFile.close();

  if( !json.success()){
    Serial.println("Failed to parse config file");
    return false;
  }

  //const char* value = json["value"];
  //const char* type = json["type"];
  int value = json["value"];
  String type = json["type"];

  Serial.print("loadConfig value: ");
  Serial.println(value);
  Serial.print("loadConfig type:  ");
  Serial.println(type);

  return true;
}

boolean saveConfig(int value, String type){
  StaticJsonBuffer<BUFF_SIZE> jsonBuffer;
  JsonObject& json = jsonBuffer.createObject();
  json["value"] = value;
  json["type"] = type;

  File configFile = SPIFFS.open("/config.json", "w");
  if (!configFile){
    Serial.println("Failed to open config file for writing");
    return false;
  }

  json.printTo(configFile);
  configFile.close();
  return true;
}

void setup() {
  Serial.begin(115200);
  Serial.println("\n");
  delay(1000);
  Serial.println("vvv Reading Config file vvv");

  if(!SPIFFS.begin()){
    Serial.println("Failed t omount file system");
    return;
  }

  if(!loadConfig()){
    Serial.println("Failed to load config");
  }else{
    Serial.println("^^^    Config loaded    ^^^\n");
  }
}

int v = 0;

void loop() {
  v++;
  saveConfig(v, "Integer");
  loadConfig();
  delay(5000);
}
