import os
from ollama import AsyncClient
from dotenv import load_dotenv

load_dotenv()

class OllamaLLM:

    def __init__(self, model=None):
        self.client = None
        self.model = model or os.environ.get("OLLAMA_MODEL", "qwen3:4b")

    def connect(self):
        # Reuse one client so its http session can be closed cleanly
        if self.client is None:
            self.client = AsyncClient(
                host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
            )
        return self.client

    async def generate_raw_response(self, messages, system="you are an AI agent", tools=None, format=None):
        client = self.connect()

        # Ollama has no separate system param; it goes in as the first message
        api_kwargs = {
                "model":self.model,
                "messages":[{"role":"system","content":system}] + messages,
                # qwen3 always reasons first; think=True keeps that in message.thinking instead of content
                "think":True,
                "options":{"num_predict":4096},
            }

        # Conditionally inject tools / output schema only if provided
        if tools:
            api_kwargs["tools"] = tools
        if format:
            api_kwargs["format"] = format
        message = await client.chat(
                       **api_kwargs
                    )
        return message


    async def close(self):
        if self.client is not None:
            await self.client.close()
            self.client = None
