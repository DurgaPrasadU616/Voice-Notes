from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.models import ExtractActionsResponse
from app.services.ai_extraction import extract_tasks_from_text
from app.limiter import limiter

router = APIRouter()

class ExtractRequest(BaseModel):
    text: str

@router.post("/extract-actions", response_model=ExtractActionsResponse)
@limiter.limit("10/minute")
async def extract_actions(request: Request, payload: ExtractRequest):
    try:
        result = extract_tasks_from_text(payload.text)
        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)} type: {type(e)}")
