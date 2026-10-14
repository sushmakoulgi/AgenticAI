import os
import asyncio
from Claude_connector import ClaudeConnector



async def decompose_task(user_request,tooldescription) -> list[str]:
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
        7. check if the tasks can be decomposed using {tooldescription}
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