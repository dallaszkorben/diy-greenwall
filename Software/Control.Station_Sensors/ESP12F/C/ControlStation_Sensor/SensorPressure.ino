// BMP180_I2C
//
// connect the BMP180 to the Arduino like this:
// Arduino - BMC180
// 5V ------ VCC
// GND ----- GND
// SDA ----- SDA
// SCL ----- SCL

#include <Arduino.h>
#include <Wire.h>
#include <BMP180I2C.h>

#define I2C_ADDRESS 0x77

//create an BMP180 object using the I2C interface
BMP180I2C bmp180(I2C_ADDRESS);

bool configurePressTempSensor(){
  bool ret = true;

  Wire.begin();

  //begin() initializes the interface, checks the sensor ID and reads the calibration parameters.  
  if (!bmp180.begin()) {
    Serial.println();
    Serial.println("!!! bmp180.begin() failed. check your BMP180 Interface and I2C Address !!!");
    isSensorBmp = false;
    ret = false;

  }else{

    //reset sensor to default parameters.
    bmp180.resetToDefaults();

    //enable ultra high resolution mode for pressure measurements
    bmp180.setSamplingMode(BMP180MI::MODE_UHR);
  
    isSensorBmp = true;
    Serial.println("   BMP Pressure Sensor has been Configured");

  }
  return ret;
}

/*
 * 
 */
struct BMP180_Struct getPressTemp(bool needToPrint){
  struct BMP180_Struct ret;
  ret.temperature = NULL;
  ret.pressure = NULL;

  if(!isSensorBmp){
    return ret;
  }

  //start a temperature measurement
  if (!bmp180.measureTemperature()){
    if(needToPrint){
      Serial.println("!!! could not start temperature measurement, is a measurement already running?");
    }  
  }else{

    //wait for the measurement to finish. proceed as soon as hasValue() returned true. 
    int searchLoop = 0;
    do{
      delay(100);
      searchLoop++;
    } while (!bmp180.hasValue() && searchLoop < 20);

    // Could measure Temperature
    if(searchLoop < 20){
      ret.temperature = bmp180.getTemperature();   

      if(needToPrint){
        Serial.print("Temperature: "); 
        Serial.print(ret.temperature); 
        Serial.println(" degC");
      }
    }
  }
  
  //start a pressure measurement. pressure measurements depend on temperature measurement, you should only start a pressure 
  //measurement immediately after a temperature measurement. 
  if (!bmp180.measurePressure()){
    if(needToPrint){
      Serial.println("could not start perssure measurement, is a measurement already running?");    
    }
  }else{

    //wait for the measurement to finish. proceed as soon as hasValue() returned true. 
    int searchLoop = 0;
    do {
      delay(100);
      searchLoop++;
    } while (!bmp180.hasValue() && searchLoop < 20);

    // Could measure Temperature
    if(searchLoop < 20){
      ret.pressure = bmp180.getPressure();
  
      if(needToPrint){
        Serial.print("Pressure: "); 
        Serial.print(ret.pressure);
        Serial.println(" Pa");
      }
    }
  }
  return ret;  
}

struct BMP180_Struct getSampleOfPressTemp(int sample){
  struct BMP180_Struct ret;
  double sumTemp = 0;
  double sumPress = 0;
  double incTemp = 0;
  double incPress = 0;  
  double actualTemp;
  double actualPress;

  struct BMP180_Struct result;
  
  for(int i = 0; i < sample; i++){
    result = getPressTemp(false);
    actualTemp = result.temperature;
    actualPress = result.pressure;

    if(actualTemp != NULL){
      sumTemp += actualTemp;
      incTemp++;
    }
    if(actualPress != NULL){
      sumPress += actualPress;
      incPress++;
    }
  }

  if(incTemp > 0){
    ret.temperature = sumTemp/incTemp;
  }else{
    ret.temperature = NULL;
  }

  if(incPress > 0){
    ret.pressure = sumPress/incPress;
  }else{
    ret.pressure = NULL;
  }
  
  return ret;
}


/********************************************************
*
* Dinamically calculate average (moving average) Pressure/Temperature
* The calculated average Press/Temp are stored in the avgBmpPress/avgBmpTemp 
* variable.
* When you call this function, it will take a new Press/Temp 
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
struct BMP180_Struct add1SampleToMovingAveragePressTemp(bool reset){
  struct BMP180_Struct ret;
  double actualTemp;
  double actualPress;

  ret.temperature = NULL;
  ret.pressure = NULL;

  if(reset){
    avgBmpTemp = NULL;
    avgBmpPress = NULL;
    avgBmpTempCounter = 0;
    avgBmpPressCounter = 0;
  }

  if (!isSensorBmp){
    return ret;
  }
  
  struct BMP180_Struct result;
  result = getSampleOfPressTemp(1);
 
  actualTemp = result.temperature;
  actualPress = result.pressure;

  // ---

  if(actualTemp != NULL && avgBmpTemp != NULL){
    avgBmpTempCounter++;
    double a = 1/avgBmpTempCounter;
    double b = 1 - a;
    avgBmpTemp = a * actualTemp + b * avgBmpTemp;
  }else if(actualTemp != NULL){
    avgBmpTempCounter = 1;
    avgBmpTemp = actualTemp;
  // If the recent measurement was not evaluable
  }else{
    avgBmpTempCounter = 0;
    avgBmpTemp = NULL;
  }

  // ---

   if(actualPress != NULL && avgBmpPress != NULL){
    avgBmpPressCounter++;
    double a = 1/avgBmpPressCounter;
    double b = 1 - a;
    avgBmpPress = a * actualPress + b * avgBmpPress;
  }else if(actualPress != NULL){
    avgBmpPressCounter = 1;
    avgBmpPress = actualPress;
  // If the recent measurement was not evaluable
  }else{
    avgBmpPressCounter = 0;
    avgBmpPress = NULL;
  }

  // ---

  ret.temperature = avgBmpTemp;
  ret.pressure = avgBmpPress;

  return ret; 
}
