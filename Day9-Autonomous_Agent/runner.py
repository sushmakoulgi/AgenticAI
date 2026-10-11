from mcp_client import discover_tools,connect,disconnect
from Agent.agent_loop import run_agent_loop
from Agent.planner import planner
from Agent.executor import execute_action
from Agent.agent_state import *
from dotenv import load_dotenv
from openai import OpenAI
import os
import asyncio

load_dotenv()

client=OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))

def format_answer(state):
    prompt=f"""
User has asked {state["user_request"]}
actions performed {state["actions"]} 
observations {state["observation"]}
Answer the user natuarally do not mention internal state details do not mention tools"""
    response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
    )

    return response.choices[0].message.content.strip()




async def main():
    mcp_client=await connect()
    tools=await discover_tools(mcp_client=mcp_client)
    user_request=input("User:\n")

    state=await run_agent_loop(user_request, planner, execute_action,format_answer,tools, mcp_client)

    print(state["final_answer"])
    await disconnect(mcp_client)


asyncio.run(main())