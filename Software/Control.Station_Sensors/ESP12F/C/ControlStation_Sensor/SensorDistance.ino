//--- define functions ---
double getAvgTemp();

bool configureDistanceSensor(){

  bool ret = true;

  pinMode(sensorDistanceTrigGPIO, OUTPUT); // Sets the trigPin as an Output
  pinMode(sensorDistanceEchoGPIO, INPUT);  // Sets the echoPin as an Input

  double dist = getSampleOfDistance(10);

  if(dist == NULL){
    ret = false;  

    Serial.println("!!! HCSR04 sensor configuration failed !!!");

  }else{
    Serial.println("   HCSR04 Ultrasonic Distance Sensor has been Configured");
  }
  
  return ret;
}

/*
 * Calculates and returns the distance by the duration in mm
 */
double getDistanceByDuration(double duration){
  double ret;

  /* 
   *  Linear solution
   *  dist = x * a + b
   *  
   *    x:  measured duration
   *    a:  temp * 0.0000303 + 0.016565
   *    b:  0
   */
  /*double avgTemp = getAvgTemp(avgDhtTemp,avgBmpTemp);
  if(avgTemp != NULL){
    ret = duration * ( (avgTemp * 0.0000303) + 0.016565 );
  }else{
    ret = duration * 0.017171;
  }*/

  /*
   *  Quadratic solution
   *  dist = a + bx + cx^2
   *  
   *  a,b,c parameters must be calculated by some real distance/duration measurements
   *  
   *  Continously check the duration to collect the correlation between x (duration) and the dist:
   *  
   *  # watch 'curl -s --header "Content-Type: application/json" --request GET http://192.168.50.112:80/duration | grep -oP "duration\":\"\d+[.]\d+"'
   *  
   *  Google online calculators by keywords: Quadratic regression Calculator
   */

  ret = sensorDistanceParA + duration*sensorDistanceParB + duration*duration*sensorDistanceParC;

  //Serial.print("dur=");
  //Serial.print(duration);
  //Serial.print(", A=");
  //Serial.print(sensorDistanceParA);
  //Serial.print(", B="); 
  //Serial.print(sensorDistanceParB);
  //Serial.print(", C="); 
  //Serial.print(sensorDistanceParC);
  //Serial.print(", =="); 
  //Serial.println(ret);

//Temporarily for test reason
ret = duration;
//

  return ret;
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

  if(incDur > 0 && sumDur > 0){
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
double add1SampleToMovingAverageDistance(bool resetBefore){

  if(resetBefore){
    avgHcsrDist = NULL;
    avgHcsrCounter = 0;
  }

  // Take a sample of distance
  double actualDist = getSampleOfDistance(1); 
  
  // If there was evaluable result and there was already an evaluable result before
  if(actualDist != NULL && avgHcsrDist != NULL){
    avgHcsrCounter++;
    double a = 1/avgHcsrCounter;
    double b = 1 - a;
    avgHcsrDist = a * actualDist + b * avgHcsrDist;
  
  // If there was NO measure yet and recent measurement is OK
  }else if(actualDist != NULL){
    avgHcsrCounter = 1;
    avgHcsrDist = actualDist;

  // If the recent measurement was not evaluable
//  }else{
//    avgHcsrCounter = 0;
//    avgHcsrDist = NULL;
  }

  return avgHcsrDist;
}
