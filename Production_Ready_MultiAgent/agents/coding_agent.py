from utils.llm import ClaudeConnector

async def code_task(task,research,feedback=""):
    prompt=f"""You are an AI code Generator, 
    your job is to generate  code  sample for the given reasearch 
     {research} and task {task} and previous feedback {feedback} return 1. short explaination
     2. Complete code sample in python 
     3. if the feedback is present then correct the code based on the previous feedback"""

    claude_connector=ClaudeConnector()
    response=await claude_connector.generate_response(prompt=prompt,system="You are an AI Researcher")
    return response