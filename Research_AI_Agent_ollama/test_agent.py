from agents import research_agent,create_research_plan
import asyncio
from tools import generate_report,get_verified_research_notes
async def main():
    user_request="search the web on how to call ollama , give a simple paragraph"

    response=await research_agent(user_request)
    #response=await create_research_plan(user_request=user_request)
    print(response)

    notes=get_verified_research_notes()

    response=await generate_report(user_request=user_request,verified_findings=notes)

    print(response)

asyncio.run(main())
