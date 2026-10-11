from agent.agent_state import *
from agent.task_planner import decompose_task
from agent.planner import planner
from agent.executor import execute_action
from agent.Claude_connector import ClaudeConnector
from memory import search_semantic_memories,save_memory,save_semantic_memory
from memory_extracter import extract_memory

async def run_agent_loop(userrequest,tools,client):
    #create a agentstate
    state=create_state(user_request=userrequest)
    memories=search_semantic_memories(userrequest)

    for memory in memories:
        add_memory(state,memory=memory)

    tasks=await decompose_task(user_request=userrequest)
    print("list of tasks from task decomposer",tasks)
    
    for task in tasks:
        add_task(state,task)


    #while the goal is not achieved,
    while can_continue(state):

        #send it planner to get the tasks and actions
        next_action=await planner(state,userrequest,tools=tools)
        print("next-action is ",next_action)
        if next_action:
            #if we get Finish, then send the agent state, answer to 
            if next_action =="Finish":
                
                break
            #if we get valid task and action
            (task,action)=next_action.split(":")
            print(next_action)
            add_action(state,action=action)
            #send it to mcp_client to execute the action
            result=await execute_action(state,action,client)
            print("result",result)
            #store the retult in agent state
            add_result(state,result)
            complete_task(state,task)
            record_observations(state,action,observation=result)
            next_step(state)

    result_prompt=f"""
    this is my user request {userrequest}
    these were the tasks performed {state["tasks"]}
    actions executed {state["actions"]} 
    here are the intermediate results {state["results"]}
    and all the observation per tasks {state["observations"]}
    these are the tools used {tools}
    use the relevant memories {state["memory"]} to generate answer when applicable
    Generate user friendly answer  using all the above infromation 
    give it one line after composing all the results {state["results"]}
    do not mention any details on how the answers was produced using state , tasks, observations
    just the final asnwer"""
    
    claudeConnector=await ClaudeConnector.Create()
      #ai agent to format it. 
    finalanswer=await claudeConnector.generate_response(result_prompt)
    finish(state,finalanswer) #TODO
    save_memory(user_request=userrequest,assistant_response=finalanswer)
    memory=await extract_memory(user_message=userrequest,assistant_message=finalanswer)
    print(memory)
    if memory !="None":
        print("saving semantic memory")
        save_semantic_memory(memory)
    else:
        print("not saving semantic memory")
    await claudeConnector.close()
    print(finalanswer)
  

  
