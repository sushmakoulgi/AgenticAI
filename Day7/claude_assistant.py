import os
import asyncio
from anthropic import AsyncAnthropic, DefaultAioHttpClient
from dotenv import load_dotenv
from claude_planner import choose_tool_by_claude
from tools import get_current_timestamp,roll_dice,generate_password

load_dotenv()

async def main() -> None:
    print("Welcome to the AI Assistant! Type 'exit' or 'quit' to end the conversation.")
   
    system_prompt = "You are an AI agent" # Default to Motivational
    async with AsyncAnthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
        http_client=DefaultAioHttpClient(),
    ) as client:
        while True:
            messages = []
            while True:
                user_input = input("\nUser: ")
                if user_input.lower() in ["exit", "quit"]:
                    return
                messages.append({"role": "user", "content": user_input})
                tool=await choose_tool_by_claude(user_input.lower())
                result=None
                if tool=="get_current_timestamp":
                    result=get_current_timestamp()
                if tool=="roll_dice":
                    result=roll_dice()
                if tool=="generate_password":
                    result=generate_password()

                
                user_prompt=f""" user has asked this question {user_input} and here is the
                result {result} , present this to the user in clean format and explaination"""
                message = await client.messages.create(
                    max_tokens=1024,
                    system=system_prompt,
                    messages=[{
                        "role":"user",
                        "content":user_prompt
                    }],
                    model="claude-opus-5-5",
                )
             
                for block in message.content:
                    if block.type == "text":
                        print(block.text)
              
asyncio.run(main())