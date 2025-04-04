import asyncio
from My_Agents import sage_dk_agent
from Pipeline import create_pipeline, run_pipeline


async def main():
    pipeline = create_pipeline(sage_dk_agent)
    await run_pipeline(pipeline)


if __name__ == "__main__":
    asyncio.run(main())
