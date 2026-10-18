
from claude_connector import ClaudeConnector

async def planner(state, tools):
    #call task_plnner with user request 
    #task_planner will give list of tasks
    #add it to agent state.
    #create a prompt to generate task and action from task's
    #planners response.
    #return one task, tool based on the completed actions
  
 
    prompt=f""" you are an AI planner.
    here is the user_request {state["user_request"]}
    here are the tools availabel {tools}
    refer the executed actions {state["actions"]}
    refer the observations {state["observations"]}
    decide the action based on the state {state}
   Rules:
1. Choose only one action
2. if user's request is completely satisfied, return 'Finish'
3. Never repeat  an action that has been already completed,
4. Use the observations to decide whats till is required
5.return only tool name or "Finish"
6.Do not explain your answers NextAction:"""

    claudeConnector=ClaudeConnector()
    response=await claudeConnector.generate_response(prompt=prompt,system="you are an AI planner")
    print("Planner generated ",response)
    return response



