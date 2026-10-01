import os
import asyncio
from anthropic import AsyncAnthropic, DefaultAioHttpClient
from dotenv import load_dotenv


load_dotenv()

async def main() -> None:
    async with AsyncAnthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
        http_client=DefaultAioHttpClient(),
    ) as client:
        system_prompt = (
            "You are a motivational Teacher. Explain concepts in simple language "
            "and with real-world examples."
        )
        messages = []
        while True:
            user_input = input("\nUser: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            messages.append({"role": "user", "content": user_input})
            message = await client.messages.create(
                max_tokens=1024,
                system=system_prompt,
                messages=messages,
                model="claude-opus-5-5",
            )
            print({"role": "assistant", "content": message.content})
            messages.append({"role": "assistant", "content": message.content})
            for block in message.content:
                if block.type == "text":
                    print(block.text)


asyncio.run(main())