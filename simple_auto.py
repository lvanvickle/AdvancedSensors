from autonomous import start_autonomy, setup_serial
from motor_func import stop_motors

def get_mode():
    return "autonomous"

def main():
    setup_serial()
    start_autonomy(get_mode)

try:
    main()
except KeyboardInterrupt:
    print("Interrupted")
    stop_motors()
    
