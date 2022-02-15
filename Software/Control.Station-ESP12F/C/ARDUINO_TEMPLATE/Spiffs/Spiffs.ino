#include <string.h>
#include "FS.h"

#define FILE_NAME "/myfile.txt"

bool    spiffsActive = false;

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Start filing subsystem
  if (SPIFFS.begin()) {
      Serial.println("SPIFFS is Active");
      spiffsActive = true;
  } else {
      Serial.println("Unable to activate SPIFFS ...");
  }
  delay(2000);
}

void loop() {
  if (spiffsActive) {  

    if (SPIFFS.exists(FILE_NAME)) {

      // Open the file to Append
      File f = SPIFFS.open(FILE_NAME, "a");
      if(f){
        String toAppend = "extra line";
        f.println(toAppend);
        f.close();
        Serial.println("Add new line: " + toAppend);
      }else{
        Serial.println("Unable to open file for reading: " + String(FILE_NAME));
      }

      // Open the file to Read
      f = SPIFFS.open(FILE_NAME, "r");
      if(f){
        String s = "";
        while(f.position() < f.size()){
          s += "\n   ";
          s += f.readStringUntil('\n');
        }
        Serial.println("Content of the file: " + s);
        f.close();
      }else{
        Serial.println("Unable to open file for reading: " + String(FILE_NAME));
      }
   
    }else{
      Serial.println(String(FILE_NAME) + " was not found ...");
    }
  }

  while(true){
    yield();
  }
}
