import asyncio
from My_Agents import assistant_agent_dansk
from Pipeline import create_pipeline, run_pipeline


async def main():
    pipeline = create_pipeline(assistant_agent_dansk)
    await run_pipeline(pipeline)


if __name__ == "__main__":
    asyncio.run(main())
