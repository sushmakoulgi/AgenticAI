from crew import crew,memory_crew
import asyncio

async def main():
    result=await crew.kickoff_async()

    print(result)
    result1=await memory_crew.kickoff_async()
    print(result1)


asyncio.run(main())