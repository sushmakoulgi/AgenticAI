import os
import asyncio
from agent.Claude_connector import ClaudeConnector



async def decompose_task(user_request) -> list[str]:
        tasks=[]
        claudeConnector=await ClaudeConnector.Create()
        prompt=f"""
        you are an AI Task planner. Break the user request into small tasks
        Rules: 
        1. Create only the tasks necessary to complete the user request .
        2.Put the tasks into correct execution order.
        3.Each task should be a short action
        4. Return one task per line
        5.do not number the tasks
        6.Do not explain anything
        CRITICAL RULE:

Return NO tasks (or "None") if the user request belongs to any of the following categories:
   1. Greetings or casual conversation (e.g., "hi", "hello", "how are you?")
   2. Introductions or personal details (e.g., "my name is Pankaj", "I live in Delhi")
   3. Memory questions about past interactions (e.g., "what is my name?", "what did we discuss earlier?")
   4. General knowledge/Q&A questions that can be answered directly without tools (e.g., "what is Machine Learning?", "explain gravity")


        here is the user_request  {user_request}
         """
         
        response=await claudeConnector.generate_response(prompt=prompt,system="you are an AI task planner")
        await claudeConnector.close()
        if response:
            for line in response.splitlines():
                tasks.append(line)
        return tasks


        
# asyncio.run(
#  decompose_task("get me the today's date and generate password for 10 character and roll the dice"))