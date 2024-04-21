#include <Ticker.h>

/*
 * blinker.attach(frequ_sec, callback_func) - every frequ_sec seconds call the callback_func function
 * blinker.detach()                         - clear the Ticker
 * 
 */
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
  blinker1.attach(1.5, signalStart);   
}

// 
void ledSignalNetworkError(){
  ledStatus = LED_ERROR;
  pulse = 0.2;
  blinker1.detach();
  blinker2.detach();
  blinker1.attach(0.4, signalStart);
}

// Pale
void ledSignalInitiate(){
  ledStatus = LED_INITIATE;
  pulse = 0.03;
  blinker1.detach();
  blinker2.detach();
  blinker1.attach(0.03, signalStart);
}

void ledSignalCommunicate(){
  ledStatus = LED_COMMUNICATE;
  pulse = 0.02;
  blinker1.detach();
  blinker2.detach();
  blinker1.attach(0.6, signalStart);
}
