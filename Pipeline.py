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
)


def create_pipeline(agent: Agent):
    """Creates a VoicePipeline for the given agent."""
    return VoicePipeline(
        workflow=SingleAgentVoiceWorkflow(agent),
        config=VoicePipelineConfig(tts_settings=TTSModelSettings(voice="sage")),
    )


async def run_pipeline(pipeline, omniverse=False):
    while True:
        """Runs the voice pipeline with recorded audio."""

        print("Recording audio... (Press and hold the spacebar to stop recording)")
        buffer = record_audio_while_pressed()
        audio_input = AudioInput(buffer=buffer)
        print("Audio recorded.")

        # result = await pipeline.run(audio_input)
        result = await pipeline.run(audio_input)

        # Stream the result
        await handle_audio_stream(
            result,
            send_audio=omniverse,  # Set to True if you want to send audio to Audio2Face
            instance_name="/World/audio2face/PlayerStreaming",
            url="localhost:50051",
        )

        # Wait for user input to continue
        input("Press Enter to run the pipeline again...")
