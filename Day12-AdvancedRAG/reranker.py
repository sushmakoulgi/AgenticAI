from claude_connector import ClaudeConnector


async def rerank(query,candidates,top_k):
    scored=[]
    claude_connector=await ClaudeConnector.Create()
    for candidate in candidates:
        prompt=f""" you are an AI document relevance calculator, 
        given the user query {query} and text {candidate["text"]}
        check the relevance of query vs text and give relevance score
        100 being completely matching and 0 being nothing matches, only
        return the number"""
        response=await claude_connector.generate_response(prompt=prompt,system="you are document relevance calculator")
        score=0.0
        try:
            if response:
                score=float(response)           
        except:
            score= 0.0
        scored.append({
            **candidate,
            "rerank_score":score
        })

    scored.sort(key=lambda item:item["rerank_score"],reverse=True)
    return scored[:top_k]