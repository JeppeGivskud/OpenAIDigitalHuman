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

# Call the Python script with the session number
echo "Calling Python script to process session $SESSION_NUMBER..."
python3 "$SCRIPT_DIR/Merge_Transcription.py" "$SESSION_NUMBER"