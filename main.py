import asyncio
from My_Agents import Trothilde_dk_agent
from Pipeline import create_pipeline, run_pipeline


async def main():
    pipeline = create_pipeline(Trothilde_dk_agent)
    await run_pipeline(pipeline, omniverse=True)


if __name__ == "__main__":
    asyncio.run(main())
