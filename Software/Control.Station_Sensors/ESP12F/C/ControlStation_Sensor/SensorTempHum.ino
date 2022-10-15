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
    Serial.println("DHT Temerature & Humidity Sensor has been Configured");
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

//double avgDhtTemp = NULL;
//double avgDhtHum = NULL;
//double avgDhtCounter = 0;
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
struct DHT_Struct add1SampleToMovingAverageTempHum(bool reset){
  struct DHT_Struct ret;
  double actualTemp;
  double actualHum;

  if(reset){
    avgDhtTemp = NULL;
    avgDhtHum = NULL;
    avgDhtCounter = 0;
  }

  struct DHT_Struct result;
  result = getSampleOfTempHum(1);
 
  actualTemp = result.temperature;
  actualHum = result.humidity;

  avgDhtCounter++;
  double a = 1/avgDhtCounter;
  double b = 1 - a;
  if(avgDhtTemp == NULL){
    avgDhtTemp = actualTemp;
  }else if(actualTemp != NULL){
    avgDhtTemp = a * actualTemp + b * avgDhtTemp;
  }
  if(avgDhtHum == NULL){
    avgDhtHum = actualHum;
  }else if(actualHum != NULL){
    avgDhtHum = a * actualHum + b * avgDhtHum;
  }

  ret.temperature = avgDhtTemp;
  ret.humidity = avgDhtHum;

  return ret; 
}
