import json
from task_planner import decompose_task
from state import add_task
from Claude_connector import ClaudeConnector



async def planner(state,user_request, tool_description):
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
    4. return the next task and action to execute using tools {tool_description}
    4.1. if the tasks fails, then reconsider the plan
5. only return the one eligible "Task:Action
 6. if all tasks are completed, thenr return Finish
 if the action is found then return the result in the following format
 {{
     "tool":"tool_name",
     "task":"task",
     "arguements":{{
     "argument_name":"arguement_value"
               }}
 }} in case of Finish return {{
 "tool":"Finish",
"task":"",
 "arguements":{{}}
 }} Next Action:"""

    claudeConnector=await ClaudeConnector.Create()
    response=await claudeConnector.generate_response(prompt=prompt,system="you are an AI planner")
    await claudeConnector.close()
    print("Planner generated ",response)
    if not response:
        return None
    # Claude returns text (sometimes inside ```json fences), so pull out the JSON object
    start=response.find("{")
    end=response.rfind("}")
    if start==-1 or end==-1:
        return None
    try:
        return json.loads(response[start:end+1])
    except json.JSONDecodeError:
        print("Planner response is not valid JSON")
        return None



