from dotenv import load_dotenv
import os
load_dotenv()

class Settings:
    ANTHROPIC_API_KEY:str=str(os.environ.get("ANTHROPIC_API_KEY"))
    LLM_MODEL=os.environ.get("LLM_MODEL","claude-opus-5-5")
    MAX_RETRIES=3
    TIMEOUT_IN_SEC=2
    MAX_REVISION=3
