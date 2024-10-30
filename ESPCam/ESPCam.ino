#include "esp_camera.h"  // Include the ESP32 camera library to control the camera
#include <WiFi.h>        // Include the WiFi library to connect to WiFi

// Replace with your network credentials
const char* ssid = "YOUR_WIFI_SSID";        // WiFi SSID (name)
const char* password = "YOUR_WIFI_PASSWORD"; // WiFi password

// Forward declaration for the function that starts the camera server
void startCameraServer();

// Select the camera model being used
#define CAMERA_MODEL_AI_THINKER  // Define the specific ESP32 camera module (AI-Thinker model)

#include "camera_pins.h"  // Include the pin definitions for the AI-Thinker model

void setup() {
   // Start the serial monitor for debugging output
   Serial.begin(115200);          // Set serial monitor speed to 115200 baud
   Serial.setDebugOutput(true);   // Enable debugging output
   Serial.println();              // Newline for clear output formatting

   // Connect to the WiFi network
   WiFi.begin(ssid, password);    // Begin WiFi connection with provided SSID and password
   while (WiFi.status() != WL_CONNECTED) {  // Loop until the WiFi is connected
     delay(500);                  // Delay for half a second between connection attempts
     Serial.print(".");           // Print dots as it connects to give feedback
   }
   Serial.println("");
   Serial.println("WiFi connected"); // Print message once connected

   startCameraServer();  // Start the camera server to enable streaming

   // Print the IP address for accessing the camera feed
   Serial.print("Camera Ready! Use 'http://");
   Serial.print(WiFi.localIP());  // Display the device's IP address
   Serial.println("' to connect"); // URL to access the camera feed
}

void loop() {
   delay(10000); // Loop delay (10 seconds), no ongoing action required here
}
