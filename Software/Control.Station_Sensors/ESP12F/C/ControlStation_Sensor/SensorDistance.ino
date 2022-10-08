

bool configureDistanceSensor(){

  bool ret = true;

  pinMode(sensorDistanceTrigGPIO, OUTPUT); // Sets the trigPin as an Output
  pinMode(sensorDistanceEchoGPIO, INPUT);  // Sets the echoPin as an Input

  double dist = getAverageDistance(10);

  if(dist == NULL){
    ret = false;  

    Serial.println("!!! HCSR04 sensor configuration failed !!!");

  }else{
    Serial.println("HCSR04 Ultrasonic Distance Sensor has been Configured");
  }
  
  return ret;
}

double getDistanceByDuration(double duration){
  return duration * 0.034 / 2.0;
}

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

double getAverageDistance(int sample){
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

double avgHcsrDist = NULL;
//double avgHcsrCounter = 0;
/////////////////////////////////////////////////
//
// Dinamically calculate average (moving average)
//
//    N = 0
//    avg = 0
//    
//    For each new value: V
//        N=N+1
//        a = 1/N
//        b = 1 - a
//        avg = a * V + b * avg
/////////////////////////////////////////////////
double getMovingAverageDistance(bool reset){
  double ret;
  double actualDist;

  if(reset){
    avgHcsrDist = NULL;
    avgHcsrCounter = 0;
  }

  double result;
  result = getAverageDistance(1); 
  actualDist = result;

  avgHcsrCounter++;
  double a = 1/avgHcsrCounter;
  double b = 1 - a;
  if(avgHcsrDist == NULL){
    avgHcsrDist = actualDist;
  }else if(actualDist != NULL){
    avgHcsrDist = a * actualDist + b * avgHcsrDist;
  }

  ret = avgHcsrDist;

  return ret; 
}
