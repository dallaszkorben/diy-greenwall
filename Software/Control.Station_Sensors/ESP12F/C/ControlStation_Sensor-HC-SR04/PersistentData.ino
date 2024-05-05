void setupVariables(){

  // --- Open "interval" namespace in read mode ---
  stationPref.begin("interval", true); 
  intervalReportMillis = stationPref.getULong("intervalReportMillis", DEFAULT_INTERVAL_REPORT_MILLIS);
  intervalRegisterMillis = stationPref.getULong("intervalRegisterMillis", DEFAULT_INTERVAL_REGISTER_MILLIS);  
  intervalResetMillis = stationPref.getULong("intervalResetMillis", DEFAULT_INTERVAL_RESET_MILLIS);  
  intervalConnectionMillis = stationPref.getULong("intervalConnectionMillis", DEFAULT_INTERVAL_CONNECTION_MILLIS);  
  stationPref.end();

  // --- Open "sensor" namespace in read mode ---
  stationPref.begin("sensor", true); 
  sensorTempHumOutGPIO = stationPref.getInt("sensorTempHumOutGPIO", DEFAULT_SENSOR_TEMPHUM_OUT_GPIO);
  sensorDistanceTrigGPIO = stationPref.getInt("sensorDistanceTrigGPIO", DEFAULT_SENSOR_DISTANCE_TRIG_GPIO);
  sensorDistanceEchoGPIO = stationPref.getInt("sensorDistanceEchoGPIO", DEFAULT_SENSOR_DISTANCE_ECHO_GPIO);

  sensorDistanceParA = stationPref.getDouble("sensorDistanceParA", DEFAULT_SENSOR_DISTANCE_PARAMETER_A);
  sensorDistanceParB = stationPref.getDouble("sensorDistanceParB", DEFAULT_SENSOR_DISTANCE_PARAMETER_B);
  sensorDistanceParC = stationPref.getDouble("sensorDistanceParC", DEFAULT_SENSOR_DISTANCE_PARAMETER_C);  
  
  stationPref.end();
  
  // --- Open "station" namespace in read mode ---
  stationPref.begin("station", true); 
  stationId = stationPref.getString("stationId", DEFAULT_STATION_ID);
  stationPref.end();

  // --- Open "general" namespace in read mode ---
  stationPref.begin("general", true); 
  needToReset = stationPref.getBool("needToReset", DEFAULT_NEED_TO_RESET);
  needToReport = stationPref.getBool("needToReport", DEFAULT_NEED_TO_REPORT);
  stationPref.end();

  // --- Open "client" namespace in read mode ---
  stationPref.begin("client", true); 
  clientIp = stationPref.getString("clientIp", DEFAULT_CLIENT_IP);
  clientPort = stationPref.getString("clientPort", DEFAULT_CLIENT_PORT);
  clientPathToRegister = stationPref.getString("clientPathToRegister", DEFAULT_CLIENT_PATH_TO_REGISTER);
  clientPathToReport = stationPref.getString("clientPathToReport", DEFAULT_CLIENT_PATH_TO_REPORT);
  clientPathToInfoTimestamp = stationPref.getString("clientPathToInfoTimestamp", DEFAULT_CLIENT_PATH_TO_INFO_TIMESTAMP);
  stationPref.end();


  // --- Show new values ---
  Serial.println();
  Serial.println("========== Setup variable ==========");
  Serial.println("version: " + version);

  Serial.println("Mutable value variables:");

  Serial.println("   intervalReportMillis: " + String(intervalReportMillis));
  Serial.println("   intervalRegisterMillis: " + String(intervalRegisterMillis) );
  Serial.println("   intervalResetMillis: " + String(intervalResetMillis) );
  Serial.println("   intervalConnectionMillis: " + String(intervalConnectionMillis) );
  Serial.println("   stationId: " + stationId );
  Serial.println("   sensorTempHumOutGPIO: " + String(sensorTempHumOutGPIO) );
  Serial.println("   sensorDistanceEchoGPIO: " + String(sensorDistanceEchoGPIO) );
  Serial.println("   sensorDistanceTrigGPIO: " + String(sensorDistanceTrigGPIO) );
  Serial.println("   sensorDistanceParA: " + String(sensorDistanceParA) );
  Serial.println("   sensorDistanceParB: " + String(sensorDistanceParB) );
  Serial.println("   sensorDistanceParC: " + String(sensorDistanceParC) );

  Serial.println("   clientIp: " + String(clientIp) );
  Serial.println("   clientPort: " + String(clientPort) );
  Serial.println("   clientPathToRegister: " + String(clientPathToRegister) );
  Serial.println("   clientPathToReport: " + String(clientPathToReport) );
  Serial.println("   clientPathToInfoTimestamp: " + String(clientPathToInfoTimestamp) );

  Serial.println("   needToReport: " + String(needToReport ));
  Serial.println("   needToReset: " + String(needToReset ));
  Serial.println("====================================");
}

