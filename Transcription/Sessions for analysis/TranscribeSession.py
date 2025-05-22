import os
import sys
import shutil
import subprocess
from pathlib import Path

# Check if a session path is provided
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <day_folder> <random_number_folder>")
    sys.exit(1)

# Get the day folder and random number folder from the command-line arguments
day_folder = sys.argv[1]
random_number_folder = sys.argv[2]

# Get the directory of the script
script_dir = Path(__file__).resolve().parent

# Define paths relative to the script's location
session_path = script_dir / day_folder / random_number_folder
audio_dir = script_dir / f"../AudioFiles/{day_folder}/{random_number_folder}"
merged_file = (
    script_dir / f"../AudioFiles/{day_folder}/{random_number_folder}_Merged.txt"
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
        print(f"Processing {audio_file.name}... with cuda")
        docker_cmd = [
            "docker",
            "run",
            "--gpus",
            "all",  # <-- Add this line
            "-it",
            "--rm",
            "-v",
            f"{os.getcwd()}/models:/root/.cache/whisper",
            "-v",
            f"{audio_dir.resolve()}:/app",
            "openai-whisper",
            "whisper",
            audio_file.name,
            "--device",
            "cuda",
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
print(f"Calling Python script to process {day_folder}/{random_number_folder}...")
merge_script = script_dir / "Merge_Transcription.py"
subprocess.run(
    ["python", str(merge_script), day_folder, random_number_folder], check=True
)
