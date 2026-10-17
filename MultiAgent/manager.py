from research_agent import research
from coding_agent import code_task
from reviewer_agent import review_code
from state import create_state
from Claude_connector import ClaudeConnector
import json

MAX_REVISION=3

async def run_manager(task):
    state=create_state(task)

    while True:
        worker=await choose_worker(state)
        print(worker)
        res_result=""
        action=""
        if worker=="Research":
            res_result=await research(state["task"])
            state["research"]=res_result
        elif worker=="Code":
            feedback=""
            print(state["revision_count"])
            if state["revision_count"] >= MAX_REVISION:
                break
            if state["review"] != "":
                dict=json.loads(state["review"])
                print(dict)
                feedback=dict.get("feedback","")

            code_result=await code_task(state["task"],state["research"],feedback)
            state["code"]=code_result
            state["revision_count"]+=1
                    
        elif worker=="Review":
            review_result=await review_code(state["task"],state["code"])
            state["review"]=review_result
        elif worker=="Finish":
            break
        else:
            raise ValueError("Invalid Woker")
        
        state["history"].append(worker)
        
        # print("Manager selected ",worker)
        # research_result=await research(task)
        # print("Research ---> code Agent")
        # code_result=await code_task(task,research_result)
        # print("Code agent--> reviewer")
        # review_result=await review_code(task,code_result)

    return {
        "research":state["research"],
        "code":state["code"],
        "review":state["review"]
    }


async def choose_worker(state):
    prompt=f""" you are AI agent Manager, your job is to choose 
    next  agent to execute for given 
    task: {state["task"]} research: {state["research"]} , code: {state["code"]}
    code review :{state["review"]} and here is the history of whats completed
    {state["history"]}
    current revision {state["revision_count"]} and max_revisions allowed is {MAX_REVISION}
    Available Workers:
    Research
    Code 
    Review

    if revision count >=  max_revisions allowed then return Finish
 if you need research  and research is empty or insuffiecient then choose Research agent,
   if research is complete and code is empty, then choose Code Agent 
   if code is not well written then choose the Review agent,
   if review agent status says Needs_Revision then send it to Code agent to revise else send Finish
  if research, code and review are complete then choose Finish when research , code and review are complete
   return only one of these exact  words 
   Research, Code, Review, Finish 
   """

    claude_connector=await ClaudeConnector.Create()
    response=await claude_connector.generate_response(prompt)
    return response