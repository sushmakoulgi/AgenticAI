import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client=OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))

def generate_tool_description(tools):
    description=""
    for tool in tools:
        description=description+f""" Tool : {tool.name} Description={tool.description}"""
    return description



def planner(state,tools):
    planner_prompt = f"""
    You are an AI planner.
    your job is to only decide next action 
    user request:{state["user_request"]} 
    completedactions={state["actions"]}
    previous_observation={state["observation"]}
available tools ={generate_tool_description(tools)}

Rules:
1. Choose only one action
2. if user's request is completely satisfied, return 'FINISH'
3. Never repeat  an action that has been already completed,
4. Use the observations to decide whats till is required
5.return only tool name or "FINISH"
6.Do not explain your answers NextAction:"

 """

    response=client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {"role": "system", "content": "You are a AI planner."},
            {"role": "user", "content": planner_prompt}
        ]
    )

    return response.choices[0].message.content