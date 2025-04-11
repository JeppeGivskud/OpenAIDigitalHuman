import numpy as np
import sounddevice as sd
import soundfile
from streaming_server.test_client import push_audio_track_stream


def load_audio_file(file_path):
    """
    Loads an audio file and returns the data and sample rate.

    Parameters:
        file_path (str): Path to the audio file.

    Returns:
        tuple: A tuple containing the audio data as a NumPy array and the sample rate.
    """
    data, samplerate = soundfile.read(file_path, dtype="float32")
    # Only Mono audio is supported
    if len(data.shape) > 1:
        data = np.average(data, axis=1)

    # sd.play(data, samplerate)
    # sd.wait()
    return data, samplerate


def save_audio_file(audio_data, samplerate=24000):
    """
    Saves audio data to a file.

    Parameters:
        file_path (str): Path to save the audio file.
        audio_data (np.ndarray): Audio data to save.
        samplerate (int): Sample rate of the audio data.
    """
    from datetime import datetime

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    randomfilepath = f"saved_audio/{current_datetime}.wav"

    soundfile.write(randomfilepath, audio_data, samplerate)


def record_audio(samplerate=24000, duration=3, channels=1):
    """Records an audio clip and returns it as a NumPy array."""
    print("Recording...")
    recording = sd.rec(
        int(samplerate * duration),
        samplerate=samplerate,
        channels=channels,
        dtype=np.int16,
    )
    sd.wait()
    print("Recording complete.")
    return recording.flatten()


def play_audio(audio_data, samplerate=24000, channels=1):
    """
    Plays back audio data.
    Only used for debugging
    """
    player = sd.OutputStream(samplerate=samplerate, channels=channels, dtype=np.int16)
    player.start()
    player.write(audio_data)


def record_audio_while_pressed(samplerate=24000, channels=1):
    import keyboard

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
        samplerate=samplerate, channels=channels, dtype=np.int16
    ) as stream:

        while not (keyboard.is_pressed("space")):
            # Read audio data from the stream
            audio_chunk, _ = stream.read(1024)  # Read in chunks of 1024 frames
            recorded_audio.append(audio_chunk)

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

    # Convert audio data to float32 and normalize to [-1.0, 1.0]
    if audio_data.dtype != np.float32:
        audio_data = audio_data.astype(np.float32)
    audio_data /= np.max(np.abs(audio_data))  # Normalize to [-1.0, 1.0]
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

    # sd.play(audio_data, samplerate)    #for debugging
    # sd.wait()                          #for debugging

    print("Sending Audio")
    push_audio_track_stream(url, audio_data, samplerate, instance_name)


async def handle_audio_stream(
    result,
    renderFace=False,
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

    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            incoming_response.append(event.data)

    audio = np.concatenate(incoming_response).flatten()

    save_audio_file(audio)  # Save the audio file for debugging
    if renderFace:
        send_audio_to_audio2face_server(
            audio,
            instance_name=instance_name,
            url=url,
        )
    else:
        play_audio(audio)
