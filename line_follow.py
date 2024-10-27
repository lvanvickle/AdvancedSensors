from motor_func import move_forward, stop_motors, turn_left, turn_right  # Import motor functions to control the rover's movements
import time  # Import time to control delays
import serial  # Import serial for communication between Raspberry Pi and Arduino

ser = None  # Initialize the serial connection as None for now

# Setup serial communication with the Arduino
def setup_serial():
    global ser  # Declare ser as a global variable so it can be used in this function and elsewhere
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        print("Connected to Arduino for Line Following")
    except serial.SerialException as e:
        print(f"Error: {e}")

# Read IR sensor data from Arduino (left, center, right)
def read_ir_sensors():
    if ser and ser.in_waiting > 0:
        try:
            # Read a line from the serial connection, decode it to a string, and strip extra spaces/newlines
            data = ser.readline().decode().strip()
            # Split the data by commas to separate each sensor value
            sensor_values = data.split(',')
            if len(sensor_values) == 3:  # Ensure we have three values
                # Convert each value to an integer (0 or 1)
                left_sensor = int(sensor_values[0])
                center_sensor = int(sensor_values[1])
                right_sensor = int(sensor_values[2])
                return left_sensor, center_sensor, right_sensor
        except ValueError:
            return None, None, None
    return None, None, None  # Return None if no data available or an error occurs

# Line following logic using 3 sensors
def start_line_following():
    setup_serial()  # Initialize serial communication with Arduino for IR sensor data
    try:
        while True:  # Infinite loop to keep the line following active
            left_sensor, center_sensor, right_sensor = read_ir_sensors()  # Read the states of the 3 sensors

            if left_sensor is None or center_sensor is None or right_sensor is None:
                continue  # Skip this iteration if no valid data is received from the sensors

            # Decision logic based on the sensor states
            if center_sensor == 1:
                # Line is centered, move forward
                move_forward(0.8)  # Move forward at 80% speed
            elif left_sensor == 1 and center_sensor == 0:
                # Line is on the left, turn left
                turn_left(0.5)  # Turn left at 50% speed
            elif right_sensor == 1 and center_sensor == 0:
                # Line is on the right, turn right
                turn_right(0.5)  # Turn right at 50% speed
            else:
                # No line detected by any sensor, stop
                stop_motors()

            # Small delay for stability
            time.sleep(0.1)

    except KeyboardInterrupt:  # Handle keyboard interrupt (Ctrl+C)
        stop_motors()  # Ensure the motors stop when the program is interrupted

if __name__ == "__main__":
    start_line_following()
