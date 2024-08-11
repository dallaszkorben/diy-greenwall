#include <Ticker.h>

Ticker blinker1;
Ticker blinker2;

float pulse = 0.1;

void setPinLow() {
  digitalWrite(LED_BUILTIN, 0);
}

void setPinHigh() {
  digitalWrite(LED_BUILTIN, 1);
}

void signalChange(){
  setPinHigh();
  blinker2.detach();
}

void signalStart(){
  setPinLow();
  blinker2.attach(pulse, signalChange);
}

//=== 

// Blinking with Short High
void ledSignalHealthy(){
  ledStatus = LED_HEALTHY;
  pulse = 0.05;
  blinker1.detach();
  blinker2.detach();
  blinker1.attach(1, signalStart);   
}

// 
void ledSignalNetworkError(){
  ledStatus = LED_ERROR;
  pulse = 0.25;
  blinker1.detach();
  blinker2.detach();
  blinker1.attach(0.5, signalStart);
}

// Pale
void ledSignalInitiate(){
  ledStatus = LED_INITIATE;
  pulse = 0.001;
  blinker1.detach();
  blinker2.detach();
  blinker1.attach(0.008, signalStart);
}

void ledSignalCommunicate(){
  ledStatus = LED_COMMUNICATE;
  pulse = 0.05;
  blinker1.detach();
  blinker2.detach();
  blinker1.attach(0.1, signalStart);
}
