import csv
import glob
import os

# Initialize variables
speaker_audio_length = {}
speaker_turns = {}
total_turns = 0

# Output file
output_file = "all_sessions.csv"

# Write header to the output file
with open(output_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "Session ID",
            "Speaker",
            "Average Audio Length (seconds)",
            "Total Audio Length (seconds)",
            "Turns",
        ]
    )

# Process all matching CSV files
for file in glob.glob("Sessions/Session_*_metadata.csv"):
    session_id = os.path.basename(file).split("_")[
        1
    ]  # Extract session ID from filename

    # Reset session-specific statistics
    session_speaker_audio_length = {}
    session_speaker_turns = {}

    with open(file, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            speaker = row["Speaker"]
            audio_length = float(row["AudioLengthSeconds"])

            # Update session-specific statistics
            session_speaker_turns[speaker] = session_speaker_turns.get(speaker, 0) + 1
            session_speaker_audio_length[speaker] = (
                session_speaker_audio_length.get(speaker, 0) + audio_length
            )
            total_turns += 1

    # Write session-specific results to the output file
    with open(output_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        for speaker, turns in session_speaker_turns.items():
            avg_audio_length = session_speaker_audio_length[speaker] / turns
            total_audio_length = session_speaker_audio_length[speaker]
            writer.writerow(
                [
                    session_id,
                    speaker,
                    f"{avg_audio_length:.2f}",
                    f"{total_audio_length:.2f}",
                    turns,
                ]
            )
