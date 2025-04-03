import numpy as np
import sounddevice as sd


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


from streaming_server.test_client import push_audio_track_stream


def send_audio_to_audio2face_server(
    audio_fpath,
    instance_name="/World/audio2face/PlayerStreaming",
    url="localhost:50051",
):
    """
    Sends audio data to the Audio2Face Streaming Audio Player via gRPC requests.
    """
    import soundfile

    # Read the audio file
    data, samplerate = soundfile.read(audio_fpath, dtype="float32")

    # Ensure the audio is mono
    if len(data.shape) > 1:
        data = np.average(data, axis=1)

    # Use the function from test_client.py
    push_audio_track_stream(url, data, samplerate, instance_name)


def play_audio(audio_data, samplerate=24000, channels=1):
    """Plays back audio data."""
    player = sd.OutputStream(samplerate=samplerate, channels=channels, dtype=np.int16)
    player.start()
    player.write(audio_data)
