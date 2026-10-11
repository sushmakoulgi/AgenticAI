from Agent.agent_state import create_state,can_continue,finish,record_observations,next_step

async def run_agent_loop(
        user_request, planner, execute_action,format_answer,tools, client
):
    state=create_state(user_request=user_request)
    while can_continue(state):
        action=planner(state,tools)
        print("Planner selected",action)

        if action=="FINISH":
            answer=format_answer(state)
            finish(state,answer)
            break

        answer=await execute_action(state,action,client)
        record_observations(state,action,answer)
        next_step(state)