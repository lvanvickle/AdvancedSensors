# Import statements for premade modules
import time

# Import statements for custom modules
from motor_func import move_forward, turn_left, turn_right, move_backward, stop_motors # Gives motor functionality

def main():
    direction = input("Enter a direction (f, b, l, r, s): ")
    
    if direction == 'f':
        move_forward(.8)
        print("Moving forward...")
        time.sleep(2)
    elif direction == 'b':
        move_backward(.8)
        print("Moving backward...")
        time.sleep(2)
    elif direction == 'l':
        turn_left(.8)
        print("Moving left...")
        time.sleep(2)
    elif direction == 'r':
        turn_right(.8)
        print("Moving right...")
        time.sleep(2)
    elif direction == 's':
        stop_motors()
        print("Stopping motors...")
        time.sleep(2)
    else:
        print("Invalid direction")

try:
    while True:
        main()
except KeyboardInterrupt:
    stop_motors()
    print("Program Interrupted.")