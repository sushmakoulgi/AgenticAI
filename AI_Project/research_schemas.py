from pydantic import BaseModel,Field

class ResearchRequest(BaseModel):
    topic:str

class ResearchResponse(BaseModel):
    report:str

class ChatRequest(BaseModel):
    request:str

class ChatResponse(BaseModel):
    response:str

class ResearchPlan(BaseModel):
    tasks:list[str]=Field(
        min_length=3,
        max_length=3,
        description="Exactly 3 research tasks, in the order the agent should do them"
    )

class ReportFinding(BaseModel):
    point:str=Field(description="One finding, written as a clear sentence")
    source:str=Field(description="File the finding came from, for example mcp.txt")

class ResearchReport(BaseModel):
    heading:str=Field(description="Short title for the report")
    findings:list[ReportFinding]=Field(description="What the research says, one item per finding")
    summary:str=Field(description="One-line summary of the research")
