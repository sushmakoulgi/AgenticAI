
import os
import asyncio
from anthropic import AsyncAnthropic, DefaultAioHttpClient
from dotenv import load_dotenv

load_dotenv()

class ClaudeConnector:

    def connect(self, value=None):

        self.client= AsyncAnthropic(
                api_key=os.environ.get("ANTHROPIC_API_KEY"),
                http_client=DefaultAioHttpClient(),
            )
        return self.client

    async def generate_response(self, prompt, system="you are an AI agent")->None|str:
        self.client=self.connect()
        response=None
        message = await self.client.messages.create(
                        max_tokens=1024,
                        system=system,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        model="claude-opus-5-5",
                    )
        for block in message.content:
            if block.type == "text":
                response= block.text

        await self.close()
        return response


    async def close(self):
        await self.client.close()