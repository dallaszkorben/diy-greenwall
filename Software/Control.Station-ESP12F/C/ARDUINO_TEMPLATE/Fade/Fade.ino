int LAMP_PIN_GPIO = 5;           // the PWM pin the LED is attached to
float MAX_PERC = 100.0;
float MAX_DUTY = 1024;
float STEP_SEC = 0.02;

int brightness = 0;    // how bright the LED is
int fadeAmount = 5;    // how many points to fade the LED by

void setup() {
  Serial.begin(115200);
  Serial.println("Initialize");
  pinMode(LAMP_PIN_GPIO, OUTPUT);     // Initialize the LED_BUILTIN pin as an output  
}

double getValue(double perc){
  //return pow(min(100.0, max(0.0, perc)), 1.50493781686); 
  return 0.000199713376287*pow(min(100.0, max(0.0, perc)), 3.354734239970603); 
}

void turnLampOn(int lengthInSec){
  double steps = lengthInSec / STEP_SEC;
  double dutyStep = MAX_PERC / steps;

  double dutyCycle = 0;
  while(dutyCycle <= (MAX_PERC + dutyStep) ){

    int pwmValue = int(getValue(dutyCycle));
    
    //String message = String("LED duty: ") + String(dutyCycle, 2) + String("% => ") + String(pwmValue);
    //int lengthMessage = message.length();
    //Serial.print(message);
    
    Serial.print("LED duty: ");
    Serial.print(dutyCycle);
    Serial.print("% => ");
    Serial.println(pwmValue);
    
    analogWrite(LAMP_PIN_GPIO, pwmValue);

    delay(long(STEP_SEC * 1000));
    dutyCycle += dutyStep;
  }
}

void turnLampOff(int lengthInSec){
  double steps = lengthInSec / STEP_SEC;
  double dutyStep = MAX_PERC / steps;

  double dutyCycle = MAX_PERC;
  while(dutyCycle >= -dutyStep){

    int pwmValue = int(getValue(dutyCycle));
    
    //String message = String("LED duty: ") + String(dutyCycle, 2) + String("% => ") + String(pwmValue);
    //int lengthMessage = message.length();
    //Serial.print(message);
    
    Serial.print("LED duty: ");
    Serial.print(dutyCycle);
    Serial.print("% => ");
    Serial.println(pwmValue);

    analogWrite(LAMP_PIN_GPIO, pwmValue);

    delay(long(STEP_SEC * 1000));
    dutyCycle -= dutyStep;
  }
}

// the loop routine runs over and over again forever:
void loop() {

  turnLampOn(5);
  //delay(1000);

  turnLampOff(5);
  //delay(1000);

  
  // set the brightness of pin 9:
  //analogWrite(led, brightness);

  // change the brightness for next time through the loop:
  //brightness = brightness + fadeAmount;

  // reverse the direction of the fading at the ends of the fade:
  //if (brightness <= 0 || brightness >= 255) {
  //  fadeAmount = -fadeAmount;
  //}
  // wait for 30 milliseconds to see the dimming effect
  
  
  
}
