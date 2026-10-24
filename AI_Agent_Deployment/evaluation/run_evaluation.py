from test_agent import run_agent,prep_agent
from test_cases import test_cases

import asyncio

async def main():
    agent=await prep_agent()
    for test_case in test_cases:
        question=test_case["question"]
        expected_tool=test_case["expected_tool"]
        context=test_case.get("context",None)

        if context is not None:
            question=question+ f"context {context}"
        messages=await run_agent(question,agent=agent)
        called_tools=[]
        for message in messages:
            # AIMessage: the tools the model asked to call
            if hasattr(message,"tool_calls"):
                for call in message.tool_calls:
                    called_tools.append(call["name"])
            # ToolMessage: the tool that actually ran
            if getattr(message,"name",None) and hasattr(message,"tool_call_id"):
                called_tools.append(message.name)

        if expected_tool in called_tools:
            print(f"Pass: {test_case['question']} -- called tool {expected_tool}")
        else:
            print(f"Fail: {test_case['question']} (expected {expected_tool}, got {called_tools})")


asyncio.run(main())