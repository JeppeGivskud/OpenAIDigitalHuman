import numpy as np
import sounddevice as sd
import soundfile
from streaming_server.test_client import push_audio_track_stream


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


def send_audio_to_audio2face_server(
    audio_data,
    samplerate=24000,
    instance_name="/World/audio2face/PlayerStreaming",
    url="localhost:50051",
):
    """
    Sends audio data to the Audio2Face Streaming Audio Player via gRPC requests.
    """

    # Ensure the audio is mono
    if len(audio_data.shape) > 1:
        audio_data = np.average(audio_data, axis=1)

    # Convert audio data to float32 and normalize to [-1.0, 1.0]
    if audio_data.dtype != np.float32:
        audio_data = audio_data.astype(np.float32)
    audio_data /= np.max(np.abs(audio_data))  # Normalize to [-1.0, 1.0]

    # Use the function from test_client.py
    push_audio_track_stream(url, audio_data, samplerate, instance_name)


def play_audio(audio_data, samplerate=24000, channels=1):
    """Plays back audio data."""
    player = sd.OutputStream(samplerate=samplerate, channels=channels, dtype=np.int16)
    player.start()
    player.write(audio_data)


async def handle_audio_stream(
    result,
    send_audio=False,
    instance_name="/World/audio2face/PlayerStreaming",
    url="localhost:50051",
    buffer_size=100000,
):
    """
    Handles streaming audio events, buffers small chunks, and optionally sends them to the Audio2Face server.

    Parameters:
        result (AsyncIterator): The asynchronous stream of audio events.
        send_audio (bool): Whether to send the audio to the Audio2Face server.
        instance_name (str): The instance name for the Audio2Face server.
        url (str): The URL of the Audio2Face server.
        buffer_size (int): The size of the buffer in samples.
    """
    buffer = []  # Temporary storage for audio chunks
    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            # Append the new chunk to the buffer
            buffer.append(event.data)

            # Combine chunks if the buffer size exceeds the threshold
            combined_audio = np.concatenate(buffer)
            if len(combined_audio) >= buffer_size:
                if send_audio:
                    send_audio_to_audio2face_server(
                        combined_audio[:buffer_size],  # Send only up to the buffer size
                        samplerate=24000,
                        instance_name=instance_name,
                        url=url,
                    )
                else:
                    play_audio(combined_audio[:buffer_size])

                # Keep the remaining audio in the buffer
                buffer = [combined_audio[buffer_size:]]

    # Handle any remaining audio in the buffer
    if buffer:
        remaining_audio = np.concatenate(buffer)
        if send_audio:
            send_audio_to_audio2face_server(
                remaining_audio,
                samplerate=24000,
                instance_name=instance_name,
                url=url,
            )
        else:
            play_audio(remaining_audio)
