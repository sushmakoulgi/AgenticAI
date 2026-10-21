from model import model,model_with_tools
from prompt import prompt
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_agent
from tools import roll_dice,generate_password,get_current_timestamp
from mcp_tools import client
import asyncio

async def main():

    # tools=[
    #     roll_dice,
    #     get_current_timestamp,
    #     generate_password
    # ]

    tools= await client.get_tools()

    messages=prompt.invoke({
    "request":"whats the weather in boston"
    })

    # response=model.invoke(messages)
    # parser=StrOutputParser()
    # chain=prompt|model|parser
    # response=chain.invoke(
    #     {
    #  "request":"what is 1+2"
    #  }
    # )
    # print(response)

    #reponse = model_with_tools.invoke("whats the current time?")

    agent=create_agent(
        model=model,
        tools=tools,
        system_prompt="you are an AI agent"
    )
    response=await agent.ainvoke(
        {
            "messages":[{
                "role":"user",
                "content":"what is current time?"
            }]
        }
    )


    for block in response['messages']:
        print("="*30)
        print(block)
        print("="*30)

    print(response['messages'][-1].content)



asyncio.run(main())