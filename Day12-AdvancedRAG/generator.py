from claude_connector import ClaudeConnector

async def generate_answer(query,results):
    context="\n\n".join(result["text"] for result in results)

    prompt=f"""
        Answer the question only using provided context 
        {context} userquestion:{query}
Rules: use only provided context, do not invent  information, 
if the answer is not present thensay information is not available 
4.give a clear and concise answer"""

    claude_connector=await ClaudeConnector.Create()
    response=await claude_connector.generate_response(prompt=prompt,system="you are an AI agent")
    return response