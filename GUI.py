import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime


# Read the current number from Current_Session_File
def readCurrentSession():
    global current_Session
    if os.path.exists(Current_Session_File):
        with open(Current_Session_File, "r") as file:
            try:
                current_Session = int(file.read().strip())
            except ValueError:
                current_Session = 0
    else:
        current_Session = 0


# Save the updated number back to FolderName


def IncrementSession():
    global current_Session  # Declare as global to modify the global variable
    readCurrentSession()
    current_Session = current_Session + 1
    with open(Current_Session_File, "w") as file:
        file.write(str(current_Session))


def makeCSV():
    # Initialize CSV file with headers if it doesn't exist
    program_timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )  # Replace invalid characters
    global csv_file
    csv_file = f"./Participants_Actions/log_{program_timestamp}.csv"
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


# Function to log actions
def log_action(success, failure):
    global ai_initiates, user_initiates, current_Session
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [timestamp, current_Session, ai_initiates, user_initiates, success, failure]
        )
    Condition = get_condition()
    update_status(
        f"""Logged \nSession={current_Session} \n\nCondition={Condition}
        \nSuccess={success}, Failure={failure}"""
    )


# Function to update the status label
def update_status(message):
    status_label.config(text=message)


# GUI setup
root = tk.Tk()
root.title("Initiation User Logger")

status_label = tk.Label(
    root, text="Press a button to log an action.", wraplength=400, width=50
)
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

    if Condition == "AI initiates":
        with open("initiate_conversation", "w") as file:
            file.write(str(1))

    update_status(
        f"""New User \nSession={current_Session} \n\nCondition={Condition}
        \n..."""
    )


def stop_recording_action():
    # set recording to false
    print("Stopping recording...")
    with open("recording_audio", "w") as file:
        file.write(str(0))


# Buttons
user_enters_zone = tk.Button(
    root,
    text="New User",
    command=user_enters_zone_action,
    bg="lightgreen",
)
user_enters_zone.pack(pady=10)

stop_recording = tk.Button(
    root,
    text="Stop recording",
    command=stop_recording_action,
    bg="lightgreen",
)
stop_recording.pack(pady=10)


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


ai_initiates = False
user_initiates = False
current_Session = 0
Current_Session_File = "Current_Session"
Current_Condition_File = "Current_Condition"

readCurrentSession()
makeCSV()
user_enters_zone_action()
# Start GUI loop
root.mainloop()
