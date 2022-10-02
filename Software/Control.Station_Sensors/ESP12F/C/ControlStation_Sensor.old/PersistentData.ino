
void setupVariables(){

  // --- Open "interval" namespace in read/write mode ---
  stationPref.begin("interval", false); 
  intervalReportMillis = stationPref.getULong("intervalReportMillis", DEFAULT_INTERVAL_REPORT_MILLIS);
  intervalRegisterMillis = stationPref.getULong("intervalRegisterMillis", DEFAULT_INTERVAL_REGISTER_MILLIS);  
  stationPref.end();

  // --- Open "station" namespace in read/write mode ---
  stationPref.begin("station", false); 
  stationId = stationPref.getString("stationId", DEFAULT_STATION_ID);
  stationPref.end();

  // --- Open "general" namespace in read/write mode ---
  stationPref.begin("general", false); 
  needToReset = stationPref.getBool("needToReset", DEFAULT_NEED_TO_RESET);
  stationPref.end();

  // --- Show new values ---
  Serial.println("Mutable value variables:");
  Serial.println("   intervalReportMillis: " + String(intervalReportMillis));
  Serial.println("   intervalRegisterMillis: " + String(intervalRegisterMillis) );
  Serial.println("   stationId: " + stationId );
  Serial.println("   needToReset: " + String(needToReset ));
}

/*
 * Persist variable individually
 */
void saveVariable(String variable){

  if(variable.compareTo("needToReset") == 0){
  
    // Open "general" namespace in read/write mode
    stationPref.begin("general", false); 

    // persist the needToReset variable
    stationPref.putBool("needToReset", needToReset);

    // Close the name space
    stationPref.end();
    
  }
  
}

void saveVariables(){

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
  
  // --- Persists variables ---
  
  // Open "interval" namespace in read/write mode
  stationPref.begin("interval", false); 
  stationPref.putULong("intervalReportMillis", intervalReportMillis);
  stationPref.putULong("intervalRegisterMillis", intervalRegisterMillis);
  stationPref.end();

  stationPref.begin("station", false); 
  stationPref.putString("stationId", stationId);
  stationPref.end();

  stationPref.begin("general", false); 
  stationPref.putBool("needToReset", needToReset);
  stationPref.end();

  // --- Show new values ---
  Serial.println("   New Mutable value variables:");
  Serial.println("      intervalReportMillis: " + String(intervalReportMillis));
  Serial.println("      intervalRegisterMillis: " + String(intervalRegisterMillis) );
  Serial.println("      stationId: " + stationId );
  Serial.println("      needToReset: " + String(needToReset));

  // If I restart the module, the HTTP request will be ended with error: Connection reset by peer
  // If I do not restart the module, the camQuality will not affect until the next restart
  //ESP.restart();

}
