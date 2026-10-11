def create_state(user_request:str,max_step=5):
    return {
        "user_request":user_request,
        "max_steps":max_step,
        "current_step":0,
        "actions":[],
        "observations":[],
        "finished":False,
        "final_answer":"",
        "tasks":[],
        "memory":[],
        "current_task":None,
        "results":[]

    }

def add_task(state,task):
    state["tasks"].append(
        {
            "task":task,
            "status":"pending"
        }
    )

def complete_task(state,task):
    for t in state["tasks"]:
        if t==task:
            t["status"]="completed"
            return

def add_action(state,action):
    state["actions"].append(action)

def record_observations(state, action,observation):
    state["observations"].append(
        {
            "step":state["current_step"],
            "action":action,
            "observation":observation
        }
    )

def add_result(state,result):
    state["results"].append(result)

def get_pending_task(state):
    return [item["task"] for item in state["tasks"] if item["status"]=="pending"]

def all_tasks_completed(state):
    return all( item["task"]=="completed" for item in state["tasks"] )

def next_step(state):
    state["current_step"]+=1

def can_continue(state):
    return (not state["finished"] and state["current_step"]<state["max_steps"])

def finish(state,answer):
    state["final_answer"]=answer
    state["finished"]=True

def add_memory(state,memory):
    state["memory"].append(memory)