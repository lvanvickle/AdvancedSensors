#include <Servo.h>

// Define pins for ultrasonic sensor and servo
int trigPin = 9;
int echoPin = 10;
int servoPin = 6;

Servo sensorServo;
const double SPEED_OF_SOUND = 0.034;

long distance = 0;  // Holds the current distance reading
bool facingFront = true;  // Track whether the sensor is facing forward

void setup() {
  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  sensorServo.attach(servoPin);
  rotateServoFront();  // Start with the sensor facing forward
}

void loop() {
  // Get distance from the current direction
  distance = getDistance();

  // If sensor is facing forward and obstacle is detected
  if (facingFront && distance < 20) {
    rotateServoBack();  // Turn to face the back
    delay(500);  // Allow time for the servo to rotate
    distance = getDistance();  // Get the distance from the back
    Serial.print(0);  // Send 0 for back
  } else if (!facingFront) {
    rotateServoFront();  // Turn to face the front again
    delay(500);  // Allow time for the servo to rotate
    distance = getDistance();  // Get the distance from the front
    Serial.print(1);  // Send 1 for front
  }

  // Send boolean (1 or 0) along with distance
  Serial.print(",");
  Serial.println(distance);
  delay(500);  // Adjust delay as needed
}

// Function to get distance using the ultrasonic sensor
long getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  long distance = duration * SPEED_OF_SOUND / 2;
  
  return distance;
}

// Rotate the servo to face forward
void rotateServoFront() {
  sensorServo.write(0);  // Adjust for your setup
  facingFront = true;
}

// Rotate the servo to face backward
void rotateServoBack() {
  sensorServo.write(255);  // Adjust for your setup
  facingFront = false;
}
