import os
import subprocess

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, "")
transcription_dir = os.path.join(script_dir, "../AudioFiles")
print(f"script_dir: {script_dir}")
print(f"base_dir: {base_dir}")
print(f"transcription_dir: {transcription_dir}")
# Loop through all day folders
for day_folder in os.listdir(base_dir):
    day_path = os.path.join(base_dir, day_folder)
    if os.path.isdir(day_path):
        # Loop through all random number folders within the day folder
        for random_number_folder in os.listdir(day_path):
            random_number_path = os.path.join(day_path, random_number_folder)
            if os.path.isdir(random_number_path):
                # Check if the transcription file already exists
                transcription_file = os.path.join(
                    transcription_dir,
                    f"{day_folder}/{random_number_folder}_Merged_Python.txt",
                )
            if not os.path.exists(transcription_file):
                print(
                    f"Transcription missing for file {transcription_file}  random_number_path{random_number_path}/day_folder{day_folder}/random_number_folder{random_number_folder}. Starting transcription..."
                )
                # C:\Users\Jeppe\Programmering\OpenAIDigitalHuman\Transcription\Sessions for analysis\../Transcription/AudioFiles\Day02/6_Merged_Python.txt
                # C:\Users\Jeppe\Programmering\OpenAIDigitalHuman\Transcription\AudioFiles\Day02\6_Merged_Python.txt
                # Call the TranscribeSession.py script with the session number
                subprocess.run(
                    [
                        "python",
                        os.path.join(script_dir, "TranscribeSession.py"),
                        day_folder,
                        random_number_folder,
                    ],
                    check=True,
                )
            else:
                print(
                    f"Transcription already exists for session {transcription_file} {day_folder}/{random_number_folder}. Skipping..."
                )
