import asyncio
from mcp_client import connect,disconnect,discover_tools,execute_tool
from crewai.tools import tool

async def call_mcp_get_current_date_time():
    try:
        client=await connect()
        result=await execute_tool(client,"get_current_date_time",None)
        return result.content[0].text
    finally:
        await disconnect(client)

@tool("MCP Current Time")
async def mcp_current_time():
    """ Gets the Current Time"""
    return await call_mcp_get_current_date_time()