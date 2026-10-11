
import asyncio
from mcp_client import connect,discover_tools,disconnect
from agent.agent_loop import run_agent_loop
from memory import create_database

def generate_tool_description(tools):
    description=""
    for tool in tools:
        description=description+f""" Tool : {tool.name} Description={tool.description}"""
    return description


async def main():
    #connect to mcpclient
    create_database()
    client=await connect()
    #get the tools
    tools=await discover_tools(client)
    tools_description=generate_tool_description(tools)
    #get the userrequest
    user_request=input("User:")
    #call agent_loop to execute
    await run_agent_loop(user_request,tools_description,client)
    #print the final answer from state
    #close the mcpclient
    await disconnect(client)
    pass


asyncio.run(main())