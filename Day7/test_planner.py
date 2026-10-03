from planner import choose_tool
from claude_planner import choose_tool_by_claude
import asyncio
# print(choose_tool("get me time"))

# print(choose_tool("whats the weather"))

# print(choose_tool("roll me a dice"))

async def test():
    print(await choose_tool_by_claude("whats the time?"))

    print(await choose_tool_by_claude("roll me a dice"))

asyncio.run(test())