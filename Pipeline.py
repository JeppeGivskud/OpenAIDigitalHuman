from agents.voice import (
    VoicePipeline,
    SingleAgentVoiceWorkflow,
    AudioInput,
    VoicePipelineConfig,
    TTSModelSettings,
    STTModelSettings,
)
from agents import Agent
from Audio import (
    record_audio_while_pressed,
    handle_audio_stream,
    load_audio_file,
    save_audio_file,
    send_audio_to_audio2face_server,
    play_audio,
    resample_audio,
)
import os
from consolePrints import printLytter, printTænker, printClear


def create_pipeline(agent: Agent):
    """Creates a VoicePipeline for the given agent."""

    return VoicePipeline(
        workflow=SingleAgentVoiceWorkflow(agent),
        config=VoicePipelineConfig(
            stt_settings=STTModelSettings(language="da"),
            tts_settings=TTSModelSettings(voice="sage"),
        ),
    )


async def run_pipeline(
    pipeline,
    renderFace=False,
    useTokens=False,
    InitiateConversation=False,
    saveAudio=False,
):

    continue_conversation = True
    sessionID = makeSessionFolder()

    while continue_conversation:
        """Runs the voice pipeline with recorded audio."""

        user_samplerate = 24000
        AI_samplerate = 22050

        user_audio = None
        ai_audio = None

        printLytter()
        if InitiateConversation:
            # print("Loading pre-recorded audio...")
            user_audio = load_audio_file("saved_audio/User/Initiering.wav")
            user_audio = resample_audio(user_audio, 24000, user_samplerate)
            printClear()
        else:
            # print("Recording audio... (Press the spacebar to stop recording)")
            user_audio = record_audio_while_pressed()
            user_audio = resample_audio(user_audio, 24000, user_samplerate)

        # User done with speaking
        save_audio_file(
            user_audio,
            sessionID,
            "user",
            saveAudio=saveAudio,
            samplerate=user_samplerate,
        )

        openai_audio_input = AudioInput(buffer=user_audio, frame_rate=user_samplerate)

        if useTokens:
            # print("Using tokens...")
            printTænker()
            result = await pipeline.run(audio_input=openai_audio_input)

            # Stream the result
            ai_audio, continue_conversation = await handle_audio_stream(
                result=result,
                InitiateConversation=InitiateConversation,
                instance_name="/World/audio2face/PlayerStreaming",
                url="localhost:50051",
            )
            InitiateConversation = False
            ai_audio = resample_audio(ai_audio, 24000, AI_samplerate)

            # print("Response finished...", " Continue = ", continue_conversation)
        else:
            # print("Using recorded audio...")
            ai_audio = user_audio
            samplerate = 24000

        # AI done with generating audio
        save_audio_file(
            ai_audio, sessionID, "rosie", saveAudio=saveAudio, samplerate=AI_samplerate
        )

        if renderFace:
            # print("Sending audio to Audio2Face...")
            printClear()
            send_audio_to_audio2face_server(
                audio_data=ai_audio,
                samplerate=AI_samplerate,
                instance_name="/World/audio2face/PlayerStreaming",
                url="localhost:50051",
            )
        else:
            # print("Playing audio locally...")
            play_audio(ai_audio)


def makeSessionFolder():
    """
    Creates a new session folder and returns the incremented session number.

    Returns:
        int: The new session number.
    """
    folder_name_path = "saved_audio/FolderName"
    sessions_folder = "saved_audio/Sessions"

    # Ensure the Sessions folder exists
    os.makedirs(sessions_folder, exist_ok=True)

    # Read the current number from FolderName
    if os.path.exists(folder_name_path):
        with open(folder_name_path, "r") as file:
            try:
                current_number = int(file.read().strip())
            except ValueError:
                current_number = 0
    else:
        current_number = 0

    # Increment the number
    new_number = current_number + 1

    # Save the updated number back to FolderName
    with open(folder_name_path, "w") as file:
        file.write(str(new_number))

    # Create a new folder for the session
    session_folder_path = os.path.join(sessions_folder, str(new_number))
    os.makedirs(session_folder_path, exist_ok=True)

    return new_number
