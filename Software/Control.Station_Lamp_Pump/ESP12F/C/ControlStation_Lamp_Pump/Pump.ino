#define PUMP_STATUS_FILE_NAME "/pump_status.json"
#define MAX_STATUS_SIZE 1024

void turnPumpOn(){
  digitalWrite(pump_gpio, HIGH);
  return;
}

//bool setPumpStatusFile(StaticJsonDocument<1024> doc, bool active, long timestamp){
bool setPumpStatusFile(bool active, long timestamp){
  bool result = false;

// ---

  File statusFileToRead = SPIFFS.open(PUMP_STATUS_FILE_NAME, "r");
  if(!statusFileToRead){
    Serial.println("Failed to open pump status file for reading");
    return result;
  }

  size_t size = statusFileToRead.size();
  if(size > MAX_STATUS_SIZE){
    statusFileToRead.close();
    Serial.println("Pump status file size is too large");
    return result;
  }

  Serial.print("Get pump status file. Size: ");
  Serial.println(size);

  std::unique_ptr<char[]> buf(new char[size]);
  statusFileToRead.readBytes(buf.get(), size);  
  Serial.println(buf.get());

  StaticJsonDocument<1024> doc;
  DeserializationError error = deserializeJson(doc, buf.get());

  if(error){
    Serial.print("Failed to parse pump status file: ");
    Serial.println(error.c_str());
    return result;
  }

  statusFileToRead.close();

// ---

  Serial.println("Set pump status file");
  
  doc["active"] = active;
  doc["off-timestamp"] = timestamp;

  File statusFileToWrite = SPIFFS.open(PUMP_STATUS_FILE_NAME, "w");
  if( !statusFileToWrite){
    Serial.println("Failed to open pump status file");
      return result;
  }

  serializeJsonPretty(doc, Serial);
  Serial.println();
  
  serializeJsonPretty(doc, statusFileToWrite);
  statusFileToWrite.close();
  result = true;
  return result;
}


bool syncPumpStatus(){

  Serial.println("Sync Pump status");
  bool result = false;

//  File statusFile = SPIFFS.open(PUMP_STATUS_FILE_NAME, "r");
//  if( !statusFile){
//    Serial.println("Failed to open pump status file for reading");
//    return result;
//  }
//
//  size_t size = statusFile.size();
//  if(size > MAX_STATUS_SIZE){
//    statusFile.close();
//    Serial.println("Pump status file size is too large");
//    return result;
//  }
//
//  Serial.print("  Config file size: ");
//  Serial.println(size);
//
//  std::unique_ptr<char[]> buf(new char[size]);
//  statusFile.readBytes(buf.get(), size);  
//  Serial.println(buf.get());
//
//  StaticJsonDocument<1024> doc;
//  DeserializationError error = deserializeJson(doc, buf.get());
//
//  if(error){
//    Serial.print("Failed to parse pump status file: ");
//    Serial.println(error.c_str());
//    return result;
//  }
//
//  statusFile.close();
//
//  pump_active = doc["active"];
//  pump_off_timestamp = doc["off-timestamp"];

  long now_timestamp = now();

  if (pump_off_timestamp > now_timestamp){
      Serial.println("The pump still should run, so it will be turned on...");
      turnPump(HIGH);
      pump_active = true;
  }else{
      Serial.println("The pump should stop, so it will be turned off...");

//      doc["active"] = false;
//      doc["off-timestamp"] = 0;
//
//      File statusFileToWrite = SPIFFS.open(PUMP_STATUS_FILE_NAME, "w");
//      if( !statusFileToWrite){
//        Serial.println("Failed to write pump status");
//        return result;
//      }
//
//      serializeJsonPretty(doc, statusFileToWrite);
//      statusFileToWrite.close();
//
//      turnPump(LOW);

    turnOffPumpImmediately();
  }
  
  result = true;
  return result;  
}

void turnOffPumpImmediately(){
  turnPump(LOW);
  pump_active = false;
  pump_off_timestamp = 0;
}

bool turnPumpOn(int lengthInSec){
//  bool result = setPumpStatusFile(true, (now() + lengthInSec));
//
//  if (result){
//    turnPump(HIGH);
//  }
//
//  pumpActive = true;

  pump_active = true;
  pump_off_timestamp = now() + lengthInSec;
  turnPump(HIGH);

//  return result;
  return true;
}

void turnPumpOff(){
//  bool result = setPumpStatusFile(false, 0);
//
//  if (result){
//    turnPump(LOW);
//  }
//  
//  pumpActive = false;

  turnPump(LOW);
  pump_active = false;
  pump_off_timestamp = 0;
  
  return;
}

void turnPump(int status){
  digitalWrite(pump_gpio, status);
}
