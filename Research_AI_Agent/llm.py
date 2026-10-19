import os
from anthropic import AsyncAnthropic, DefaultAioHttpClient
from dotenv import load_dotenv

load_dotenv()

class ClaudeLLM:

    def __init__(self):
        self.client = None

    def connect(self):
        # Reuse one client so its aiohttp session can be closed cleanly
        if self.client is None:
            self.client = AsyncAnthropic(
                api_key=os.environ.get("ANTHROPIC_API_KEY"),
                http_client=DefaultAioHttpClient(),
            )
        return self.client

    async def generate_raw_response(self, messages, system="you are an AI agent", tools=None):
        client = self.connect()
        
        api_kwargs = {
                "max_tokens":1024,
                "system":system,
                "messages":messages,
                "model":"claude-opus-5-5",
            }

            # 2. Conditionally inject tools only if the list is not empty
        if tools:
            api_kwargs["tools"] = tools
        message = await client.messages.create(
                       **api_kwargs
                    )
        return message


    async def close(self):
        if self.client is not None:
            await self.client.close()
            self.client = None
