import threading
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, SUCCESS, DANGER

from motor_func import move_forward, move_backward, turn_left, turn_right, stop_motors
from autonomous import start_autonomy, setup_serial
from line_follow import start_line_follow  # Import line following logic

# Global variables
speed = 1.0  # Default speed
mode = "manual"  # Start in manual mode
autonomous_thread = None  # Placeholder for autonomous thread
line_follow_thread = None  # Placeholder for line following thread

# Function to toggle between fast and slow
def toggle_speed():
    global speed
    if speed == 1.0:
        speed = 0.5  # Slow mode
        speed_button.config(text="Fast Mode: Off")
    else:
        speed = 1.0  # Fast mode
        speed_button.config(text="Fast Mode: On")
    print(f"Speed set to {'Slow' if speed == 0.5 else 'Fast'}.")

# Function to toggle between manual, autonomous, and line-following modes
def toggle_mode():
    global mode, autonomous_thread, line_follow_thread
    
    if mode == "manual":
        mode = "autonomous"
        mode_button.config(text="Mode: Autonomous")
        # Start autonomous mode in a separate thread
        autonomous_thread = threading.Thread(target=start_autonomy, args=(get_mode,))
        autonomous_thread.start()
        
    elif mode == "autonomous":
        mode = "line_follow"
        mode_button.config(text="Mode: Line Following")
        # Stop autonomous mode
        stop_motors()  # Stop motors before switching
        if autonomous_thread is not None:
            autonomous_thread.join()  # Ensure autonomous thread is stopped
        # Start line following in a separate thread
        line_follow_thread = threading.Thread(target=start_line_follow, args=(get_mode,))
        line_follow_thread.start()
        
    elif mode == "line_follow":
        mode = "manual"
        mode_button.config(text="Mode: Manual")
        # Stop line-following mode
        stop_motors()  # Ensure the motors stop when switching to manual
        if line_follow_thread is not None:
            line_follow_thread.join()  # Ensure line-follow thread is stopped
        print("Switching to Manual Mode.")

# Function to return the current mode
def get_mode():
    return mode

# Call each movement direction based on button pressed
def forward_press(event):
    move_forward(speed)

def backward_press(event):
    move_backward(speed)

def left_press(event):
    turn_left(speed)

def right_press(event):
    turn_right(speed)

def stop_release(event):
    stop_motors()

# Set up the GUI
root = ttk.Window(themename="darkly")
root.title("Rover Control")

# Create the buttons for movement
forward_button = ttk.Button(root, text="Forward", width=10)
backward_button = ttk.Button(root, text="Backward", width=10)
left_button = ttk.Button(root, text="Left", width=10)
right_button = ttk.Button(root, text="Right", width=10)
stop_button = ttk.Button(root, text="Stop", width=10, command=stop_motors)
speed_button = ttk.Button(root, text="Fast Mode: On", width=15, command=toggle_speed)
mode_button = ttk.Button(root, text="Mode: Manual", width=20, command=toggle_mode)

# Bind the buttons to their respective functions
forward_button.bind("<ButtonPress-1>", forward_press)
forward_button.bind("<ButtonRelease-1>", stop_release)
backward_button.bind("<ButtonPress-1>", backward_press)
backward_button.bind("<ButtonRelease-1>", stop_release)
left_button.bind("<ButtonPress-1>", left_press)
left_button.bind("<ButtonRelease-1>", stop_release)
right_button.bind("<ButtonPress-1>", right_press)
right_button.bind("<ButtonRelease-1>", stop_release)

# Layout the buttons in the grid
forward_button.grid(row=0, column=1, padx=10, pady=10)
backward_button.grid(row=2, column=1, padx=10, pady=10)
left_button.grid(row=1, column=0, padx=10, pady=10)
right_button.grid(row=1, column=2, padx=10, pady=10)
stop_button.grid(row=1, column=1, padx=10, pady=10)
speed_button.grid(row=3, column=1, padx=10, pady=10)
mode_button.grid(row=4, column=1, padx=10, pady=10)

# Initialize the serial connection for the Arduino
setup_serial()

root.mainloop()
