import sys
from pathlib import Path
import asyncio
from fastapi import FastAPI,HTTPException
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse,StreamingResponse
from fastapi.staticfiles import StaticFiles

from agent import run_agent
from research_schemas import ResearchRequest,ResearchResponse,ChatRequest,ChatResponse

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Starting")
    yield
    print("Stopping")


app=FastAPI(title="AI_Reasearch_Project",
            version="1.0.0",
            lifespan=lifespan)

app.mount("/static",StaticFiles(directory="frontend"),name="static")

@app.get("/")
async def home():
    return FileResponse("frontend/index.html")

@app.get("/health")
async def health():
    return {"status":"ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat(user_request:ChatRequest):
    if user_request.request.strip()=="":
        raise HTTPException(status_code=400, detail="request cannot be empty")
    result=await run_agent(user_request.request)
    return ChatResponse(response=str(result))

@app.post("/research", response_model=ResearchResponse)
async def research(request:ResearchRequest):
 
    if request.topic.strip()=="":
        raise HTTPException(status_code=400, detail="topic cannot be empty")
    
    queue=asyncio.queue()

    def process_callback(event):
        queue.put_nowait(event)

        
    result=await run_agent(request.topic)
    return ResearchResponse(report=str(result))
