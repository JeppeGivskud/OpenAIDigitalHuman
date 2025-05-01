import asyncio
import sys
from My_Agents import Rosie_dk_agent
from Pipeline import create_pipeline, run_pipeline


async def main():
    renderFace = False
    useTokens = False
    InitiateConversation = False
    saveAudio = False
    if len(sys.argv) >= 5:

        renderFace = sys.argv[1].lower() == "true"
        useTokens = sys.argv[2].lower() == "true"
        InitiateConversation = sys.argv[3].lower() == "true"
        saveAudio = sys.argv[4].lower() == "true"

    pipeline = create_pipeline(Rosie_dk_agent)

    if renderFace:
        print("Rendering face")
    if useTokens:
        print("Using tokens")
    if InitiateConversation:
        print("Initiating conversation")
    if saveAudio:
        print("Saving microphone audio:", saveAudio)

    await run_pipeline(
        pipeline,
        renderFace=renderFace,
        useTokens=useTokens,
        InitiateConversation=InitiateConversation,
        saveAudio=saveAudio,
    )


if __name__ == "__main__":
    asyncio.run(main())
