// Define the analog pins for each sensor
int leftIRSensor = A0;
int centerIRSensor = A1;
int rightIRSensor = A2;

void setup() {
  // Initialize the sensor pins
  pinMode(leftIRSensor, INPUT);
  pinMode(centerIRSensor, INPUT);
  pinMode(rightIRSensor, INPUT);

  // Start the serial connection with the Raspberry Pi
  Serial.begin(9600);
}

void loop() {
  // Send processed sensor data as 1 or 0 for each sensor
  Serial.print(getSensorData(leftIRSensor));
  Serial.print(",");
  Serial.print(getSensorData(centerIRSensor));
  Serial.print(",");
  Serial.print(getSensorData(rightIRSensor));
  Serial.println();  // End of data set, for easier parsing on the Raspberry Pi

  delay(1000);  // Small delay to stabilize readings
}

// Function to process analog values into binary (1 or 0)
int getSensorData(int sensor) {
  // Read the sensor value
  int sensorValue = analogRead(sensor);

  // Return 1 for low values (line detected), 0 for high values (no line)
  if (sensorValue < 500) {
    return 1;
  } else {
    return 0;
  }
}
