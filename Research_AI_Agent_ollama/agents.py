import json
from llm import OllamaLLM
from tools import (
    search_web_tool,read_web_page_tool,
    search_web,read_webpage,get_research_notes,
    get_research_notes_tool,add_research_notes,
    add_research_notes_tool,verify_findings,
    verify_findings_tool)

async def run_tool(tool_name, tool_input):
    # Names must match the "name" field in each tool definition
    if tool_name == "search_web":
        return json.dumps(search_web(
            query=tool_input["query"],
            max_results=2
        ))
    elif tool_name == "read_webpage":
        return read_webpage(url=tool_input["url"])
    elif tool_name=="add_research_notes":
        return json.dumps(add_research_notes(source=tool_input["source"],findings=tool_input["findings"],evidence=tool_input["evidence"]))
    elif tool_name=="get_research_notes":
        return json.dumps(get_research_notes())
    elif tool_name=="verify_findings":
        return json.dumps(await verify_findings(source=tool_input["source"],findings=tool_input["findings"],evidence=tool_input["evidence"]))
    raise ValueError(f"Unknown tool: {tool_name}")


async def research_agent(user_request):


    tools=[search_web_tool,read_web_page_tool,add_research_notes_tool,get_research_notes_tool,
           verify_findings_tool]
    plan=await create_research_plan(user_request=user_request)

    print("="*60)
    print("Research Plan",plan)
    print("="*60)
    llm=OllamaLLM()

    system=" you are an AI research Agent," \
    "given the research plan, search the web to provide findings and provide the research report" \
    "store the important findings in the research notes , before returning the report ," \
    "for all the findings , verify the findings to make sure it is correct against the source and evidence " \
    "do not invent sources. reject a final answer when no notes have been verified and tell Claude to go back and verify them"
    messages=[
        {
            "role":"user",
            "content":f" Given the user request {user_request} and plan {plan} ,provide the research report"
        }
    ]
    max_step=5
    try:
        for step in range(max_step):
            print("Working on step ",{step+1})
            raw_response=await llm.generate_raw_response(messages,system,tools)

            # Ollama has no stop_reason; a reply with tool_calls means the model wants tools run
            if raw_response.message.tool_calls:
                # Append the model's assistant message (which contains the tool calls) to history
                messages.append(raw_response.message)

                # The model may request several tools at once; each gets its own "tool" message
                for call in raw_response.message.tool_calls:
                    name = call.function.name
                    args = call.function.arguments

                    print(f"Ollama wants to use: {name} with arguments: {args}")

                    try:
                        result = await run_tool(name, args)
                    except Exception as e:
                        result = f"Error: {e}"

                    messages.append({
                        "role": "tool",
                        "tool_name": name,
                        "content": result
                    })
            else:
                return raw_response.message.content
        print("max steps reached")
        return "Max_ steps reached"
    finally:
        await llm.close()



async def create_research_plan(user_request):
    prompt=f"Given the user request, create a concise numbered research plan to serve the user request " \
    f"{user_request}"

    llm=OllamaLLM()
    message=[{
        "role":"user",
        "content":prompt}
    ]
    raw_response=await llm.generate_raw_response(message,"you are an AI research Planning agent")
    await llm.close()
    return raw_response.message.content
