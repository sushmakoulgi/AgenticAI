from memory_extracter import extract_memory
import asyncio

async def test():
    memory=await extract_memory(
    user_message="I am learning AI agent Course",
    assistant_message="Great, let me know if you need help with that"
)

    print(memory)

    memory=await extract_memory(
        user_message="what 5+2",
        assistant_message="7"
    )
    
    print(memory)
    

asyncio.run(test())