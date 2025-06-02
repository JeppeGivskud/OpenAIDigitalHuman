import re
import os
import csv


def extract_user_turns_from_folders(base_path, output_csv):
    # Define the folder names (e.g., Day02 to Day13)
    folders = [f"Day{str(i).zfill(2)}" for i in range(2, 14)]

    # Regular expression to match speaker lines
    speaker_regex = (
        r"^(User) \(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}, Length: (\d+) chars\)"
    )

    # Initialize a list to store user turn data
    user_turns = []

    # Iterate through each folder
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        if os.path.exists(folder_path):
            # Iterate through all text files in the folder
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".txt"):
                    file_path = os.path.join(folder_path, file_name)
                    participant = f"{folder}_{file_name.split('_')[0]}"  # Combine day and participant ID

                    with open(file_path, "r", encoding="utf-8") as file:
                        turn_number = 1
                        for line in file:
                            line = line.strip()
                            match = re.match(speaker_regex, line)
                            if match:
                                char_count = int(match.group(2))
                                user_turns.append(
                                    {
                                        "Day": folder,
                                        "Participant": participant,
                                        "Turn Number": turn_number,
                                        "Sentence Length": char_count,
                                    }
                                )
                                turn_number += 1

    # Write user turn data to a CSV file
    with open(output_csv, "w", encoding="utf-8", newline="") as csvfile:
        fieldnames = ["Day", "Participant", "Turn Number", "Sentence Length"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(user_turns)

    print(f"User turn data saved to {output_csv}")


# Example usage
base_path = r"C:\Users\Jeppe\Programmering\OpenAIDigitalHuman\Transcription\Sessions for analysis\Transcriptions"
output_csv = r"C:\Users\Jeppe\Programmering\OpenAIDigitalHuman\Transcription\Sessions for analysis\Transcriptions\user_turns_combined.csv"
extract_user_turns_from_folders(base_path, output_csv)
