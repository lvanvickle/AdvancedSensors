#include <Servo.h>

// Initialize pins for trigger, echo, and servo
int trigPin = 9;
int echoPin = 10;
int servoPin = 3;

 // Create an instance of Servo class
Servo servo;

// Create a threshold at which rover should stop and turn (cm)
int thresholdDistance = 35;

void setup() {
  Serial.begin(9600); // Begin serial connection
  servo.attach(servoPin); // Attach servo object to pin
  pinMode(trigPin, OUTPUT); // Set trig pin to output
  pinMode(echoPin, INPUT); // Set echo pin to input
}

void loop() {
  int distance = measureDistance(); // Measure clearance in front of rover

  if (distance < thresholdDistance) {
    // Obstacle detected!
    // Begin scanning to find a clear path
    int bestAngle = scanForClearPath();
    // Send angle to Raspberry Pi
    Serial.println(bestAngle);
  } else {
    // No obstacle detected; send a "clear" signal to the Raspberry Pi
    Serial.println("clear");
  }

  delay(1000);
}

// Function to measure distance with ultrasonic sensor
int measureDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  int distance = duration * 0.034 / 2;
  return distance;
}

// Function to scan at multiple angles and find clear path
int scanForClearPath() {
  int angles[] = {-90, 0, 90};

  for (int i = 0; i < 3; i++) {
    servo.write(angles[i] + 90);  // Offset by 90 since servo operates 0-180
    delay(500);                     // Wait for servo to reach position

    int distance = measureDistance();
    if (distance > thresholdDistance) {
      return angles[i]; // Stop scanning once clear path is found
    }
  }

  return 0; // If no clear path is found, return 0
}
