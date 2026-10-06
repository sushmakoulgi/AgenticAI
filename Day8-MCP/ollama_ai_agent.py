from openai import OpenAI
from dotenv import load_dotenv
from mcp_client import *
import os   
import asyncio

load_dotenv()

client=OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))

def generate_tool_description(tools):
    description=""
    for tool in tools:
        description=description+f"""
Tool : {tool.name} Description={tool.description}"""
    return description

async def plan_tool(user_input,mcp_client):
    
    tools=await discover_tools(mcp_client)
    tool_description=generate_tool_description(tools)
    prompt=f"""you are an AI Planner
    here are tools and their description available {tool_description}
    choose the right tool and return only tool_name, here is the user request {user_input}"""
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    print("\nAssistant:", response.choices[0].message.content)
    return response.choices[0].message.content


async def main():
    user_input=input("User:")
    mcp_client =await connect()
    tool_name=await plan_tool(user_input,mcp_client)
    print(f"Choosen Tool Name {tool_name}")
    choosen_tool_name=await plan_tool(user_input,mcp_client)
    result=await execute_tool(mcp_client=mcp_client,tool=choosen_tool_name,args=None)
    print("choosen_tool_name",choosen_tool_name)
    print("result ",result.content[0].text)

    prompt=f""" you are an AI agent and here is the 
      User  question is {user_input} and result is {result} , return result in complete sentence"""

    response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    
    print("\nAssistant:", response.choices[0].message.content)
    await disconnect(mcp_client)




asyncio.run(main())