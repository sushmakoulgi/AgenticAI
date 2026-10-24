from model import model
from langchain.agents import create_agent
from tenacity import retry,wait_exponential,stop_after_attempt
import asyncio
from fastapi import HTTPException
from schemas import ChatResponse


agent=create_agent(
    model=model,
    tools=[]
)



@retry(stop=stop_after_attempt(2),wait=wait_exponential(multiplier=1,min=1,max=4))
async def run_agent(request):
    try:
        response=await asyncio.wait_for(agent.ainvoke(
            {
            "messages":[{
                "role":"user",
                "content":request
            }]
            }
        ),timeout=30)

        return ChatResponse(
                answer=response["messages"][-1].content)
    except asyncio.TimeoutError as te:
        raise HTTPException(
            status_code=504,
            detail="request timed out"
        )
    except Exception as exc:
        print(f"Agent Execution Failed",exc)
        raise HTTPException(
            status_code=500,
            detail="Agent Execution Failed"
        )