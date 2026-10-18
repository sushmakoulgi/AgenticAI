from langgraph.graph import START,END,StateGraph
from langgraph.types import interrupt,Command
from langgraph.checkpoint.memory  import InMemorySaver
from planner import planner
from agent_state import AgentState
from executor import execute_action
from format_answer import format_answer

async def create_planner_node(tools):

    async def planner_node(state:AgentState):
        action=await planner(state,tools) 
        print("planner selected action ",action)
        return {
            "actions":state["actions"],
            "observations":state["observations"],
            "finished": state["finished"]==True,
            "final_answer":state["final_answer"],
            "current_step":state["current_step"],
            "action":action
                            }
    return planner_node

def route_after_planner(state:AgentState):
    if state["action"]=="Finish":
        return "format_answer"
    return "approval"

async def create_tool_node(client):
    async def tool_node(state:AgentState):
        action=state["action"]
        result=await execute_action(state,action,client)
        print("observations ",result)
        observation={
            "step":state["current_step"],
            "action":state["action"],
            "observation":result
        }
        state["observations"].append(observation)
        state["actions"].append(action)
        state["current_step"]+=1
        return state

    return tool_node

async def route_after_tool(state):
    if state["current_step"] < state["max_steps"]:
        return "continue"
    return "format_answer"


async def format_answer_node(state:AgentState):
        state=await format_answer(state)
        return state

async def approval_node(state:AgentState):
    decision=interrupt(
       value= {
        "message":"Do you want to approve the action",
        "action":state["action"]
        }
    )
    state["approval"]=decision
    return state

async def route_after_approval(state:AgentState):
    if state['approval']=="yes":
        return "yes"
    return "no"

async def build_graph(tools,client):
    checkpointer=InMemorySaver()
    builder=StateGraph(AgentState)
    planner_node=await create_planner_node(tools)
    builder.add_node("planner", planner_node)
    tool_node=await create_tool_node(client)
    builder.add_node("tool",tool_node)
    builder.add_node("format_answer",format_answer_node)
    builder.add_node("approval",approval_node)

    builder.add_edge(START,"planner")

    builder.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "approval":"approval", # this is graph node
            "format_answer":"format_answer"
        })
        
    builder.add_conditional_edges(
        "approval",
        route_after_approval,
        {
            "yes":"tool",
            "no":"format_answer"
        }
    )

    builder.add_conditional_edges(
        "tool",
        route_after_tool,
        {
            "format_answer":"format_answer",
            "continue":"planner"
        }
    )
    builder.add_edge("format_answer",END)

    return builder.compile(checkpointer=checkpointer)


