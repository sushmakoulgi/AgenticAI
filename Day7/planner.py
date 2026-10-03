import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client=OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))

def choose_tool(userinput:str):
    planner_prompt = f"""
    You are an AI planner.
    
    Available tools:
    
    1. get_current_time
       Use when the user asks for the current date or time.
    
    2. roll_dice
       Use when the user asks to roll a dice.
    
    3. generate_password
       Use when the user wants a secure password.
    
    If no tool is required, return:
    
    none
    
    Return ONLY the tool name.
    
    User Request:
    
    {userinput}
    """

    response=client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {"role": "system", "content": "You are a AI planner."},
            {"role": "user", "content": planner_prompt}
        ]
    )

    return response.choices[0].message.content