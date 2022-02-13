/*
  ESP8266 Blink by Simon Peter
  Blink the blue LED on the ESP-01 module
  This example code is in the public domain

  The blue LED on the ESP-01 module is connected to GPIO1
  (which is also the TXD pin; so we cannot use Serial.print() at the same time)

  Note that this sketch uses LED_BUILTIN to find the pin with the internal LED
*/

int LAMP_PIN_GPIO = 5;

void setup() {
  Serial.begin(115200);
  Serial.println("Initialize");
  pinMode(LAMP_PIN_GPIO, OUTPUT);     // Initialize the LED_BUILTIN pin as an output  
}

// the loop function runs over and over again forever
void loop() {
  Serial.println("High");
  digitalWrite(LAMP_PIN_GPIO, HIGH);  // Turn the LED on
  delay(2000);                        // Wait for two seconds (to demonstrate the active LED)
  Serial.println("Low");
  digitalWrite(LAMP_PIN_GPIO, LOW);   // Turn the LED off
  delay(1000);                        // Wait for a second
}
