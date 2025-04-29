#!/bin/bash

# Define the base directory for sessions and transcriptions
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SESSION_DIR="$BASE_DIR/../saved_audio/Sessions"
TRANSCRIPTION_DIR="$BASE_DIR/../Transcription/AudioFiles"

# Loop through all session folders
for session_folder in "$SESSION_DIR"/*; do
    if [ -d "$session_folder" ]; then
        # Extract the session number from the folder name
        session_number=$(basename "$session_folder")
        
        # Check if the transcription file already exists
        transcription_file="$TRANSCRIPTION_DIR/session_${session_number}_Merged_Python.txt"
        if [ ! -f "$transcription_file" ]; then
            echo "Transcription missing for session $session_number. Starting transcription..."
            
            # Call the TranscribeSession.sh script with the session number
            "$BASE_DIR/TranscribeSession.sh" "$session_number"
        else
            echo "Transcription already exists for session $session_number. Skipping..."
        fi
    fi
done