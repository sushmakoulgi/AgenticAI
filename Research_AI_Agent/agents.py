import json
from llm import ClaudeLLM
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
    llm=ClaudeLLM()

    system=" you are an AI research Agent," \
    "given the research plan, search the web to provide findings and provide the list of findings along with source and evidence" \
    "store the important findings in the research notes , before returning the report ," \
    "for all the findings , verify the findings to make sure it is correct against the evidence " \
    "do not invent sources, keep it very short. reject a final answer when no notes have been verified and tell Claude to go back and verify them"
    messages=[
        {
            "role":"user",
            "content":f" Given the user request {user_request} and plan {plan} ,provide the research findings"
        }
    ]
    max_step=10
    try:
        for step in range(max_step):
            print("Working on step ",{step+1})
            raw_response=await llm.generate_raw_response(messages,system,tools)

            if raw_response.stop_reason == "tool_use":
                # Append Claude's assistant message (which contains the tool call blocks) to history
                messages.append({"role": "assistant", "content": raw_response.content})

                # Claude may request several tools at once; every tool_use needs a matching tool_result
                tool_results = []
                for block in raw_response.content:
                    if block.type != "tool_use":
                        continue

                    print(f"Claude wants to use: {block.name} with arguments: {block.input}")

                    try:
                        result = await run_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id, # Must match the exact ID Claude gave you
                            "content": result
                        })
                    except Exception as e:
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": f"Error: {e}",
                            "is_error": True
                        })

                messages.append({"role": "user", "content": tool_results})
            else:
                return "".join(
                    block.text for block in raw_response.content if block.type == "text"
                )
        print("max steps reached")
        return "Max_ steps reached"
    finally:
        await llm.close()



async def create_research_plan(user_request):
    prompt=f"Given the user request, create a concise numbered research plan to serve the user request keep it within 3 limit" \
    f" {user_request}"

    llm=ClaudeLLM()
    message=[{
        "role":"user",
        "content":prompt}
    ]
    raw_response=await llm.generate_raw_response(message,"you are an AI research Planning agent")
    await llm.close()
    for block in raw_response.content:
        if block.type=="text":
            return block.text    
