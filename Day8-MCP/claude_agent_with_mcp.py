import os
import asyncio
from anthropic import AsyncAnthropic, DefaultAioHttpClient
from dotenv import load_dotenv
from mcp_client import *

load_dotenv()


def generate_tool_description(tools):
    description=""
    for tool in tools:
        description=description+ f""" Tool: {tool.name} 
        Description: {tool.description}"""
    return description


async def plan_and_get_prompt(mcp_client, user_input):
    tools=await discover_tools(mcp_client=mcp_client)
    tool_description=generate_tool_description(tools)
    planner_prompt=f"""
you are an AI PLanner and here are my tools and their descrioption
{tool_description}. and user question is {user_input} find
the appropriate tool and return toolname only"""
    return planner_prompt
    




async def main() -> None:
    async with AsyncAnthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
        http_client=DefaultAioHttpClient(),
    ) as client:
        mcp_client=await connect()
        while True:
            user_input = input("\nUser: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            planner_prompt=await plan_and_get_prompt(mcp_client=mcp_client,user_input=user_input)
            tool_name=""
            message = await client.messages.create(
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": planner_prompt
                    }
                ],
                model="claude-opus-5-5",
            )
            for block in message.content:
                if block.type == "text":
                    tool_name=block.text
                    print("choosen tool ",block.text)

            tool_result=await execute_tool(mcp_client,tool_name,None)
            print("tool result ",tool_result.content[0].text)

            llm_prompt=f"""you are an AI agent, here is user question{user_input }. and result is {tool_result.content[0].text}
reply with detailed one liner answer"""
            message = await client.messages.create(
                            max_tokens=1024,
                            messages=[
                                {
                                    "role": "user",
                                    "content": llm_prompt
                                }
                            ],
                            model="claude-opus-5-5",
                        )
            for block in message.content:
                if block.type == "text":
                    print("Assistant: ",block.text)


asyncio.run(main())