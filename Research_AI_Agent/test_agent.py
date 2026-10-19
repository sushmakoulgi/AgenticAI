from agents import research_agent,create_research_plan
import asyncio

async def main():
    user_request="search the web on how to call ollama , give a simple paragraph"

    response=await research_agent(user_request)
    #response=await create_research_plan(user_request=user_request)
    print(response)


asyncio.run(main())