import os
import subprocess

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
session_dir = os.path.join(script_dir, "../saved_audio/Sessions")
transcription_dir = os.path.join(script_dir, "../Transcription/AudioFiles")

# Loop through all session folders
for session_folder in os.listdir(session_dir):
    session_path = os.path.join(session_dir, session_folder)
    if os.path.isdir(session_path):
        session_number = session_folder

        # Check if the transcription file already exists
        transcription_file = os.path.join(
            transcription_dir, f"session_{session_number}_Merged_Python.txt"
        )
        if not os.path.exists(transcription_file):
            print(
                f"Transcription missing for session {session_number}. Starting transcription..."
            )

            # Call the TranscribeSession.py script with the session number
            subprocess.run(
                [
                    "python",
                    os.path.join(script_dir, "TranscribeSession.py"),
                    session_number,
                ],
                check=True,
            )
        else:
            print(
                f"Transcription already exists for session {session_number}. Skipping..."
            )
