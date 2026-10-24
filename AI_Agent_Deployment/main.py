from agent import run_agent
from fastapi import FastAPI,HTTPException,Request
from schemas import ChatRequest,ChatResponse
import httpx
from contextlib import asynccontextmanager
import asyncio
from utils import RateLimiter
import uuid
from logger import logger

rate_limiter=RateLimiter()
@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Application Starting")
    
    yield

    print("Application Shutting down")


app=FastAPI(title="My First AI Agent API",
            version="1.0.0",
            lifespan=lifespan)

@app.post("/chat",response_model=ChatResponse)
async def chat(request:Request,user_request:ChatRequest):
    request_id=str(uuid.uuid4())
    logger.info(f" Checking for rate Limits for {request_id}")
    if rate_limiter.is_rate_within_limit(request.client.host):
        logger.info(f"Executing the Agent {request_id}")
        return await run_agent(user_request.message)
    else:
        raise HTTPException(
            status_code=429,detail="Too many requests"
        )
    

@app.get("/health")
async def health():
    return {
        "status":"OK"
    }

@app.get("/ready")
async def ready():
    try:

        async with httpx.AsyncClient() as client:
            response=await client.post("https://anthropic.com/",timeout=2)
            print(response)
            if response.status==200:
                return {
                    "status":"ready"
                }
            return {
                        "status":"Not Ready"
                    }
    except Exception as ex:
        return {
            "status":"Not Ready"
        }


