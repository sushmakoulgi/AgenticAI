from crewai import Crew,Process
from agents import researcher,coder,reviewer
from tasks import research_task,reviewer_task,coding_task,memory_task
from llm import claude_manager_llm
import os
from dotenv import load_dotenv

load_dotenv()
embedding_key=os.getenv("VOYAGE_API_KEY")

embedding_config={
        "provider": "voyageai",
        "config": {
            "model": "voyage-3.5",  # Or voyage-3-large, voyage-code-3, etc.
            "api_key": embedding_key # Or set the VOYAGE_API_KEY environment variable
        }
    }
crew=Crew(
    agents=[researcher,coder,reviewer],
    tasks=[research_task,coding_task,reviewer_task],
    process=Process.hierarchical,
    manager_llm=claude_manager_llm,
    memory=True,
    embedder=embedding_config,
    verbose=True
)

memory_crew=Crew(
    agents=[researcher],
    tasks=[memory_task],
    manager_llm=claude_manager_llm,
    memory=True,
    embedder=embedding_config
)