
import asyncio
from mcp_client import connect,discover_tools,disconnect
from loop import run_agent_loop
from mcp_manager import create_tool_registry

def generate_tool_description(tools):
    description=""
    for tool in tools:
        description=description+f""" Tool : {tool.name} Description={tool.description}"""
    return description


async def main():
    #connect to mcpclient
    from mcp_manager import create_tool_registry,close_servers,run_tool

    servers=[
        "time_mcp_server/mcp_server.py",
        "weather_mcp_server/mcp_server.py"
    ]

    clients,registry=await create_tool_registry(servers=servers)
    tools=[]
    for entry in registry.values():
        tools.append(entry["tool"])

    
    #get the tools
    
    #get the userrequest
    user_request=input("User:")
    #call agent_loop to execute
    await run_agent_loop(user_request,tools,registry)
    #print the final answer from state
    #close the mcpclient
    await close_servers(clients)
    pass


asyncio.run(main())