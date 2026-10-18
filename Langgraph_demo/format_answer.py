from agent_state import AgentState
from claude_connector import ClaudeConnector

async def format_answer(state:AgentState):
    result_prompt=f"""
        this is my user request {state['user_request']}
        actions executed {state["actions"]} 
        and all the observation per tasks {state["observations"]}
        Generate user friendly answer  using all the above infromation 
        give it one line after composing all the results {state["observations"]}
        do not mention any details on how the answers was produced using state , tasks, observations
        just the final asnwer"""
        
    claudeConnector= ClaudeConnector()
          #ai agent to format it. 
    finalanswer=await claudeConnector.generate_response(result_prompt)
    state["final_answer"]=finalanswer if finalanswer else ""
    state["finished"]=True
    print(finalanswer)
    return state