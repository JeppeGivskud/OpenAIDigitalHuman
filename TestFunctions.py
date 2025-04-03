import asyncio
import sounddevice as sd
import numpy as np


async def stream_microphone_data(samplerate=24000, channels=1, chunk_size=1024):
    """
    Asynchronously streams microphone data in chunks.

    Parameters:
        samplerate (int): Sampling rate for the audio.
        channels (int): Number of audio channels.
        chunk_size (int): Number of frames per chunk.

    Yields:
        np.ndarray: A chunk of audio data as a NumPy array.
    """
    loop = asyncio.get_event_loop()

    # Callback function to collect audio chunks
    def audio_callback(indata, frames, time, status):
        if status:
            print(f"Audio status: {status}")
        loop.call_soon_threadsafe(queue.put_nowait, indata.copy())

    # Create an asyncio queue to hold audio chunks
    queue = asyncio.Queue()

    # Open the input stream
    with sd.InputStream(
        samplerate=samplerate,
        channels=channels,
        blocksize=chunk_size,
        callback=audio_callback,
        dtype=np.int16,
    ):
        print("Streaming microphone data...")
        while True:
            # Wait for the next chunk of audio data
            chunk = await queue.get()
            yield chunk
