import asyncio
import sys
from My_Agents import Rosie_dk_agent
from Pipeline import create_pipeline, run_pipeline


async def main():
    renderFace = False
    useTokens = False
    prerecordedaudiopath = None
    if len(sys.argv) >= 4:
        renderFace = sys.argv[1].lower() == "true"
        useTokens = sys.argv[2].lower() == "true"
        prerecordedaudiopath = sys.argv[3].lower()

    pipeline = create_pipeline(Rosie_dk_agent)
    print(renderFace, useTokens)
    await run_pipeline(
        pipeline,
        renderFace=renderFace,
        useTokens=useTokens,
        prerecordedaudiopath=prerecordedaudiopath,
    )


if __name__ == "__main__":
    asyncio.run(main())
