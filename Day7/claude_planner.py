
import os
import asyncio
from anthropic import AsyncAnthropic, DefaultAioHttpClient
from dotenv import load_dotenv


load_dotenv()

async def choose_tool_by_claude(user_input:str):

    #system_prompt="You are an AI planner"
    user_prompt=f"""you are an AI planner, here are my tools ,
    if user asks for time, return get_current_timestamp
    if user asks to roll a dice return roll_dice 
    if user asks for password generation return generate_password if
    nothing matches then return None , here is user question {user_input}"""
    async with AsyncAnthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
        http_client=DefaultAioHttpClient(),
    ) as client:
       
        message = await client.messages.create(
                max_tokens=1024,
                #system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                model="claude-opus-5-5",
            )
        
       
        for block in message.content:
            if block.type == "text":
                print(block.text)
                return block.text
       

 