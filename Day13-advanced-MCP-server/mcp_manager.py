from mcp_client import connect,disconnect,discover_tools,execute_tool

async def create_tool_registry(servers:list):
    clients=[]
    tool_registry={}

    for server in servers:
        client=await connect(server)
        print("connecting to ",server)
        clients.append(client)

        tools=await discover_tools(mcp_client=client)
        for tool in tools:
            tool_registry[tool.name]={
            
                    "client":client,
                    "tool":tool
                }

    return clients,tool_registry

async def close_servers(clients):
    for client in clients:
        await disconnect(client=client)


async def run_tool(tool_registry,tool_name,args):
    entry=tool_registry.get(tool_name,None)
    if entry is None:
        raise ValueError( "Invalid tool name")
    tool=entry["tool"]
    client=entry["client"]
    return await execute_tool(client,tool.name,args)