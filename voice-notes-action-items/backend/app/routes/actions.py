import logging
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.models import ExtractActionsResponse
from app.services.ai_extraction import extract_tasks_from_text
from app.limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter()

class ExtractRequest(BaseModel):
    text: str

@router.post("/extract-actions", response_model=ExtractActionsResponse)
@limiter.limit("10/minute")
async def extract_actions(request: Request, payload: ExtractRequest):
    try:
        result = extract_tasks_from_text(payload.text)
        return result
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Error extracting actions: {str(e)}")
        raise
