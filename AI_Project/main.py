import sys
from pathlib import Path
import asyncio
from fastapi import FastAPI,HTTPException
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse,StreamingResponse
from fastapi.staticfiles import StaticFiles
import json
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


@app.post("/research", response_model=ResearchResponse)
async def research(request:ResearchRequest):
 
    if request.topic.strip()=="":
        raise HTTPException(status_code=400, detail="topic cannot be empty")
    
    queue=asyncio.Queue()

    def process_callback(event):
        queue.put_nowait(event)

    async def event_stream():
        task=asyncio.create_task(run_agent(request.topic,process_callback))
        

        while True:
            if task.done() and queue.empty():
                break

            try:
                event=await asyncio.wait_for(
                    queue.get(),timeout=0.5
                )
                yield (""
                "data:"+json.dumps(event)+"\n\n")

            except TimeoutError:
                continue
        try:
            result=await task
        except HTTPException as exc:
            # The stream has already started, so send the error as an event
            yield ("data:"+json.dumps({"error":exc.detail})+"\n\n")
            return
        yield ("data:"+json.dumps({"result":result})+"\n\n")

    return StreamingResponse(event_stream(),media_type="text/event-stream")
        
    # result=await run_agent(request.topic)
    # return ResearchResponse(report=str(result))
