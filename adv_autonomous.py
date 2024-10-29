from motor_func import move_forward, stop_motors, turn_left, turn_right  # Import motor functions to control the rover's movements
import time  # Import time to control delays
import serial  # Import serial for communication between Raspberry Pi and Arduino

ser = None  # Initialize the serial connection as None for now

# Setup serial communication with the Arduino
def setup_serial():
    global ser  # Declare ser as a global variable so it can be used in this function and elsewhere
    try:
        # Establish serial connection on specified port with baud rate of 9600
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        print("Connected to Arduino for Line Following")
    except serial.SerialException as e:
        # Print error message if serial connection fails
        print(f"Error: {e}")

# Function to read direction data from Arduino
def read_direction():
    # Check if data is available in the serial buffer
    if ser.in_waiting > 0:
        # Read one line from serial, decode it, and strip whitespace/newlines
        data = ser.readline().decode().strip()
        return data  # Return the decoded data
    return None  # Return None if no data is available

# Main function to control the rover
def main():
    setup_serial()  # Initialize serial communication with Arduino

    while True:
        direction = read_direction()  # Read direction data from Arduino

        if direction == "clear":
            # Move forward if the path is clear
            move_forward(0.8)
        elif direction is not None:
            try:
                # Attempt to convert direction data to an integer (angle)
                angle = int(direction)
                stop_motors()  # Stop the rover before making a turn
                if angle < 0:
                    # Turn left if the angle is negative
                    turn_left(0.5)
                elif angle > 0:
                    # Turn right if the angle is positive
                    turn_right(0.5)
            except ValueError:
                # Ignore any data that isn't an integer
                pass

# Run main function when script is executed
if __name__ == "__main__":
    main()
