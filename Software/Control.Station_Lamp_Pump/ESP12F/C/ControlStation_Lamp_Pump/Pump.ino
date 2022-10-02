#define PUMP_STATUS_FILE_NAME "/pump_status.json"
#define MAX_STATUS_SIZE 1024

void turnPumpOn(){
  digitalWrite(pump_gpio, HIGH);
  return;
}


/*
StaticJsonDocument<1024> getPumpStatusDoc(){
  StaticJsonDocument<1024> result;
  
  File statusFile = SPIFFS.open(PUMP_STATUS_FILE_NAME, "r");
  if(!statusFile){
    Serial.println("Failed to open pump status file for reading");
    return result;
  }

  size_t size = statusFile.size();
  if(size > MAX_STATUS_SIZE){
    statusFile.close();
    Serial.println("Pump sttus file size is too large");
    return result;
  }

  Serial.print("Get pump status file. Size: ");
  Serial.println(size);

  std::unique_ptr<char[]> buf(new char[size]);
  statusFile.readBytes(buf.get(), size);  
  Serial.println(buf.get());

  StaticJsonDocument<1024> doc;
  DeserializationError error = deserializeJson(doc, buf.get());

  if(error){
    Serial.print("Failed to parse pump status file: ");
    Serial.println(error.c_str());
    return result;
  }

  statusFile.close();

  result = doc;
  return result;
}
*/


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
  File statusFile = SPIFFS.open(PUMP_STATUS_FILE_NAME, "r");
  if( !statusFile){
    Serial.println("Failed to open pump status file for reading");
    return result;
  }

  size_t size = statusFile.size();
  if(size > MAX_STATUS_SIZE){
    statusFile.close();
    Serial.println("Pump sttus file size is too large");
    return result;
  }

  Serial.print("  Config file size: ");
  Serial.println(size);

  std::unique_ptr<char[]> buf(new char[size]);
  statusFile.readBytes(buf.get(), size);  
  Serial.println(buf.get());

  StaticJsonDocument<1024> doc;
  DeserializationError error = deserializeJson(doc, buf.get());

  if(error){
    Serial.print("Failed to parse pump status file: ");
    Serial.println(error.c_str());
    return result;
  }

  statusFile.close();

  bool active = doc["active"];
  long off_timestamp = doc["off-timestamp"];
  
  long now_timestamp = now();

  pumpActive = false;
  if(active){
    if (off_timestamp > now_timestamp){
      Serial.println("The pump still should run, so it will be turn on...");
      turnPump(HIGH);
      pumpActive = true;
    }else{

      Serial.println("The pump should stop, so it will be turn off...");
      
      doc["active"] = false;
      doc["off-timestamp"] = 0;

      File statusFileToWrite = SPIFFS.open(PUMP_STATUS_FILE_NAME, "w");
      if( !statusFileToWrite){
        Serial.println("Failed to write pump status");
        return result;
      }

      serializeJsonPretty(doc, statusFileToWrite);
      statusFileToWrite.close();

      turnPump(LOW);        
    }      
  }

  result = true;
  return result;
}

bool turnPumpOn(int lengthInSec){
  bool result = setPumpStatusFile(true, (now() + lengthInSec));

  if (result){
    turnPump(HIGH);
  }

  pumpActive = true;

  return result;
}

void turnPumpOff(){
  bool result = setPumpStatusFile(false, 0);

  if (result){
    turnPump(LOW);
  }
  
  pumpActive = false;
  
  return;
}

void turnPump(int status){
  digitalWrite(pump_gpio, status);
}
