import numpy as np
import numpy.typing as npt
import sounddevice as sd
import soundfile
from streaming_server.test_client import push_audio_track_stream
import sys
import keyboard
import csv
import os
from consolePrints import printLytter


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


def read_variable(path):
    # Read the current value from the file
    with open(path, "r") as file:
        try:
            return int(file.read().strip())
        except ValueError:
            return 1


def record_audio_while_pressed(samplerate=24000, channels=1):
    """
    Records an audio clip as long as a button is pressed and returns it as a NumPy array.

    Parameters:
        samplerate (int): The sampling rate for the audio.
        channels (int): The number of audio channels.

    Returns:
        np.ndarray: The recorded audio as a NumPy array.
    """
    with open("recording_audio", "w") as file:
        file.write(str(1))

    # Create a buffer to store the recorded audio
    recorded_audio = []
    # Start the input stream
    with sd.InputStream(
        samplerate=samplerate, channels=channels, dtype=np.float32
    ) as stream:
        record = read_variable("recording_audio")
        while record == 1:
            Initiate = read_variable("initiate_conversation")
            record = read_variable("recording_audio")

            if Initiate == 1:
                recorded_audio = load_audio_file("saved_audio/User/Initiering.wav")
                return recorded_audio
            else:
                # Read audio data from the stream
                audio_chunk, _ = stream.read(1024)  # Read in chunks of 1024 frames
                recorded_audio.append(audio_chunk)

            # If the current condition is Initiate the recorded audio is overwritten
            if keyboard.is_pressed("escape"):
                # print("Program stopped by user.")
                sys.exit()  # Terminates the entire program

    return trim_audio(np.concatenate(recorded_audio).flatten())


first_time = True  # Used to trim the audio only the first time the user initiates the conversation


def trim_audio(audio_data, sample_rate=24000, max_length_sec=30):
    """
    Trims the audio data to a maximum length.

    Parameters:
        audio_data (np.ndarray): The audio data to trim.
        max_length (int): The maximum length of the audio data.

    Returns:
        np.ndarray: The trimmed audio data.
    """
    global first_time
    if first_time:
        first_time = False
        max_length_sec = 5

    print(
        "Trimming audio to max length of ",
        max_length_sec,
        " seconds, was previously",
        len(audio_data) / sample_rate,
        "seconds long",
    )
    length = int(max_length_sec * sample_rate)  # Convert seconds to samples
    if len(audio_data) > length:
        audio_data = audio_data[-length:]  # Take the last `length` samples
    return audio_data


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
    if len(audio_data.shape) > 1:
        audio_data = np.average(audio_data, axis=1)

    push_audio_track_stream(url, audio_data, samplerate, instance_name)


def int16_to_float32(audio: npt.NDArray[np.int16]) -> npt.NDArray[np.float32]:
    return (audio.astype(np.float32) / 32768.0).clip(-1.0, 1.0)


async def handle_audio_stream(
    result,
    InitiateConversation=False,
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

    waiting = read_variable("recording_audio")
    # print("Ready to Initiate Conversation - Press space to start")
    printLytter()
    print("Waiting for facilitator")
    while waiting == 1:
        waiting = read_variable("recording_audio")
    with open("initiate_conversation", "w") as file:
        file.write(str(0))
    return audio, continue_conversation
