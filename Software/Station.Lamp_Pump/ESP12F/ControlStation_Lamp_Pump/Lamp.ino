#define LAMP_STATUS_FILE_NAME "/lamp_status.json"
#define MAX_STATUS_SIZE 1024

float MAX_PERC = 100.0;
float MAX_DUTY = 1024;
float STEP_SEC = 0.02;

double getPowByPerc(double perc){
  return 0.000199713376287*pow(min(100.0, max(0.0, perc)), 3.354734239970603); 
}








bool syncLampStatus(){

  Serial.println("Sync Lamp status");
  
  bool result = false;
  File statusFile = SPIFFS.open(LAMP_STATUS_FILE_NAME, "r");
  if( !statusFile){
    Serial.println("Failed to open Lamp status file for reading");
    return result;
  }

  size_t size = statusFile.size();
  if(size > MAX_STATUS_SIZE){
    statusFile.close();
    Serial.println("Lamp sttus file size is too large");
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
    Serial.print("Failed to parse lamp status file: ");
    Serial.println(error.c_str());
    return result;
  }

  statusFile.close();

  bool active = doc["active"];

  lampActive = active;
  if(active){
    Serial.println("The lamp should be ON so it will be turn ON...");
    turnLampOn(10);
  }else{
    Serial.println("The lamp should be OFF so it will be turn OFF...");
    //turnLampOff(0);
  }

  result = true;
  return result;
}


void setLampStatusFile(bool active){
  
  lampActive = active;

  File statusFileToRead = SPIFFS.open(LAMP_STATUS_FILE_NAME, "r");
  if(!statusFileToRead){
    Serial.println("Failed to open lamp status file for reading");
    return;
  }

  size_t size = statusFileToRead.size();
  if(size > MAX_STATUS_SIZE){
    statusFileToRead.close();
    Serial.println("Lamp status file size is too large");
    return;
  }

  Serial.print("Get Lamp status file. Size: ");
  Serial.println(size);

  std::unique_ptr<char[]> buf(new char[size]);
  statusFileToRead.readBytes(buf.get(), size);  
  Serial.println(buf.get());

  StaticJsonDocument<1024> doc;
  DeserializationError error = deserializeJson(doc, buf.get());

  if(error){
    Serial.print("Failed to parse lamp status file: ");
    Serial.println(error.c_str());
    return;
  }

  statusFileToRead.close();

// ---

  Serial.println("Set Lamp status file");
  
  doc["active"] = active;

  File statusFileToWrite = SPIFFS.open(LAMP_STATUS_FILE_NAME, "w");
  if( !statusFileToWrite){
    Serial.println("Failed to open Lamp status file");
      return;
  }

  serializeJsonPretty(doc, Serial);
  Serial.println();
  
  serializeJsonPretty(doc, statusFileToWrite);
  statusFileToWrite.close();

  return;
}













void turnLampOn(int lengthInSec){
  double steps = lengthInSec / STEP_SEC;
  double dutyStep = MAX_PERC / steps;

  double dutyCycle = 0;
  while(dutyCycle <= (MAX_PERC + dutyStep) ){

    int pwmValue = int(getPowByPerc(dutyCycle));
   
    //Serial.print("LED duty: ");
    //Serial.print(dutyCycle);
    //Serial.print("% => ");
    //Serial.println(pwmValue);
    
    analogWrite(lamp_gpio, pwmValue);

    delay(long(STEP_SEC * 1000));
    dutyCycle += dutyStep;
  }

  setLampStatusFile(true);

  return;
}

void turnLampOff(int lengthInSec){
  double steps = lengthInSec / STEP_SEC;
  double dutyStep = MAX_PERC / steps;

  double dutyCycle = MAX_PERC;
  while(dutyCycle >= -dutyStep){

    int pwmValue = int(getPowByPerc(dutyCycle));
    
    //Serial.print("LED duty: ");
    //Serial.print(dutyCycle);
    //Serial.print("% => ");
    //Serial.println(pwmValue);

    analogWrite(lamp_gpio, pwmValue);

    delay(long(STEP_SEC * 1000));
    dutyCycle -= dutyStep;
  }

  setLampStatusFile(false);

  return;
}
