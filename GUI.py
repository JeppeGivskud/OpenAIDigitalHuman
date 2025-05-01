import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

current_Session = 0
# Read the current number from FolderName
if os.path.exists("./saved_audio/FolderName"):
    folder_name_path = "./saved_audio/FolderName"
    with open(folder_name_path, "r") as file:
        try:
            current_Session = int(file.read().strip())
        except ValueError:
            current_Session = 0
else:
    current_Session = 0

# Save the updated number back to FolderName


def IncrementSession():
    global current_Session  # Declare as global to modify the global variable
    current_Session = current_Session + 1

    with open(folder_name_path, "w") as file:
        file.write(str(current_Session))


# Initialize CSV file with headers if it doesn't exist
program_timestamp = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S"
)  # Replace invalid characters
csv_file = f"actions_log_{program_timestamp}.csv"
with open(csv_file, mode="a", newline="") as file:
    writer = csv.writer(file)
    if file.tell() == 0:  # Check if file is empty
        writer.writerow(
            [
                "Timestamp",
                "Session",
                "AI Initiates",
                "User Initiates",
                "Success",
                "Failure",
            ]
        )

ai_initiates = False
user_initiates = False


# Function to log actions
def log_action(success, failure):
    global ai_initiates, user_initiates, current_Session
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [timestamp, current_Session, ai_initiates, user_initiates, success, failure]
        )
    update_status(
        f"Logged: AI={ai_initiates}, Session={current_Session}, User={user_initiates}, Success={success}, Failure={failure}"
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
def success():
    log_action(1, 0)


def failure():
    log_action(0, 1)


def get_condition():
    global current_Session, ai_initiates, user_initiates
    if current_Session % 2 == 0:
        ai_initiates = True
        user_initiates = False
        return "AI initiates"
    else:
        ai_initiates = False
        user_initiates = True
        return "User initiates"


def user_enters_zone_action():
    IncrementSession()
    Condition = get_condition()
    update_status(f"Logged: Session={current_Session}, \nCondition={Condition}")


# Buttons
user_enters_zone = tk.Button(
    root,
    text="User present",
    command=user_enters_zone_action,
    bg="lightgreen",
)
user_enters_zone.pack(pady=10)

success_button = tk.Button(
    root,
    text="Success",
    command=success,
    bg="lightgreen",
)
success_button.pack(pady=10)

failure_button = tk.Button(
    root,
    text="Failure",
    command=failure,
    bg="lightgreen",
)
failure_button.pack(pady=10)

# Start GUI loop
root.mainloop()
