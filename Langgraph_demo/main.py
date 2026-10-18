import asyncio
from mcp_client import connect,disconnect,discover_tools
from agent_state import AgentState
from graph import build_graph
from langgraph.types import Command

async def main():
    client=await connect()
    tools=await discover_tools(client)
    for tool in tools:
        print(tool.name, tool.description)

    graph=await build_graph(tools,client)
    user_request=input("User:")
    initial_state=AgentState(
        user_request=user_request,
        current_step=0,
        max_steps=5,
        actions=[],
        approval="",
        observations=[],
        final_answer="",
        finished=False,
        action=""
    )
    config= {
        "configurable":{
            "thread_id":"demo-1"
        }
    }
    result=await graph.ainvoke(initial_state,config)

    while True:
        interrupts=result.get(
        "__interrupt__"
    )
        if not interrupts:
            break
        if interrupts:
            interrupt_data=interrupts[0].value
            print("==================")
            print("Human approval Needed")
            print("===================")

            print(interrupt_data["message"])
            print("tool",interrupt_data["action"])
            user_input =input("Yes/no ?").strip().lower()
        result=await graph.ainvoke(Command(resume=user_input),config)


    print("result",result)
    await disconnect(client)

if __name__=="__main__":
    asyncio.run(main())
