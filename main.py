import asyncio
from Agents import assistant_agent
from Pipeline import create_pipeline, run_pipeline


async def main():
    pipeline = create_pipeline(assistant_agent)
    await run_pipeline(pipeline)


if __name__ == "__main__":
    asyncio.run(main())
