import os
import asyncio
from anthropic import AsyncAnthropic, DefaultAioHttpClient
from dotenv import load_dotenv
from tool_manager import decide_tool

load_dotenv()

async def main() -> None:
    print("Welcome to the AI Assistant! Type 'exit' or 'quit' to end the conversation.")
    roles={
        "1": "You are a motivational Teacher. Explain concepts in simple language and with real-world examples.",
        "2": "You are a friendly AI Teacher. Explain concepts in simple language and with real-world examples.",
        "3": "You are a helpful assistant. Provide concise and accurate answers to user queries.",
        "4": "You are a creative storyteller. Generate engaging and imaginative stories"
    }
    print("Select a role for the AI Assistant:")
    role_choice = input("1. Motivational Teacher\n2. Friendly AI Teacher\n3. Helpful Assistant\n4. Creative Storyteller\nEnter the number of your choice: ")
    system_prompt = roles.get(role_choice, roles["1"])  # Default to Motivational
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
                tool=decide_tool(user_input.lower())
                if tool is not None:
                    print("AI:",tool)
                    continue
                message = await client.messages.create(
                    max_tokens=1024,
                    system=system_prompt,
                    messages=messages,
                    model="claude-opus-5-5",
                )
               
                messages.append({"role": "assistant", "content": message.content})
                for block in message.content:
                    if block.type == "text":
                        print(block.text)


asyncio.run(main())