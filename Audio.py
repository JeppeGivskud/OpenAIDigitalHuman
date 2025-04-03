import numpy as np
import sounddevice as sd
import grpc
import time
import soundfile

from streaming_server import audio2face_pb2
from streaming_server import audio2face_pb2_grpc


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
    audio_fpath,
    instance_name="/World/audio2face/PlayerStreaming",
    url="localhost:50051",
):
    """
    Sends audio data to the Audio2Face Streaming Audio Player via gRPC requests.

    Parameters:
        audio_fpath (str): Path to the WAV audio file.
        instance_name (str): Prim path of the Audio2Face Streaming Audio Player on the stage.
        url (str): URL of the Audio2Face Streaming Audio Player server (default: "localhost:50051").
    """

    def push_audio_track_stream(url, audio_data, samplerate, instance_name):
        """
        Pushes audio chunks sequentially via PushAudioStreamRequest.
        """
        chunk_size = samplerate // 10  # Number of samples per chunk
        sleep_between_chunks = 0.04  # Time to wait between sending chunks
        block_until_playback_is_finished = True

        with grpc.insecure_channel(url) as channel:
            print("Channel created")
            stub = audio2face_pb2_grpc.Audio2FaceStub(channel)

            def make_generator():
                # First message with start_marker
                start_marker = audio2face_pb2.PushAudioRequestStart(
                    samplerate=samplerate,
                    instance_name=instance_name,
                    block_until_playback_is_finished=block_until_playback_is_finished,
                )
                yield audio2face_pb2.PushAudioStreamRequest(start_marker=start_marker)

                # Subsequent messages with audio_data
                for i in range(len(audio_data) // chunk_size + 1):
                    time.sleep(sleep_between_chunks)
                    chunk = audio_data[i * chunk_size : i * chunk_size + chunk_size]
                    yield audio2face_pb2.PushAudioStreamRequest(
                        audio_data=chunk.astype(np.float32).tobytes()
                    )

            request_generator = make_generator()
            print("Sending audio data...")
            response = stub.PushAudioStream(request_generator)
            if response.success:
                print("SUCCESS")
            else:
                print(f"ERROR: {response.message}")
        print("Channel closed")

    # Read the audio file
    data, samplerate = soundfile.read(audio_fpath, dtype="float32")

    # Ensure the audio is mono (only one channel is supported)
    if len(data.shape) > 1:
        data = np.average(data, axis=1)

    # Emulate latency before sending
    sleep_time = 2.0  # Adjust as needed
    print(f"Sleeping for {sleep_time} seconds")
    time.sleep(sleep_time)

    # Push audio chunks sequentially
    push_audio_track_stream(url, data, samplerate, instance_name)


def play_audio(audio_data, samplerate=24000, channels=1):
    """Plays back audio data."""
    player = sd.OutputStream(samplerate=samplerate, channels=channels, dtype=np.int16)
    player.start()
    player.write(audio_data)
