import numpy as np
import numpy.typing as npt
import sounddevice as sd
import soundfile
from streaming_server.test_client import push_audio_track_stream
import sys
import keyboard
import csv
import os
import librosa
from consolePrints import printLytter


def resample_audio(audio, original_sr, target_sr):
    print("Resampling audio from {} Hz to {} Hz".format(original_sr, target_sr))
    resampled_audio = librosa.resample(audio, orig_sr=original_sr, target_sr=target_sr)
    return resampled_audio


def load_audio_file(file_path, samplerate=24000, channels=1):
    """
    Loads an audio file and returns the data and sample rate.

    Parameters:
        file_path (str): Path to the audio file.

    Returns:
        tuple: A tuple containing the audio data as a NumPy array and the sample rate.
    """
    import soundfile as sf

    data, samplerate = sf.read(file_path, dtype="float32")

    # Only Mono audio is supported
    if len(data.shape) > 1:
        data = np.average(data, axis=1)

    # sd.play(data, samplerate)
    # sd.wait()

    return data


def save_audio_file(audio_data, SessionID, Speaker, samplerate=24000, saveAudio=False):
    """
    Saves audio data to a file or logs metadata to a CSV file.

    Parameters:
        audio_data (np.ndarray): Audio data to save.
        SessionID (int): The session ID.
        Speaker (str): The speaker (e.g., "user" or "rosie").
        samplerate (int): Sample rate of the audio data.
    """
    from datetime import datetime

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    audio_length = len(audio_data) / samplerate  # Calculate audio length in seconds
    # print("saveAudio: ", saveAudio)
    if saveAudio:
        # Path for saving raw audio (if enabled)
        # print("Saving audio to file...")
        randomfilepath = (
            f"saved_audio/Sessions/{SessionID}/{current_datetime}-{Speaker}.wav"
        )
        soundfile.write(randomfilepath, audio_data, samplerate)

    # Save metadata to a CSV file
    csv_file_path = f"saved_data/Sessions/Session_{SessionID}_metadata.csv"
    file_exists = os.path.isfile(csv_file_path)

    with open(csv_file_path, mode="a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Write header if the file is being created
        if not file_exists:
            writer.writerow(["Timestamp", "AudioLengthSeconds", "Speaker", "SessionID"])
        # Write metadata row
        writer.writerow([current_datetime, audio_length, Speaker, SessionID])


def play_audio(audio_data, samplerate=24000, channels=1):
    """
    Plays back audio data.
    Only used for debugging
    """
    player = sd.OutputStream(samplerate=samplerate, channels=channels, dtype=np.float32)
    player.start()
    player.write(audio_data)


def record_audio_while_pressed(
    InitiateConversation=False, samplerate=24000, channels=1
):
    """
    Records an audio clip as long as a button is pressed and returns it as a NumPy array.

    Parameters:
        samplerate (int): The sampling rate for the audio.
        channels (int): The number of audio channels.

    Returns:
        np.ndarray: The recorded audio as a NumPy array.
    """

    # Create a buffer to store the recorded audio
    recorded_audio = []
    # Start the input stream
    with sd.InputStream(
        samplerate=samplerate, channels=channels, dtype=np.float32
    ) as stream:

        while not (keyboard.is_pressed("space")):
            # Read audio data from the stream
            audio_chunk, _ = stream.read(1024)  # Read in chunks of 1024 frames
            recorded_audio.append(audio_chunk)

            if keyboard.is_pressed("escape"):
                # print("Program stopped by user.")
                sys.exit()  # Terminates the entire program

    # print("Recording complete.")
    # Combine all chunks into a single NumPy array
    return np.concatenate(recorded_audio).flatten()


def format_audio_data(audio_data, samplerate=24000):
    """
    Formats audio data to be sent to the Audio2Face server.

    Parameters:
        audio_data (np.ndarray): The audio data to format.
        samplerate (int): The sample rate of the audio data.

    Returns:
        np.ndarray: The formatted audio data.
    """
    # Ensure the audio is mono
    if len(audio_data.shape) > 1:
        audio_data = np.average(audio_data, axis=1)

    return audio_data


def send_audio_to_audio2face_server(
    audio_data,
    samplerate=24000,
    instance_name="/World/audio2face/PlayerStreaming",
    url="localhost:50051",
):
    """
    Sends audio data to the Audio2Face Streaming Audio Player via gRPC requests.
    """
    # Format the audio data

    audio_data = format_audio_data(audio_data, samplerate)
    A2F_Samplerate = 16000
    audio_data = resample_audio(audio_data, samplerate, A2F_Samplerate)
    # sd.play(audio_data, samplerate)    #for debugging
    # sd.wait()                          #for debugging

    # print("Sending Audio")
    push_audio_track_stream(url, audio_data, A2F_Samplerate, instance_name)


def int16_to_float32(audio: npt.NDArray[np.int16]) -> npt.NDArray[np.float32]:
    return (audio.astype(np.float32) / 32768.0).clip(-1.0, 1.0)


async def handle_audio_stream(
    result,
    InitiateConversation=False,
    instance_name="/World/audio2face/PlayerStreaming",
    url="localhost:50051",
):
    """
    Handles streaming audio events, processes the audio, and optionally sends it to the Audio2Face server.

    Parameters:
        result (AsyncIterator): The asynchronous stream of audio events generated by the pipeline.
        renderFace (bool): Whether to send the processed audio to the Audio2Face server.
        instance_name (str): The instance name for the Audio2Face Streaming Audio Player on the Omniverse stage.
        url (str): The URL of the Audio2Face server (e.g., "localhost:50051").

    Behavior:
        - Collects audio data from the stream and concatenates it into a single audio buffer.
        - If `renderFace` is True, sends the audio to the Audio2Face server.
        - If `renderFace` is False, plays the audio locally.
    """
    incoming_response = []
    continue_conversation = True
    async for event in result.stream():
        if event.type == "voice_stream_event_lifecycle":
            # print(event.event)
            if event.event == "turn_ended":
                # print("turn_ended")
                break
            if event.event == "session_ended":
                # print("session should end")
                continue_conversation = False
                break
        if event.type == "voice_stream_event_audio":
            incoming_response.append(int16_to_float32(event.data))
        # print("global event printer: ", event.type)

    audio = np.concatenate(incoming_response).flatten()

    if InitiateConversation:
        # print("Ready to Initiate Conversation - Press space to start")
        printLytter()
        while not (keyboard.is_pressed("space")):
            if keyboard.is_pressed("space"):
                # print("Initiating conversation...")
                break

    return audio, continue_conversation
