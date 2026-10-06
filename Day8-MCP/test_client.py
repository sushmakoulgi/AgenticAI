from mcp_client import *
import asyncio


async def main():
    client=await connect()
    print("Connected to MCP Client")
    print("Discovering tools")
    tools=await discover_tools(client)
    print("execting tool")
    await execute_tool(client,tool=tools[0].name,args=None)
    await disconnect(client)
    
asyncio.run(main())
