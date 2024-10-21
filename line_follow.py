from motor_func import move_forward, stop_motors, turn_left, turn_right  # Import motor functions to control the rover's movements
import time  # Import time to control delays
import serial  # Import serial for communication between Raspberry Pi and Arduino
import random # Import random to generate random direction

ser = None  # Initialize the serial connection as None for now

# Setup serial communication with the Arduino
def setup_serial():
    global ser  # Declare ser as a global variable so it can be used in this function and elsewhere
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        print("Connected to Arduino for Line Following")
    except serial.SerialException as e:
        print(f"Error: {e}")

# Read IR sensor data from Arduino
def read_ir_sensor():
    if ser and ser.in_waiting > 0:
        try:
            # Read a line from the serial connection, decode it to a string, and strip extra spaces/newlines
            data = ser.readline().decode().strip()
            ir_state = int(data)  # Read either 0 (no line) or 1 (line detected)
            return ir_state
        except ValueError:
            return None
    return None # Return None if no data available

# Line following logic
def start_line_following():
    setup_serial()  # Initialize serial communication with Arduino for IR sensor data
    try:
        while True:  # Infinite loop to keep the line following active
            ir_state = read_ir_sensor()  # Read the current state from the IR sensor (1 or 0)

            if ir_state is None:
                continue  # Skip this iteration if no valid data is received from the sensor

            if ir_state:  # If ir_state is True (non-zero), print that the line is detected
                print("Line detected!")

            # If the sensor detects a line (value of 1)
            if ir_state == 1:  
                start_time = time.time()  # Record the start time
                # Move forward for 1 second
                while time.time() - start_time < 1:  
                    move_forward(0.8)  # Move forward at 80% speed
            else:
                # If no line is detected (ir_state == 0), randomly choose to turn left or right
                if random.choice([True, False]):  # Randomly decide to turn left
                    start_time = time.time()  # Record the start time for the turn
                    # Turn left for 1 second
                    while time.time() - start_time < 1:  
                        turn_left(0.5)  # Turn left at 50% speed
                        # Check if the sensor detects the line while turning
                        if read_ir_sensor():  # If the line is detected during the turn
                            stop_motors()  # Stop the motors
                            break  # Exit the turning loop
                else:
                    # If the random choice was False, turn right
                    start_time = time.time()  # Record the start time for the turn
                    # Turn right for 1 second
                    while time.time() - start_time < 1:  
                        turn_right(0.5)  # Turn right at 50% speed
                        # Check if the sensor detects the line while turning
                        if read_ir_sensor():  # If the line is detected during the turn
                            stop_motors()  # Stop the motors
                            break  # Exit the turning loop

            stop_motors()  # Stop the motors when the loop ends

    except KeyboardInterrupt:  # Handle keyboard interrupt (Ctrl+C)
        stop_motors()  # Ensure the motors stop when the program is interrupted

if __name__ == "__main__":
    start_line_following()