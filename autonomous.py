# Importing necessary modules
import serial  # Provides communication between the Raspberry Pi and Arduino via USB
import random  # Allows us to generate random choices for turning left or right
import time  # Gives us the ability to add delays (pauses) in the code
import sys  # Allows us to safely exit the script

# Importing custom motor functions to control the robot's movement
from motor_func import move_forward, move_backward, turn_left, turn_right, stop_motors

# Initializing the serial connection to None (not connected yet)
ser = None

# This function sets up the serial connection between the Raspberry Pi and Arduino
# The Raspberry Pi will communicate with the Arduino via USB
def setup_serial():
    global ser  # This makes sure we can access the 'ser' variable defined outside the function
    try:
        # Try to connect to Arduino on port /dev/ttyUSB0 with a baud rate of 9600
        # 'timeout=1' means it will wait 1 second for a response before timing out
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        print("Connected to Arduino on /dev/ttyUSB0")
    except serial.SerialException as e:
        # If there's an error in setting up the connection, print the error message
        print(f"Error: {e}")

# This function reads the boolean and distance data sent from the Arduino
# It returns the boolean (1 for front, 0 for back) and the distance value in centimeters
def read_distance():
    # Check if the serial connection is active and if there's any data to read
    if ser and ser.in_waiting > 0:
        try:
            # Read the data from the serial connection, decode it to a string, and remove extra spaces/newlines
            data = ser.readline().decode().strip()
            # Split the comma-separated boolean and distance
            sensor_data = data.split(',')
            is_front = bool(int(sensor_data[0]))  # 1 for front, 0 for back
            distance = float(sensor_data[1])  # Distance in cm
            return is_front, distance  # Return both the boolean and distance as a tuple
        except (ValueError, IndexError):
            # If there is an issue with parsing the data, return None
            return None, None
    return None, None  # Return None if no data is available

# This function handles the robot's autonomous movement behavior
# It will keep moving and reacting to obstacles as long as the mode is set to 'autonomous'
def start_autonomy(get_mode):
    try:
        last_distance = None  # Store the last known distance
        while get_mode() == "autonomous":
            # Read the data from the Arduino (boolean + distance)
            is_front, distance = read_distance()

            # If the sensor is facing forward
            if is_front:
                print(f"Front distance: {distance} cm")

                # If obstacle detected in front, prepare to back up
                if distance < 20:
                    print("Obstacle detected in front. Preparing to back up.")
                    stop_motors()  # Stop and prepare to back up
                    last_distance = distance  # Store the last front distance

            # If the sensor is facing backward
            elif not is_front:
                print(f"Back distance: {distance} cm")

                # If the last distance was less than 20 cm, use the back sensor data to back up
                if last_distance is not None and last_distance < 20:
                    print("Backing up based on back sensor data.")
                    start_time = time.time()
                    while time.time() - start_time < 1:  # Back up for 1 second
                        move_backward(0.5)
                        if distance < 40:  # If obstacle detected behind, stop backing up
                            print(f"Obstacle detected behind at {distance} cm. Stopping backup.")
                            break  # Stop backing up if an obstacle is detected behind
                    stop_motors()
                    last_distance = None  # Reset the last distance

            # If no obstacles detected, move forward
            if last_distance is None:
                move_forward(1)
                time.sleep(0.5)  # Check for obstacles periodically

    except KeyboardInterrupt:
        stop_motors()
        print("Autonomy interrupted")

# Main function that sets up and starts the robot in autonomous mode
def main():
    # Set up the serial connection with the Arduino
    setup_serial()

    # Placeholder for mode control (example function that could be used to switch modes)
    def get_mode():
        return "autonomous"  # Always return "autonomous" mode for this example

    # Start the autonomous behavior
    start_autonomy(get_mode)

# This ensures that the script will run if executed directly but won't run if imported as a module
if __name__ == "__main__":
    main()  # Run the main function if this script is executed directly
