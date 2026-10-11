from mcp_client import execute_tool

async def execute_action(state,action,client):
    result=await execute_tool(client,action,None)

    if hasattr(result,"content"):
        if len(result.content)>0:
            return str(result.content[0].text)