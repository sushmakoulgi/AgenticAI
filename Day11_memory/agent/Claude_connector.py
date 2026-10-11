

from typing_extensions import Self
import os
import asyncio
from anthropic import AsyncAnthropic, DefaultAioHttpClient
from dotenv import load_dotenv

load_dotenv()

class ClaudeConnector:
    _instance=None
    _lock=asyncio.Lock()


    @classmethod
    async def Create(cls):
        if cls._instance is not None:
            return cls._instance
        async with cls._lock:
            if cls._instance is None:
                self=cls()
                
                cls._instance=self

        return cls._instance

    

    def connect(self, value=None):

        self.client= AsyncAnthropic(
                api_key=os.environ.get("ANTHROPIC_API_KEY"),
                http_client=DefaultAioHttpClient(),
            )
        return self.client

    async def generate_response(self, prompt, system="you are an AI agent")->None|str:
        try:
            self.client=self.connect()
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
                    print(block.text)
                    return block.text
            return None
        except Exception as e:
            print(e)
        finally:
            await self.close()
           



    async def close(self):
        await self.client.close()