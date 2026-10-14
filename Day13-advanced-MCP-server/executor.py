from mcp_manager import run_tool

async def execute_action(state,action,tool_registry):
    result=await run_tool(tool_registry,action["tool"],action["arguements"])

    if hasattr(result,"content"):
        if len(result.content)>0:
            return str(result.content[0].text)