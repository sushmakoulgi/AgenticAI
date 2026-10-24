from langchain_anthropic import ChatAnthropic
import os
from dotenv import load_dotenv



load_dotenv()
key=os.getenv("ANTHROPIC_API_KEY","")
llm_model=os.getenv("LLM_MODEL","")

model=ChatAnthropic(
    model_name=llm_model,
    max_tokens_to_sample=1024,
    api_key=key,
    timeout=10,
    stop=[]
)

#model_with_tools=model.bind_tools(tools)