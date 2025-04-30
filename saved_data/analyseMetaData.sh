#!/bin/bash

# Initialize variables
declare -A speakerAudioLength
declare -A speakerTurns

# Output file
output_file="all_sessions.csv"
echo "Speaker,Average Audio Length (seconds),Total Audio Length (seconds),Turns" > "$output_file"

# Loop through all matching CSV files
for file in Sesssion_*_metadata.csv; do
    # Skip if no files match
    [ -e "$file" ] || continue

    # Process the file using awk
    awk -F',' 'NR > 1 { 
        speakerTurns[$3]++; 
        speakerAudioLength[$3] += $2; 
        totalTurns++;
    } 
    END {
        for (speaker in speakerTurns) {
            printf "%s,%.2f,%.2f,%d\n", speaker, speakerAudioLength[speaker] / speakerTurns[speaker], speakerAudioLength[speaker], speakerTurns[speaker];
        }
    }' "$file" >> "$output_file"
done

# Append total turns to the output file
total_turns=$(awk -F',' 'NR > 1 { total++ } END { print total }' Sesssion_*_metadata.csv)
echo "Total, , ,$total_turns" >> "$output_file"
