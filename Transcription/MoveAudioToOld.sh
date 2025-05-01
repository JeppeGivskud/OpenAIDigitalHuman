#!/bin/bash

# Define directories
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSCRIPTION_DIR="$BASE_DIR/../Transcription/AudioFiles/"
OLD_DIR="$BASE_DIR/../saved_audio/old"
SESSIONS_DIR="$BASE_DIR/../saved_audio/Sessions"
OLD_TIMESTAMP_DIR="$OLD_DIR/$(date +"%Y%m%d_%H%M%S")"

METADATA_DIR="$BASE_DIR/../saved_data/Sessions"
OLD_DATA_DIR="$BASE_DIR/../saved_data/old"
OLD_TIMESTAMP_DIR_DATA="$OLD_DATA_DIR/$(date +"%Y%m%d_%H%M%S")"

# Ensure the old directory exists
mkdir -p "$OLD_DIR"
mkdir -p "$OLD_DATA_DIR"
mkdir -p "$OLD_TIMESTAMP_DIR"
mkdir -p "$OLD_TIMESTAMP_DIR_DATA"

# Move contents from ../Transcription/AudioFiles/ to ../saved_audio/old/
if [ -d "$TRANSCRIPTION_DIR" ]; then
    echo "Moving files from $TRANSCRIPTION_DIR to $OLD_TIMESTAMP_DIR..."
    find "$TRANSCRIPTION_DIR" -type f ! -name ".gitkeep" -exec mv {} "$OLD_TIMESTAMP_DIR/" \; || echo "No regular files to move."
else
    echo "Directory $TRANSCRIPTION_DIR does not exist. Skipping..."
fi

# Move contents from ../saved_audio/Sessions to ../saved_audio/old/timestamp
if [ -d "$SESSIONS_DIR" ]; then
    echo "Moving files and folders from $SESSIONS_DIR to $OLD_TIMESTAMP_DIR..."
    mkdir -p "$OLD_TIMESTAMP_DIR"  # Ensure the target directory exists
    find "$SESSIONS_DIR" -mindepth 1 -maxdepth 1 ! -name ".gitkeep" -exec mv {} "$OLD_TIMESTAMP_DIR/" \; || echo "No files or folders to move."
else
    echo "Directory $SESSIONS_DIR does not exist. Skipping..."
fi

# Move contents from ../saved_data/Sessions to ../saved_data/old/timestamp
if [ -d "$METADATA_DIR" ]; then
    echo "Moving files and folders from $METADATA_DIR to $OLD_TIMESTAMP_DIR_DATA..."
    mkdir -p "$OLD_TIMESTAMP_DIR_DATA"  # Ensure the target directory exists
    find "$METADATA_DIR" -mindepth 1 -maxdepth 1 ! -name ".gitkeep" -exec mv {} "$OLD_TIMESTAMP_DIR_DATA/" \; || echo "No files or folders to move."
else
    echo "Directory $METADATA_DIR does not exist. Skipping..."
fi

echo "File moving completed."