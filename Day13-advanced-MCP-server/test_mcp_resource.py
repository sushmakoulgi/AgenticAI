from fastmcp import Client
import pathlib
import asyncio


async def connect():
    mcp_client=Client("weather_mcp_server/mcp_server.py")
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

async def discover_resources(mcp_client:Client):
    resources=await mcp_client.list_resources()
    for resource in resources:
        print(f" resource is {resource.uri} description :{resource.description}")
        content=await mcp_client.read_resource(resource.uri)
        print(content)


async def execute_tool(mcp_client:Client, tool,args):
    if args is None:
        args= {}
    result=await mcp_client.call_tool(tool,arguments=args)
    return result

async def main():
    client=await connect()
    await discover_resources(client)
    await disconnect(client=client)


asyncio.run(main())

    
              
    
    
