void modifyFrameSize();

void setupVariables(){

  // Open "cam" namespace in read/write mode
  camPref.begin("cam", false); 

  needToReset = camPref.getBool("needToReset", DEFAULT_NEED_TO_RESET);

  camId = camPref.getString("camId", DEFAULT_CAMID);
  camQuality = camPref.getString("camQuality", DEFAULT_CAMQUALITY);
  camRotate = camPref.getString("camRotate", DEFAULT_CAMROTATE);
  intervalFrameMillis = camPref.getULong("intervalFrame", DEFAULT_INTERVALFRAME);
  camPref.end();

  // Open "client" namespace in read/write mode
  clientPref.begin("client", false); 

  clientIp = clientPref.getString("clientIp", DEFAULT_CLIENTIP);
  clientPort = clientPref.getString("clientPort", DEFAULT_CLIENTPORT);

  clientPref.end();

  // --- Show new values ---

  Serial.println("Mutable value variables:");
  Serial.println("   needToReset: " + String(needToReset));
  Serial.println("   camId: " + camId );
  Serial.println("   camQuality: " + camQuality );
  Serial.println("   camRotate: " + camRotate );
  Serial.println("   intervalFrameMillis: " + String(intervalFrameMillis) );
  Serial.println("   clientIp: " + clientIp );
  Serial.println("   clientPort: " + clientPort ); 
}

void saveVariable(String variable){

  if(variable.compareTo("needToReset") == 0){
  
    // Open "cam" namespace in read/write mode
    camPref.begin("cam", false); 

    // persist the needToReset variable
    camPref.putBool("needToReset", needToReset);

    // Close the name space
    camPref.end();
    
  }
  
}

void saveVariables(){

  //--- Verify values ---
  // camQuality: 96X96,QQVGA,QCIF,HQVGA,240X240,QVGA,CIF,HVGA,VGA,SVGA,XGA,HD,SXGA,UXGA
  if(
    camQuality.compareTo("96X96") != 0 && 
    camQuality.compareTo("QQVGA") != 0 &&
    camQuality.compareTo("QCIF") != 0 &&
    camQuality.compareTo("HQVGA") != 0 &&
    camQuality.compareTo("240X240") != 0 &&
    camQuality.compareTo("QVGA") != 0 &&
    camQuality.compareTo("CIF") != 0 &&
    camQuality.compareTo("HVGA") != 0 &&
    camQuality.compareTo("VGA") != 0 &&
    camQuality.compareTo("SVGA") != 0 &&
    camQuality.compareTo("XGA") != 0 &&
    camQuality.compareTo("HD") != 0 &&  
    camQuality.compareTo("SXGA") != 0 &&
    camQuality.compareTo("UXGA") != 0){

    camQuality = DEFAULT_CAMQUALITY;
  }

  // camRotate: 0, 1, 2, 3
  if(
    camRotate.compareTo("1") != 0 && 
    camRotate.compareTo("2") != 0 &&
    camRotate.compareTo("3") != 0 &&
    camRotate.compareTo("0") != 0){

    camRotate = DEFAULT_CAMROTATE;
  }

  if( intervalFrameMillis < 1000 ){
    intervalFrameMillis = DEFAULT_INTERVALFRAME;
  }

  // --- Persists variables ---
  
  // Open "cam" namespace in read/write mode
  camPref.begin("cam", false); 

  camPref.putBool("needToReset", needToReset);
  camPref.putString("camId", camId);
  camPref.putString("camQuality", camQuality);
  camPref.putString("camRotate", camRotate);
  camPref.putULong("intervalFrame", intervalFrameMillis);
  
  camPref.end();

  // --- Show new values ---
  
  Serial.println("   New Mutable value variables:");
  Serial.println("      needToReset: " + String(needToReset));
  Serial.println("      camId: " + camId );
  Serial.println("      camQuality: " + camQuality );
  Serial.println("      camRotate: " + camRotate );
  Serial.println("      intervalFrameMillis: " + String(intervalFrameMillis) );
  Serial.println("      clientIp: " + clientIp );
  Serial.println("      clientPort: " + clientPort );

  // If I restart the module, the HTTP request will be ended with error: Connection reset by peer
  // If I do not restart the module, the camQuality will not affect until the next restart
  //ESP.restart();

}
