from agent.task_planner import decompose_task
from agent.agent_state import add_task
from agent.Claude_connector import ClaudeConnector

async def planner(state,user_request, tools):
    #call task_plnner with user request 
    #task_planner will give list of tasks
    #add it to agent state.
    #create a prompt to generate task and action from task's
    #planners response.
    #return one task, tool based on the completed actions
  

    prompt=f""" you are an AI planner.
    here is the user_request {user_request}
    and here are the tasks needed to complete the user request
    1. pick pending tasks {state["tasks"]} from agent state {state}
    2. check the completed tasks, actions {state["actions"]}
    3. check the observations {state["observations"]}
    3.1 here are the relevant previous memory {state["memory"]}  
    4. return the next task and action to execute using tools {tools}
    4.1. if the tasks fails, then reconsider the plan
    4.2: If the request can be answered using previous memory/ standard knowledge, 
    or if the tasks is None then return "Finish" (no need to include in the format for Task:Action)
    4.3 never output None
5. only return the one eligible "Task:Action
 6. if all tasks are completed, thenr return Finish"""

    claudeConnector=await ClaudeConnector.Create()
    response=await claudeConnector.generate_response(prompt=prompt,system="you are an AI planner")
    await claudeConnector.close()
    print("Planner generated ",response)
    return response



