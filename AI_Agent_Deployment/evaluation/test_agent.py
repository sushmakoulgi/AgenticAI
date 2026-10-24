from model import model
from langchain.agents import create_agent
from tools import get_current_timestamp,generate_password,roll_dice

async def prep_agent():
    tools=[
         roll_dice,
         get_current_timestamp,
         generate_password
     ]
    agent=create_agent(
            model=model,
            tools=tools
        )

    return agent

async def run_agent(request,agent): 
    response=await agent.ainvoke(
        {
            "messages":[{
                "role":"user",
                "content":request
            }]
        }
    )

    return response['messages']
