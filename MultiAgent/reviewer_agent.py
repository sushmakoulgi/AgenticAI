from Claude_connector import ClaudeConnector
import json
async def review_code(task,code):
    prompt=f"""You are an AI code reviewer, 
    your job is to review the given  code {code} for the 
      task {task}  perform following things
1.check the correctness
2. invalid python syntax, 
3. any improvements
4. logic 
provide the response in structured json, 
return the output in the following format.
{{"status":"Approved" or " Needs_Revision ",
"feedback":""}} - a proper json string only
Add the feedback - a one liner review about what needs to be improved else solution is correct 
only return the json response"""

    claude_connector=await ClaudeConnector.Create()
    response=await claude_connector.generate_response(prompt=prompt,system="You are an AI code reviewer")
    print("response ",response)
    if not response:
        return ""
    # Claude often wraps the JSON in ```json fences, so keep only the {...} part
    start=response.find("{")
    end=response.rfind("}")
    if start==-1 or end==-1:
        return ""
    review=response[start:end+1]
    try:
        json.loads(review)
    except json.JSONDecodeError:
        print("Reviewer response is not valid JSON")
        return ""
    return review