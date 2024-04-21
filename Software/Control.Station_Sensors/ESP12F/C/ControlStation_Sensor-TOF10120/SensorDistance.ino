
unsigned short lenth_val = 0;
unsigned char i2c_rx_buf[16];
unsigned char dirsend_flag=0;

double getAvgTemp();

bool configureDistanceSensor(){

  bool ret = true;

  Serial.println("    ToF10120 sensor configuration failed !!!");
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
  double sumDist = 0;
  double incDist = 0;
  double actualDist;
  double avgDist;
  double result;

  for(int i = 0; i < sample; i++){
    actualDist = ReadDistance();

    sumDist += actualDist;
    incDist++;
  }

  if(incDist > 0 && sumDist > 0){
    avgDist = (sumDist / incDist);
    
    if(avgDist > 0.0){
      ret = (100-avgDist)/10;      
    }else{
      ret = NULL;
    }
  }else{
    ret = NULL;
  }

  if(ret < 0.0){
    ret = 0.0;
  }

  //Serial.println(ret);
  
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
  //Temporarily 5 sample was taken instead of 1  
  double actualDist = getSampleOfDistance(5); 
  
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
  }

  return avgHcsrDist;
}

void DistanceSensorRead(unsigned char addr,unsigned char* datbuf,unsigned char cnt){
  unsigned short result=0;
  // step 1: instruct sensor to read echoes
  Wire.beginTransmission(82); // transmit to device #82 (0x52), you can also find this address using the i2c_scanner code, which is available on electroniclinic.com
  // the address specified in the datasheet is 164 (0xa4)
  // but i2c adressing uses the high 7 bits so it's 82
  Wire.write(byte(addr));      // sets distance data address (addr)
  Wire.endTransmission();      // stop transmitting
  // step 2: wait for readings to happen
  delay(1);                   // datasheet suggests at least 30uS
  // step 3: request reading from sensor
  Wire.requestFrom(82, cnt);    // request cnt bytes from slave device #82 (0x52)
  // step 5: receive reading from sensor
  if (cnt <= Wire.available()) { // if two bytes were received
    *datbuf++ = Wire.read();  // receive high byte (overwrites previous reading)
    *datbuf++ = Wire.read(); // receive low byte as lower 8 bits
  }
}
 
int ReadDistance(){
    DistanceSensorRead(0x00,i2c_rx_buf,2);
    lenth_val=i2c_rx_buf[0];
    lenth_val=lenth_val<<8;
    lenth_val|=i2c_rx_buf[1];
    delay(100); 
    return lenth_val;
}
