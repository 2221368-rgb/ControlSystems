// Python and Arduino Activity
// Control LED using Serial Monitor

const int ledPin = 13;  // Built-in LED (or use any digital pin)

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == '1') {
      digitalWrite(ledPin, HIGH);   // LED ON
    }
    else if (command == '0') {
      digitalWrite(ledPin, LOW);    // LED OFF
    }
  }
}
