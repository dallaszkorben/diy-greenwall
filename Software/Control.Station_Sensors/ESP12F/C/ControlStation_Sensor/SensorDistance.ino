

bool configureDistanceSensor(){

  bool ret = true;

  pinMode(sensorDistanceTrigGPIO, OUTPUT); // Sets the trigPin as an Output
  pinMode(sensorDistanceEchoGPIO, INPUT);  // Sets the echoPin as an Input

  double dist = getSampleOfDistance(10);

  if(dist == NULL){
    ret = false;  

    Serial.println("!!! HCSR04 sensor configuration failed !!!");

  }else{
    Serial.println("HCSR04 Ultrasonic Distance Sensor has been Configured");
  }
  
  return ret;
}

/*
 * Calculates and returns the distance by the duration
 */
double getDistanceByDuration(double duration){
  return duration * 0.034 / 2.0;
}

/*
 * Measure and returns the latency of the returned signal
 * 
 * return: 0 - sensor is not connected
 * 
 */
double getDuration(bool needToPrint){
  double ret = 0.0;  

  // Clears the trigPin
  digitalWrite(sensorDistanceTrigGPIO, LOW);
  delayMicroseconds(2);
  // Sets the sensorDistanceTrigGPIO on HIGH state for 10 micro seconds
  digitalWrite(sensorDistanceTrigGPIO, HIGH);
  delayMicroseconds(10);
  digitalWrite(sensorDistanceTrigGPIO, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  ret = pulseIn(sensorDistanceEchoGPIO, HIGH);

  if(needToPrint){
    Serial.print("Duration: ");
    Serial.println(ret);
  }

  return ret;
}

/*
 * Returns the calculated the distance of the measured average latency
 * 
 * return:  NULL - missing sensor
 * 
 */
double getSampleOfDistance(int sample){
  double ret;
  double sumDur = 0;
  double incDur = 0;
  double actualDur;
  double avgDur;
  double result;

  for(int i = 0; i < sample; i++){
    actualDur = getDuration(false);
    sumDur += actualDur;
    incDur++;
  }

  if(incDur > 0){
    avgDur = sumDur / incDur;
    
    if(avgDur > 0.0){
      ret = getDistanceByDuration(avgDur);
    }else{
      ret = NULL;
    }
  }else{
    ret = NULL;
  }
  return ret;
}

/********************************************************
*
* Dinamically calculate average (moving average) distance
* The calculated average distance is stored in the avgHcsrdist 
* variable.
* When you call this function, it will take a new distance 
* measurement and calculates new average value including
* this new value.
* 
* Calculation of moving average:
*    N = 0
*    avg = 0
*    
*    For each new value: V
*        N=N+1
*        a = 1/N
*        b = 1 - a
*        avg = a * V + b * avg
*        
*********************************************************/
double add1SampleToMovingAverageDistance(bool reset){

  if(reset){
    avgHcsrDist = NULL;
    avgHcsrCounter = 0;
  }

  double actualDist = getSampleOfDistance(1); 
  
  // If there was evaluable result and there was already an evaluable result before
  if(actualDist != NULL && avgHcsrDist != NULL){
    avgHcsrCounter++;
    double a = 1/avgHcsrCounter;
    double b = 1 - a;
    avgHcsrDist = a * actualDist + b * avgHcsrDist;
  
  // If this result or the previous result was NULL => NO sensor
  // The recent measurement in evaluable, but before there was not
  }else if(actualDist != NULL){
    avgHcsrCounter = 1;
    avgHcsrDist = actualDist;

  // If the recent measurement was not evaluable
  }else{
    avgHcsrCounter = 0;
    avgHcsrDist = NULL;
  }

  return avgHcsrDist;
}
