import os
import re
from datetime import datetime

# Directory containing the .txt files
AUDIO_DIR = "./AudioFiles/session_6"
MERGED_FILE = "./AudioFiles/session_6_Merged_Python.txt"

# Initialize variables to track the oldest and newest dates
oldest_date = None
newest_date = None

# Prepare the merged content
merged_content = []
turn_count = 0  # Counter for the number of turns
total_sentence_length = 0  # Accumulator for total sentence length

# Process each .txt file in the directory
for txt_file in sorted(os.listdir(AUDIO_DIR)):
    if txt_file.endswith(".txt"):
        # Extract the date and time from the filename
        match = re.search(r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})", txt_file)
        if match:
            file_date_str = match.group(1)
            file_date = datetime.strptime(file_date_str, "%Y-%m-%d_%H-%M-%S")

            # Update the oldest and newest dates
            if oldest_date is None or file_date < oldest_date:
                oldest_date = file_date
            if newest_date is None or file_date > newest_date:
                newest_date = file_date
        else:
            file_date_str = "Unknown"

        # Determine the speaker type based on the filename
        if "rosie" in txt_file:
            speaker = "Rosie"
        elif "user" in txt_file:
            speaker = "User"
        else:
            speaker = "Unknown"

        # Read the content of the .txt file
        with open(os.path.join(AUDIO_DIR, txt_file), "r", encoding="utf-8") as f:
            text = f.read().strip()

        # Calculate the sentence length
        sentence_length = len(text)
        total_sentence_length += sentence_length  # Add to total length

        # Increment the turn count
        turn_count += 1

        # Append the speaker, date, sentence length, and text to the merged content
        merged_content.append(
            f"{speaker} ({file_date_str}, Length: {sentence_length} chars)\n{text}\n"
        )

# Calculate the difference in seconds between the oldest and newest dates
if oldest_date and newest_date:
    date_difference = int((newest_date - oldest_date).total_seconds())
else:
    date_difference = 0

# Calculate the average sentence length
average_sentence_length = total_sentence_length / turn_count if turn_count > 0 else 0

# Add the date range, difference, turn count, and average sentence length to the top of the merged content
header = [
    f"Oldest Date: {oldest_date.strftime('%Y-%m-%d_%H-%M-%S') if oldest_date else 'Unknown'}",
    f"Newest Date: {newest_date.strftime('%Y-%m-%d_%H-%M-%S') if newest_date else 'Unknown'}",
    f"Difference in Seconds: {date_difference}",
    f"Total Turns: {turn_count}",
    f"Average Sentence Length: {average_sentence_length:.2f} chars",
    "\n",
]
merged_content = "\n".join(header) + "\n".join(merged_content)

# Write the merged content to the output file
with open(MERGED_FILE, "w", encoding="utf-8") as f:
    f.write(merged_content)

print(f"Transcription and merging completed. Merged file: {MERGED_FILE}")
