from Claude_connector import ClaudeConnector

async def research(task):
    prompt=f"""You are an AI researcher, 
    your job is to research following {task}
provide 1.Important Concepts
2. Key facts
3. Relevant Examples
Keep the answer Concise  and useful for another AI Agent """

    claude_connector=await ClaudeConnector.Create()
    response=await claude_connector.generate_response(prompt=prompt,system="You are an AI Researcher")
    return response