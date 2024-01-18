#include <SoftwareSerial.h>

// Define the RX and TX pins for the HC-05 module
int hc05_rx = 0;  // Connect HC-05 TX to Arduino pin 2
int hc05_tx = 1;  // Connect HC-05 RX to Arduino pin 3
int touch_pin=7;
SoftwareSerial hc05(hc05_rx, hc05_tx);  // Create a SoftwareSerial object

void setup() {
  Serial.begin(9600);     // Serial monitor for debugging
  hc05.begin(9600);
  pinMode(touch_pin,INPUT_PULLUP);     // HC-05 baud rate (make sure it matches the module's configuration)
}

void loop() {
  if (hc05.available()) {
    char receivedChar = hc05.read();  // Read the incoming character from HC-05

    // Print the received character to the Arduino's serial monitor
    Serial.print(receivedChar); 
    

    // You can add your custom code here to process the received data
  }
}
