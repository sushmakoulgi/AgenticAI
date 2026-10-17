
import asyncio
from anthropic import AsyncAnthropic, DefaultAioHttpClient
from utils.config import Settings
from utils.logger import logger



class ClaudeConnector:

    def connect(self, value=None):

        self.client= AsyncAnthropic(
                api_key=Settings.ANTHROPIC_API_KEY,
                http_client=DefaultAioHttpClient(),
            )
        return self.client

    async def generate_response(self, prompt, system="you are an AI agent")->None|str:
        response=""
        attempt=0
        self.client=self.connect()
        while(attempt < Settings.MAX_RETRIES):
            try:

                logger.info("LLM Agent Connected")
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
                                model=Settings.LLM_MODEL,
                            )
                for block in message.content:
                    if block.type == "text":
                        response= block.text
                break
            except Exception as e:
                logger.error("Failed to generate the response from LLM")
                attempt=attempt+1
                if attempt >= Settings.MAX_RETRIES:
                    raise RuntimeError(F"Failed to generate response from LLM -- {e}")
                else:
                    wait_time=attempt*Settings.TIMEOUT_IN_SEC
                    await asyncio.sleep(wait_time)
        
           

        await self.close()
        logger.info("LLM agent closed")
                        
        
        return response


    async def close(self):
        await self.client.close()