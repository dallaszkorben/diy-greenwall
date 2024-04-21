#include <DHT.h>;

//#define DHTTYPE    DHT11     // DHT 11
#define DHTTYPE    DHT22     // DHT 22 (AM2302)

DHT dht(sensorTempHumOutGPIO, DHTTYPE);

bool configureTempHumSensor(){

  bool ret = true;

  dht.begin();
  double h = dht.readHumidity();
  double t = dht.readTemperature();
  
  if(isnan(h) || isnan(t)){
    Serial.println();
    Serial.println("!!! dht.begin() failed. check your DHT Interface !!!");
    ret = false;
  }else{
    Serial.println("   DHT Temerature & Humidity Sensor has been Configured");
  }
  
  return ret;
}


struct DHT_Struct getTempHum(bool needToPrint){
  struct DHT_Struct ret;
  ret.temperature = NULL;
  ret.humidity = NULL;

  double h = dht.readHumidity();
  double t = dht.readTemperature();
  
  if(!isnan(h)){
    ret.humidity = h;
  }
  if(!isnan(t)){
    ret.temperature = t;
  }

  if(needToPrint){
    Serial.print("Temperature: "); 
    Serial.print(ret.temperature); 
    Serial.println(" degC");
  }
  if(needToPrint){
    Serial.print("Humidity: "); 
    Serial.print(ret.humidity); 
    Serial.println(" %");
  }
  
  return ret;
}

/*
 * Returns the average value of the Temperature/Humidity
 * 
 * return:  
 *    .temp=NULL      - missing sensor
 *    .humidity=NULL  - missing sensor
  * 
 */
struct DHT_Struct getSampleOfTempHum(int sample){
  struct DHT_Struct ret;
  double sumTemp = 0;
  double sumHum = 0;
  double incTemp = 0;
  double incHum = 0;
  double actualTemp;
  double actualHum;

  struct DHT_Struct result;

  for(int i = 0; i < sample; i++){
    result = getTempHum(false);
    actualTemp = result.temperature;
    actualHum = result.humidity;

    if(actualTemp != NULL){
      sumTemp += actualTemp;
      incTemp++;
    }
    if(actualHum != NULL){
      sumHum += actualHum;
      incHum++;
    }
  }

  if(incTemp > 0){
    ret.temperature = sumTemp/incTemp;
  }else{
    ret.temperature = NULL;
  }

  if(incHum >0){
    ret.humidity = sumHum/incHum;
  }else{
    ret.humidity = NULL;
  }
  
  return ret;
}

/********************************************************
*
* Dinamically calculate average (moving average) Temperature/Humidity
* The calculated average Temp/Hum are stored in the avgDhtTemp/avgDhtHum 
* variable.
* When you call this function, it will take a new Temp/Hum
* measurement and calculates new average value including
* this new value.
* 
* Calculation of moving average:
* 
*     N = 0
*     avg = 0
*    
*     For each new value: V
*        N=N+1
*        a = 1/N
*        b = 1 - a
*        avg = a * V + b * avg
*        
*********************************************************/
struct DHT_Struct add1SampleToMovingAverageTempHum(bool reset){
  struct DHT_Struct ret;
  double actualTemp;
  double actualHum;

  if(reset){
    avgDhtTemp = NULL;
    avgDhtHum = NULL;
    avgDhtTempCounter = 0;
    avgDhtHumCounter = 0;
  }

  struct DHT_Struct result;
  result = getSampleOfTempHum(1);
 
  actualTemp = result.temperature;
  actualHum = result.humidity;

  // ---

  if(actualTemp != NULL && avgDhtTemp != NULL){
    avgDhtTempCounter++;
    double a = 1/avgDhtTempCounter;
    double b = 1 - a;
    avgDhtTemp = a * actualTemp + b * avgDhtTemp;
  }else if(actualTemp != NULL){
    avgDhtTempCounter = 1;
    avgDhtTemp = actualTemp;
  // If the recent measurement was not evaluable
//  }else{
//    avgDhtTempCounter = 0;
//    avgDhtTemp = NULL;
  }

  // ---

  if(actualHum != NULL && avgDhtHum != NULL){
    avgDhtHumCounter++;
    double a = 1/avgDhtHumCounter;
    double b = 1 - a;
    avgDhtHum = a * actualHum + b * avgDhtHum;
  }else if(actualHum != NULL){
    avgDhtHumCounter = 1;
    avgDhtHum = actualHum;
  // If the recent measurement was not evaluable
//  }else{
//    avgDhtHumCounter = 0;
//    avgDhtHum = NULL;
  }

  // ---

  ret.temperature = avgDhtTemp;
  ret.humidity = avgDhtHum;

  return ret; 
}
