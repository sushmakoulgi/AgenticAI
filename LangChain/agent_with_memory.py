from model import model
from langchain.agents import create_agent
from mcp_tools import client
from retriever import retriever
from langchain_core.tools import tool
from mcp_tools import client
import asyncio


@tool
async def search_context(request):
    """
    for any request  on MCP related questions, returns the top results from 
    notes"""
    response=await retriever.ainvoke(request)
    return response

async def main():
    tools=await client.get_tools()
    tools.append(search_context)

    agent=create_agent(
        model=model,
        tools=tools
    )
    request=input("\n user:")
    messages=[]
    while request != "quit":
        
        messages.append({
            "role":"user",
            "content":request
        })

        response=await agent.ainvoke(
                {
                    "messages":messages
                }
            )

        print("AI Assistant:",response['messages'][-1].content)

        messages.append({
            "role":"assistant",
            "content":response['messages'][-1].content
                            })
        request=input("\n user:")

asyncio.run(main())

