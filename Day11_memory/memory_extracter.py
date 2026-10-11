from agent.Claude_connector import ClaudeConnector

async def extract_memory(user_message, assistant_message):
    claude_connector=await ClaudeConnector.Create()
    prompt=f""" 
You are a memory extraction system.

Read the conversation below and determine whether
it contains useful long-term information about the user.

User:
{user_message}

Assistant:
{assistant_message}

Store information only if it will be useful
in future conversations.

Useful information includes:
- preferences
- interests
- goals
- skills
- projects
- important user facts

Do NOT store:
- temporary questions
- current time
- random calculations
- one-time requests
- tool results
- casual conversation

If useful information exists,
return ONLY the fact that should be remembered.

If there is nothing useful to remember,
return: None
"""

    response=await claude_connector.generate_response(prompt,"you are an AI memory extractor")
    await claude_connector.close()
    return response