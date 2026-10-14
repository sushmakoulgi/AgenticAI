import asyncio

from mcp_manager import create_tool_registry,close_servers,run_tool

async def main():
    servers={
       # "time_mcp_server/mcp_server.py",
        "http://127.0.0.1:8001/mcp"
    }

    clients,registry=await create_tool_registry(servers=servers)
   # print(registry)
    resposne=await run_tool(registry,"get_weather",{"city":"Boston"})
    await close_servers(clients=clients)
    print(resposne.content[0].text)


asyncio.run(main())