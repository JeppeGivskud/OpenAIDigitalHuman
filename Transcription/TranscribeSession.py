import os
import sys
import shutil
import subprocess
from pathlib import Path

# Check if a session number is provided
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <session_number>")
    sys.exit(1)

# Get the session number from the command-line argument
session_number = sys.argv[1]

# Get the directory of the script
script_dir = Path(__file__).resolve().parent

# Define paths relative to the script's location
session_path = script_dir / "../saved_audio/Sessions" / session_number
audio_dir = script_dir / f"../Transcription/AudioFiles/session_{session_number}"
merged_file = (
    script_dir / f"../Transcription/AudioFiles/session_{session_number}_Merged.txt"
)

# Ensure the output and temporary directories exist
audio_dir.mkdir(parents=True, exist_ok=True)

# Copy all .wav files into the temporary directory
print("Copying .wav files to temporary directory...")
for wav_file in Path(session_path).glob("*.wav"):
    shutil.copy(wav_file, audio_dir)

# Iterate over all .wav files in the session folder
for audio_file in audio_dir.glob("*.wav"):
    if audio_file.is_file():
        print(f"Processing {audio_file.name}...")
        docker_cmd = [
            "docker",
            "run",
            "-it",
            "--rm",
            "-v",
            f"{os.getcwd()}/models:/root/.cache/whisper",
            "-v",
            f"{audio_dir.resolve()}:/app",
            "openai-whisper",
            "whisper",
            audio_file.name,
            "--model",
            "turbo",
            "--language",
            "Danish",
            "--output_dir",
            "/app",
            "--output_format",
            "txt",
        ]
        subprocess.run(docker_cmd, check=True)

# Call the Python script with the session number
print(f"Calling Python script to process session {session_number}...")
merge_script = script_dir / "Merge_Transcription.py"
subprocess.run(["python", str(merge_script), session_number], check=True)
