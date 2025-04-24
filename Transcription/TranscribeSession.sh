#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Get the session number
SESSION_NUMBER=6  # Change this to the desired session number

# Define paths relative to the script's location
SESSION_PATH="$SCRIPT_DIR/../saved_audio/Sessions/$SESSION_NUMBER"
OUTPUT_DIR="$SCRIPT_DIR/../Transcription/Output"
AUDIO_DIR="$SCRIPT_DIR/../Transcription/AudioFiles/session_$SESSION_NUMBER"
MERGED_FILE="$SCRIPT_DIR/../Transcription/AudioFiles/session_${SESSION_NUMBER}_Merged.txt"

# Ensure the output and temporary directories exist
mkdir -p "$OUTPUT_DIR"
mkdir -p "$AUDIO_DIR"

# Copy all .wav files into the temporary directory
echo "Copying .wav files to temporary directory..."
cp "$SESSION_PATH"/*.wav "$AUDIO_DIR"

# Iterate over all .wav files in the session folder
for audio_file in "$AUDIO_DIR"/*.wav; do
    if [ -f "$audio_file" ]; then
        echo "Processing $audio_file..."
        
        # Extract the filename without the path
        filename=$(basename -- "$audio_file")
        
        # Run the Docker container to transcribe the audio file
        docker run -it --rm \
            -v "${PWD}/models:/root/.cache/whisper" \
            -v "${AUDIO_DIR}:/app" \
            openai-whisper whisper "$filename" \
            --model turbo \
            --language Danish \
            --output_dir /app \
            --output_format txt
    fi
done

# Initialize variables to track the oldest and most recent dates
oldest_date=""
newest_date=""

# Merge all .txt files into one with speaker names and timestamps
echo "Merging text files into $MERGED_FILE..."
> "$MERGED_FILE"  # Clear the merged file if it exists

for txt_file in "$AUDIO_DIR"/*.txt; do
    if [ -f "$txt_file" ]; then
        # Extract the filename without the path
        filename=$(basename -- "$txt_file")
        
        # Extract the date and time from the filename using a POSIX-compliant method
        file_date=$(echo "$filename" | sed -E 's/.*([0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}).*/\1/')

        # Update the oldest and newest dates
        if [[ -n "$file_date" ]]; then
            if [[ -z "$oldest_date" || "$file_date" < "$oldest_date" ]]; then
                oldest_date="$file_date"
            fi
            if [[ -z "$newest_date" || "$file_date" > "$newest_date" ]]; then
                newest_date="$file_date"
            fi
        fi
        echo "Extracted date: $file_date"
        echo "Oldest date so far: $oldest_date"
        echo "Newest date so far: $newest_date"

        # Determine the speaker type based on the filename
        if [[ "$filename" == *rosie.txt ]]; then
            speaker="Rosie"
        elif [[ "$filename" == *user.txt ]]; then
            speaker="User"
        else
            speaker="Unknown"
        fi

        # Write the speaker name, timestamp, and the text to the merged file
        echo "$speaker ($file_date)" >> "$MERGED_FILE"
        cat "$txt_file" >> "$MERGED_FILE"
        echo "" >> "$MERGED_FILE"  # Add a blank line for separation
    fi
done

# Calculate the difference in seconds between the oldest and newest dates
if [[ -n "$oldest_date" && -n "$newest_date" ]]; then
    oldest_epoch=$(date -j -f "%Y-%m-%d_%H-%M-%S" "$oldest_date" "+%s")
    newest_epoch=$(date -j -f "%Y-%m-%d_%H-%M-%S" "$newest_date" "+%s")
    date_difference=$((newest_epoch - oldest_epoch))
else
    date_difference=0
fi

# Add the date range and difference to the top of the merged file
{
    echo "Oldest Date: $oldest_date"
    echo "Newest Date: $newest_date"
    echo "Difference in Seconds: $date_difference"
    echo ""
    cat "$MERGED_FILE"
} > "${MERGED_FILE}.tmp" && mv "${MERGED_FILE}.tmp" "$MERGED_FILE"

echo "Transcription and merging completed. Merged file: $MERGED_FILE"