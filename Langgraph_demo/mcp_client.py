from fastmcp import Client
import pathlib



async def connect():
    mcp_client=Client(pathlib.Path('mcp_server.py'))
    await mcp_client.__aenter__()
    print("Connecting to MCP Server ")
    return mcp_client

async def disconnect(client:Client):
    await client.__aexit__(None,None,None)
    return

async def discover_tools(mcp_client:Client):
    tools=await mcp_client.list_tools()

    for tool in tools:
        print(f" tool-- {tool.name}---{tool.description}")

    return tools

async def execute_tool(mcp_client:Client, tool,args):
    if args is None:
        args= {}
    result=await mcp_client.call_tool(tool,arguments=args)
    return result


    
              
    
    