/*
 * Persist variable individually
 */
void persistVariable(String variable){

  if(variable.compareTo("needToReset") == 0){
  
    // Open "general" namespace in read/write mode
    stationPref.begin("general", false); 

    // persist the needToReset variable
    stationPref.putBool("needToReset", needToReset);

    // Close the name space
    stationPref.end();    
  }  
}

void persistVariables(){

  //--- Verify values ---
  //
  if(stationId.compareTo("") == 0){
    stationId = DEFAULT_STATION_ID;
  }

  if( intervalReportMillis < 1000 ){
    intervalReportMillis = DEFAULT_INTERVAL_REPORT_MILLIS;
  }

  if( intervalRegisterMillis < 1000 ){
    intervalRegisterMillis = DEFAULT_INTERVAL_REGISTER_MILLIS;
  }

  if( intervalConnectionMillis < 1000 ){
    intervalConnectionMillis = DEFAULT_INTERVAL_CONNECTION_MILLIS;
  }
  // --- Persists variables ---
  
  // Open "interval" namespace in read/write mode
  stationPref.begin("interval", false); 
  stationPref.putULong("intervalReportMillis", intervalReportMillis);
  stationPref.putULong("intervalRegisterMillis", intervalRegisterMillis);
  stationPref.putULong("intervalResetMillis", intervalResetMillis);
  stationPref.putULong("intervalConnectionMillis", intervalConnectionMillis);
  stationPref.end();

  stationPref.begin("station", false); 
  stationPref.putString("stationId", stationId);
  stationPref.end();

  stationPref.begin("sensor", false); 
  stationPref.putInt("sensorTempHumOutGPIO", sensorTempHumOutGPIO);
  stationPref.putInt("sensorDistanceEchoGPIO", sensorDistanceEchoGPIO);
  stationPref.putInt("sensorDistanceTrigGPIO", sensorDistanceTrigGPIO);
  stationPref.putDouble("sensorDistanceParA", sensorDistanceParA);
  stationPref.putDouble("sensorDistanceParB", sensorDistanceParB);
  stationPref.putDouble("sensorDistanceParC", sensorDistanceParC);

  stationPref.end();

  stationPref.begin("client", false); 
  stationPref.putString("clientIp", clientIp);
  stationPref.putString("clientPort", clientPort);
  stationPref.putString("clientPathToRegister", clientPathToRegister);
  stationPref.putString("clientPathToReport", clientPathToReport);
  stationPref.putString("clientPathToInfoTimestamp", clientPathToInfoTimestamp);
    
  stationPref.end();
  
  stationPref.begin("general", false); 
  stationPref.putBool("needToReset", needToReset);
  stationPref.putBool("needToReport", needToReport);
  stationPref.end();

  // --- Show new values ---
  Serial.println("===============================");
  Serial.println("   version: " + version);
  Serial.println("   New Mutable value variables:");
  Serial.println("      intervalReportMillis: " + String(intervalReportMillis));
  Serial.println("      intervalRegisterMillis: " + String(intervalRegisterMillis) );
  Serial.println("      intervalResetMillis: " + String(intervalResetMillis) );  
  Serial.println("      intervalConnectionMillis: " + String(intervalConnectionMillis) );  
  Serial.println("      stationId: " + stationId );
  Serial.println("      sensorTempHumOutGPIO: " + String(sensorTempHumOutGPIO) );
  Serial.println("      sensorDistanceEchoGPIO: " + String(sensorDistanceEchoGPIO) );
  Serial.println("      sensorDistanceTrigGPIO: " + String(sensorDistanceTrigGPIO) );
  Serial.println("      sensorDistanceParA: " + String(sensorDistanceParA) );
  Serial.println("      sensorDistanceParB: " + String(sensorDistanceParB) );
  Serial.println("      sensorDistanceParC: " + String(sensorDistanceParC) );

  Serial.println("      clientIp: " + String(clientIp) );
  Serial.println("      clientPort: " + String(clientPort) );
  Serial.println("      clientPathToRegister: " + String(clientPathToRegister) );
  Serial.println("      clientPathToReport: " + String(clientPathToReport) );
  Serial.println("      clientPathToInfoTimestamp: " + String(clientPathToInfoTimestamp) );

  Serial.println("      needToReport: " + String(needToReport ));
  Serial.println("      needToReset: " + String(needToReset));
  Serial.println("===============================");
}
