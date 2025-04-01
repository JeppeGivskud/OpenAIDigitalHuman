from agents.voice import VoicePipeline, SingleAgentVoiceWorkflow, AudioInput
from agents import Agent
from Audio import record_audio, play_audio


def create_pipeline(agent: Agent):
    """Creates a VoicePipeline for the given agent."""
    return VoicePipeline(workflow=SingleAgentVoiceWorkflow(agent))


async def run_pipeline(pipeline):
    while True:
        """Runs the voice pipeline with recorded audio."""
        buffer = record_audio()
        audio_input = AudioInput(buffer=buffer)
        result = await pipeline.run(audio_input)

        # Stream the result
        async for event in result.stream():
            if event.type == "voice_stream_event_audio":
                play_audio(event.data)

        # Wait for user input to continue
        input("Press Enter to run the pipeline again...")
