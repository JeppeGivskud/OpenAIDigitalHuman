from agents.voice import (
    VoicePipeline,
    SingleAgentVoiceWorkflow,
    AudioInput,
    VoicePipelineConfig,
    TTSModelSettings,
)
from agents import Agent
from Audio import (
    record_audio_while_pressed,
    handle_audio_stream,
    load_audio_file,
    send_audio_to_audio2face_server,
    play_audio,
)


def create_pipeline(agent: Agent):
    """Creates a VoicePipeline for the given agent."""
    return VoicePipeline(
        workflow=SingleAgentVoiceWorkflow(agent),
        config=VoicePipelineConfig(tts_settings=TTSModelSettings(voice="sage")),
    )


async def run_pipeline(
    pipeline, renderFace=False, useTokens=False, prerecordedaudiopath=None
):
    while True:
        """Runs the voice pipeline with recorded audio."""

        print("Recording audio... (Press and hold the spacebar to stop recording)")
        mic_recording = record_audio_while_pressed()
        audio_input = AudioInput(buffer=mic_recording)
        print("Audio recorded.")

        if useTokens:
            # Send the audio input to the pipeline
            print("Sending audio to Audio2Face...")
            result = await pipeline.run(audio_input)

            # Stream the result
            await handle_audio_stream(
                result,
                renderFace=renderFace,  # Set to True if you want to send audio to Audio2Face
                instance_name="/World/audio2face/PlayerStreaming",
                url="localhost:50051",
            )
        else:
            if prerecordedaudiopath != None:
                print("loading file - ", prerecordedaudiopath)
                file, samplerate = load_audio_file(prerecordedaudiopath)
            else:
                print("Using recorded audio...")
                file = mic_recording
                samplerate = 24000

            if renderFace:
                # Send the audio input to the pipeline
                print("Sending audio to Audio2Face...")
                send_audio_to_audio2face_server(
                    file,
                    samplerate=samplerate,
                    instance_name="/World/audio2face/PlayerStreaming",
                    url="localhost:50051",
                )
            else:
                # Play the audio locally
                print("Playing audio locally...")
                play_audio(file, samplerate)

        # Wait for user input to continue
        input("Press Enter to run the pipeline again...")
