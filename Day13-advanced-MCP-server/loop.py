from state import *
from task_planner import decompose_task
from planner import planner
from executor import execute_action
from Claude_connector import ClaudeConnector

def build_tool_description(tools):
    description=""
    for tool in tools:
        description+=f"tool name: {tool.name} description: {tool.description} input schema: {tool.input_schema}"
    return description


async def run_agent_loop(userrequest,tools,tools_registry):
    #create a agentstate
    tool_description=build_tool_description(tools=tools)
    state=create_state(user_request=userrequest)
    tasks=await decompose_task(user_request=userrequest,tooldescription=tool_description)
    print("list of tasks from task decomposer",tasks)
    
    for task in tasks:
        add_task(state,task)


    #while the goal is not achieved,
    while can_continue(state):

        #send it planner to get the tasks and actions
        next_action=await planner(state,userrequest,tool_description=tool_description)
        print("next-action is ",next_action)
        if next_action:
            #if we get Finish, then send the agent state, answer to 
            if next_action["tool"] =="Finish":
                
                break
            #if we get valid task and action
            task=next_action["task"]
            # executor needs both "tool" and "arguements", so pass the whole dict
            action=next_action
            print(next_action)
            add_action(state,action=action)
            #send it to mcp_client to execute the action
            result=await execute_action(state,action,tool_registry=tools_registry)
            print("result",result)
            #store the retult in agent state
            add_result(state,result)
            complete_task(state,task)
            record_observations(state,action,observation=result)
            next_step(state)
        else:
            # count the failed plan as a step so max_steps still stops the loop
            next_step(state)

    result_prompt=f"""
    this is my user request {userrequest}
    these were the tasks performed {state["tasks"]}
    actions executed {state["actions"]} 
    here are the intermediate results {state["results"]}
    and all the observation per tasks {state["observations"]}
    these are the tools used {tools}
    Generate user friendly answer  using all the above infromation 
    give it one line after composing all the results {state["results"]}
    do not mention any details on how the answers was produced using state , tasks, observations
    just the final asnwer"""
    
    claudeConnector=await ClaudeConnector.Create()
      #ai agent to format it. 
    finalanswer=await claudeConnector.generate_response(result_prompt)
    finish(state,finalanswer) #TODO
    await claudeConnector.close()
    print(finalanswer)
  

  
