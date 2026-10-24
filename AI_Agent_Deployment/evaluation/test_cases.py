# from retriever import retriever

# def get_context(question):
#     documents=retriever.invoke(question)
#     return documents

test_cases=[
    {
    "question":"What is the current time?",
    "expected_tool":"get_current_timestamp"
    }
    # ,
    #  {
    #      "context":get_context("What is MCP? "),
    #     "question":"What is MCP? find the in the given context",
    #     "expected_tool":"search_context"
    #     }
    
]