from agents.voice import VoicePipeline, SingleAgentVoiceWorkflow, AudioInput
from agents import Agent
from Audio import (
    record_audio,
    handle_audio_stream,
)


def create_pipeline(agent: Agent):
    """Creates a VoicePipeline for the given agent."""
    return VoicePipeline(workflow=SingleAgentVoiceWorkflow(agent))


async def run_pipeline(pipeline):
    while True:
        """Runs the voice pipeline with recorded audio."""
        buffer = record_audio()
        audio_input = AudioInput(buffer=buffer)
        # result = await pipeline.run(audio_input)
        result = await pipeline.run(audio_input)

        # Stream the result
        await handle_audio_stream(
            result,
            send_audio=True,  # Set to True if you want to send audio to Audio2Face
            instance_name="/World/audio2face/PlayerStreaming",
            url="localhost:50051",
        )

        # Wait for user input to continue
        input("Press Enter to run the pipeline again...")
