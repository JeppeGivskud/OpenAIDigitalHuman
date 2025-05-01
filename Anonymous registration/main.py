import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

# Initialize CSV file with headers if it doesn't exist
program_timestamp = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S"
)  # Replace invalid characters
csv_file = f"actions_log_{program_timestamp}.csv"
with open(csv_file, mode="a", newline="") as file:
    writer = csv.writer(file)
    if file.tell() == 0:  # Check if file is empty
        writer.writerow(
            ["Timestamp", "AI Initiates", "User Initiates", "Success", "Failure"]
        )


# Function to log actions
def log_action(ai_initiates, user_initiates, success, failure):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, ai_initiates, user_initiates, success, failure])
    update_status(
        f"Logged: AI={ai_initiates}, User={user_initiates}, Success={success}, Failure={failure}"
    )


# Function to update the status label
def update_status(message):
    status_label.config(text=message)


# GUI setup
root = tk.Tk()
root.title("Initiation User Logger")

status_label = tk.Label(root, text="Press a button to log an action.", wraplength=400)
status_label.pack(pady=10)


# Button actions
def ai_initiates_action_success():
    log_action(1, 0, 1, 0)


def ai_initiates_action_failure():
    log_action(1, 0, 0, 1)


def user_initiates_action_success():
    log_action(0, 1, 1, 0)


def user_initiates_action_failure():
    log_action(0, 1, 0, 1)


# Buttons
ai_button = tk.Button(
    root,
    text="AI Initiates - Success",
    command=ai_initiates_action_success,
    bg="lightgreen",
)
ai_button.pack(pady=10)

success_button = tk.Button(
    root,
    text="AI Initiates - Failure",
    command=ai_initiates_action_failure,
    bg="lightgreen",
)
success_button.pack(pady=10)

failure_button = tk.Button(
    root,
    text="User Initiates - Success",
    command=user_initiates_action_success,
    bg="lightblue",
)
failure_button.pack(pady=10)

user_button = tk.Button(
    root,
    text="User Initiates - Failure",
    command=user_initiates_action_failure,
    bg="lightblue",
)
user_button.pack(pady=10)

# Start GUI loop
root.mainloop()
