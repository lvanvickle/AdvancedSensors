# Import statement for premade modules
from adafruit_motorkit import MotorKit # Module for motor hat

kit = MotorKit() # Stands for the motor hat on the Raspberry Pi
                 # and allows us to program motor1, motor2, motor3,
                 # and motor4 screwdown terminals

def move_forward(speed):
    kit.motor1.throttle = speed # All motors will go forward with the given speed
    kit.motor2.throttle = speed
    kit.motor3.throttle = speed
    kit.motor4.throttle = speed

def move_backward(speed):
    kit.motor1.throttle = -speed # All motors will go backward with the given speed
    kit.motor2.throttle = -speed
    kit.motor3.throttle = -speed
    kit.motor4.throttle = -speed

def turn_left(speed):
    kit.motor1.throttle = speed # Left motors will go foward at the given speed
    kit.motor2.throttle = 0.25 # Right motors will go forward at 25% speed
    kit.motor3.throttle = speed
    kit.motor4.throttle = 0.25

def turn_right(speed):
    kit.motor1.throttle = 0.25 # Left motors will go forward at 25% speed
    kit.motor2.throttle = speed # Right motors will go forward at the given speed
    kit.motor3.throttle = 0.25
    kit.motor4.throttle = speed

def stop_motors():
    kit.motor1.throttle = 0.0 # Stop all motors
    kit.motor2.throttle = 0.0
    kit.motor3.throttle = 0.0
    kit.motor4.throttle = 0.0