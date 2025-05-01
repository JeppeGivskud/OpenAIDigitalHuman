import asyncio
import threading
import sys
from GUI import root  # Import the tkinter root object from GUI.py
from My_Agents import Rosie_dk_agent
from Pipeline import create_pipeline, run_pipeline


def start_gui():
    root.mainloop()  # Start the tkinter GUI event loop


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

    # Start the GUI in a separate thread
    gui_thread = threading.Thread(target=start_gui, daemon=True)
    gui_thread.start()

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
