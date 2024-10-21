int irSensorPin = A0;  // Pin for IR sensor

void setup() {
  Serial.begin(9600);  // Start serial communication
  pinMode(irSensorPin, INPUT);  // Set IR sensor pin as input
}

void loop() {
  int sensorValue = analogRead(irSensorPin);  // Read the IR sensor

  // If the sensorValue is low, it sees the line
  if (sensorValue < 500) {  
    Serial.println(1);  // Send 1 if the sensor detects the line
  } else {
    Serial.println(0);  // Send 0 if no line is detected
  }

  delay(100);  // Small delay for readability
}