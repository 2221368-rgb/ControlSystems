#include <Servo.h>
const int servoPin = 9;
Servo myServo;

void setup() {
  Serial.begin(9600);
  myServo.attach(servoPin);
  myServo.write(90); // Safe Initial State
  Serial.println("Arduino ready. Servo initialised to 90 degrees.");
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    
    if (data.length() == 0) {
      Serial.println("ERR: Empty input received");
      return;
    }

    bool isValid = true;
    for (byte i = 0; i < data.length(); i++) {
      if (!isDigit(data[i])) { isValid = false; break; }
    }

    if (!isValid) {
      Serial.println("ERR: Invalid input, not a number");
    } else {
      int angle = data.toInt();
      if (angle >= 0 && angle <= 180) {
        myServo.write(angle);
        Serial.print("ACK:"); Serial.println(angle);
      } else {
        Serial.println("ERR: Angle out of range (0-180)");
      }
    }
  }
}
