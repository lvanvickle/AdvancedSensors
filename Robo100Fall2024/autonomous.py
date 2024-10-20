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

# This function reads the distance data sent from the Arduino
# It returns the distance values in centimeters (e.g. 45,60)
def read_distances():
    # Check if the serial connection is active and if there's any data to read
    if ser and ser.in_waiting > 0:
        try:
            # Read the data from the serial connection, decode it to a string, and remove extra spaces/newlines
            data = ser.readline().decode().strip()
            # Split the comma-separated values into a list of strings and convert them to floats
            sensor_data = data.split(',')
            front_distance = float(sensor_data[0])  # Front ultrasonic sensor
            back_distance = float(sensor_data[1])   # Back ultrasonic sensor
            # Return both distances as floating-point values
            return front_distance, back_distance
        except (ValueError, IndexError):
            # If there is an issue with parsing the data (e.g., missing or malformed values), return None
            return None, None
    return None, None  # Return None if no data is available

# This function handles the robot's autonomous movement behavior
# It will keep moving and reacting to obstacles as long as the mode is set to 'autonomous'
def start_autonomy(get_mode):
    try:
        # Loop while the robot is in autonomous mode
        while get_mode() == "autonomous":
            # Get the front and back distances from the Arduino
            front_distance, back_distance = read_distances()
    
            # If an obstacle is detected in front (closer than 20 cm), stop and prepare to back up
            if front_distance is not None and front_distance < 20:
                print(f"Obstacle detected at {front_distance} cm. Stopping and backing up.")
                stop_motors()  # Stop all motor activity
    
                # Check if there is enough clearance in the back (at least 40 cm)
                while back_distance is not None and back_distance < 40:
                    print(f"Obstacle behind at {back_distance} cm.")  # Print the obstacle distance behind
                    # Re-check front and back distances to update the values
                    front_distance, back_distance = read_distances()

                # Start backing up once the rear clearance is at least 40 cm
                print("Rear clearance sufficient, starting to back up.")
                start_time = time.time()  # Record the start time for backing up
                while time.time() - start_time < 1:  # Back up for 1 second
                    move_backward(0.5)  # Move backward at 50% speed
                    _, back_distance = read_distances()  # Continuously check back distance
                    # If an obstacle is detected behind (less than 40 cm), stop backing up
                    if back_distance is not None and back_distance < 40:
                        print(f"Obstacle detected behind at {back_distance} cm. Stopping backup.")
                        break  # Stop the backup process
                stop_motors()  # Stop motors after backing up
    
                # After backing up, randomly decide whether to turn left or right
                if random.choice([True, False]):  # Randomly choose True (turn left) or False (turn right)
                    print("Turning left to avoid obstacle.")
                    start_time = time.time()  # Record the start time for turning left
                    while time.time() - start_time < 1:  # Turn left for 1 second
                        turn_left(0.5)  # Turn left at 50% speed
                        # Continuously check the front and back distances while turning
                        front_distance, back_distance = read_distances()
                        # If the front is clear (more than 20 cm), stop turning
                        if front_distance is not None and front_distance > 20:
                            break  # Exit the turning loop
                else:
                    print("Turning right to avoid obstacle.")
                    start_time = time.time()  # Record the start time for turning right
                    while time.time() - start_time < 1:  # Turn right for 1 second
                        turn_right(0.5)  # Turn right at 50% speed
                        # Continuously check the front and back distances while turning
                        front_distance, back_distance = read_distances()
                        # If the front is clear (more than 20 cm), stop turning
                        if front_distance is not None and front_distance > 20:
                            break  # Exit the turning loop
                stop_motors()  # Stop motors after the turn is complete
    
            # If there are no close obstacles, move forward
            elif front_distance is not None:
                print(f"Closest obstacle {front_distance} cm away. Moving forward.")
                move_forward(1)  # Move forward at full speed (100%)
    
                # Move for 0.5 seconds, continuously checking for obstacles
                start_time = time.time()
                while time.time() - start_time < 0.5:  # Move for 0.5 seconds
                    front_distance, _ = read_distances()  # Check if there's a new obstacle in the front
                    # If an obstacle is detected (less than 20 cm), stop moving forward
                    if front_distance is not None and front_distance < 20:
                        break  # Exit the forward movement loop
                stop_motors()  # Stop the motors after moving forward for 0.5 seconds

    # If a keyboard interrupt (Ctrl + C) is detected, stop the motors and exit safely
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