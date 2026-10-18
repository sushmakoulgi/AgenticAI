from crewai import LLM
from dotenv import load_dotenv
import os
load_dotenv()

claude_llm=LLM(model="claude-opus-5-5",api_key=os.environ.get("ANTHROPIC_API_KEY"))

claude_manager_llm=LLM(model="claude-opus-5-5",api_key=os.environ.get("ANTHROPIC_API_KEY"))