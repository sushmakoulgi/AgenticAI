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
        while True:
            user_input = input("\nUser: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            message = await client.messages.create(
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                model="claude-opus-5-5",
            )
            for block in message.content:
                if block.type == "text":
                    print(block.text)


asyncio.run(main())