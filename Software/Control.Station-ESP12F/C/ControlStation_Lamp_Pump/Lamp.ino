float MAX_PERC = 100.0;
float MAX_DUTY = 1024;
float STEP_SEC = 0.02;

double getPowByPerc(double perc){
  return 0.000199713376287*pow(min(100.0, max(0.0, perc)), 3.354734239970603); 
}

void turnLampOn(int lengthInSec){
  double steps = lengthInSec / STEP_SEC;
  double dutyStep = MAX_PERC / steps;

  double dutyCycle = 0;
  while(dutyCycle <= (MAX_PERC + dutyStep) ){

    int pwmValue = int(getPowByPerc(dutyCycle));
   
    //Serial.print("LED duty: ");
    //Serial.print(dutyCycle);
    //Serial.print("% => ");
    //Serial.println(pwmValue);
    
    analogWrite(lamp_gpio, pwmValue);

    delay(long(STEP_SEC * 1000));
    dutyCycle += dutyStep;
  }
  return;
}

void turnLampOff(int lengthInSec){
  double steps = lengthInSec / STEP_SEC;
  double dutyStep = MAX_PERC / steps;

  double dutyCycle = MAX_PERC;
  while(dutyCycle >= -dutyStep){

    int pwmValue = int(getPowByPerc(dutyCycle));
    
    //Serial.print("LED duty: ");
    //Serial.print(dutyCycle);
    //Serial.print("% => ");
    //Serial.println(pwmValue);

    analogWrite(lamp_gpio, pwmValue);

    delay(long(STEP_SEC * 1000));
    dutyCycle -= dutyStep;
  }
  return;
}
