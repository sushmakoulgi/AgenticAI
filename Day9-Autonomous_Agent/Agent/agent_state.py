def create_state(user_request:str,max_step=5):
    return {
        "user_request":user_request,
        "max_steps":max_step,
        "current_step":0,
        "actions":[],
        "observation":[],
        "finished":False,
        "final_answer":""

    }

def add_action(state,action):
    state["actions"].append(action)


def record_observations(state, action, result):
    state["observation"].append(
        {
            "action":action,
            "observation":result,
            "step":state["current_step"]
        }
    )

def can_continue(state):
    if state["finished"]==True or state["current_step"] >= state["max_steps"]:
        return False
    return True

def next_step(state):
    state["current_step"]+=1

def finish(state,answer):
    state["finished"]=True
    state["final_answer"]=answer