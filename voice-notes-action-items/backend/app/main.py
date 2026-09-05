from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import time
import logging
import uuid

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.database import engine, Base
from app.routes import transcription, actions, tasks
from app.limiter import limiter

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Create SQLite tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Voice Notes API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Enable CORS restricted to FRONTEND_URL
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    req_id = str(uuid.uuid4())
    logger.info(f"Request started: {req_id} - {request.method} {request.url.path}")
    start_time = time.time()
    
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(f"Request completed: {req_id} - Status {response.status_code} - Latency: {process_time:.2f}ms")
        return response
    except Exception as e:
        process_time = (time.time() - start_time) * 1000
        logger.error(f"Request failed: {req_id} - Latency: {process_time:.2f}ms - Error: {str(e)}")
        raise

import openai
from fastapi import HTTPException

# OpenAI and Global Error Handlers
@app.exception_handler(openai.AuthenticationError)
async def openai_auth_error_handler(request: Request, exc: openai.AuthenticationError):
    logger.error(f"OpenAI Authentication Error: {str(exc)}")
    return JSONResponse(
        status_code=401,
        content={"detail": "OpenAI Authentication Failed: Invalid or missing API key. Please check your OPENAI_API_KEY in backend/.env"},
    )

@app.exception_handler(openai.RateLimitError)
async def openai_rate_limit_handler(request: Request, exc: openai.RateLimitError):
    logger.error(f"OpenAI Rate Limit Error: {str(exc)}")
    return JSONResponse(
        status_code=429,
        content={"detail": "OpenAI account credit balance is exhausted ($0 balance). Please add credits to your OpenAI account at https://platform.openai.com/settings/organization/billing to continue using Whisper & GPT."},
    )

@app.exception_handler(openai.OpenAIError)
async def openai_error_handler(request: Request, exc: openai.OpenAIError):
    logger.error(f"OpenAI API Error: {str(exc)}")
    return JSONResponse(
        status_code=502,
        content={"detail": f"OpenAI Service Error: {str(exc)}"},
    )

from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

from google.genai import errors as genai_errors

@app.exception_handler(genai_errors.APIError)
async def gemini_api_error_handler(request: Request, exc: genai_errors.APIError):
    logger.error(f"Gemini API Error [{exc.code}]: {str(exc)}")
    if exc.code in (400, 401, 403):
        return JSONResponse(
            status_code=401,
            content={"detail": "Gemini API Authentication Failed: Invalid API key. Please check your GEMINI_API_KEY in backend/.env"},
        )
    if exc.code == 429:
        return JSONResponse(
            status_code=429,
            content={"detail": "Gemini API rate limit or quota exceeded. Please wait a moment or check your Google AI Studio quota."},
        )
    return JSONResponse(
        status_code=502,
        content={"detail": f"Gemini API Error: {str(exc)}"},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, (HTTPException, StarletteHTTPException)):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    if isinstance(exc, genai_errors.APIError):
        if exc.code in (400, 401, 403):
            return JSONResponse(
                status_code=401,
                content={"detail": "Gemini API Authentication Failed: Invalid API key. Please check your GEMINI_API_KEY in backend/.env"},
            )
        if exc.code == 429:
            return JSONResponse(
                status_code=429,
                content={"detail": "Gemini API rate limit or quota exceeded. Please wait a moment or check your Google AI Studio quota."},
            )
        return JSONResponse(
            status_code=502,
            content={"detail": f"Gemini API Error: {str(exc)}"},
        )
    if isinstance(exc, openai.AuthenticationError):
        return JSONResponse(
            status_code=401,
            content={"detail": "OpenAI Authentication Failed: Invalid or missing API key. Please check your OPENAI_API_KEY in backend/.env"},
        )
    if isinstance(exc, openai.RateLimitError):
        return JSONResponse(
            status_code=429,
            content={"detail": "OpenAI account credit balance is exhausted ($0 balance). Please add credits to your OpenAI account at https://platform.openai.com/settings/organization/billing to continue using Whisper & GPT."},
        )
    if isinstance(exc, openai.OpenAIError):
        return JSONResponse(
            status_code=502,
            content={"detail": f"OpenAI Service Error: {str(exc)}"},
        )
    
    logger.exception(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )

app.include_router(transcription.router, prefix="/api", tags=["transcription"])
app.include_router(actions.router, prefix="/api", tags=["actions"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "hello world"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

