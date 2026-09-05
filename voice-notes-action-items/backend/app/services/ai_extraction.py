import os
import json
from fastapi import HTTPException
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError
from app.models import ExtractActionsResponse

SYSTEM_PROMPT = """You are an AI assistant that extracts structured tasks from voice note transcripts.

Rules:
- NEVER invent tasks. Only extract tasks explicitly stated or clearly implied by the user's intent.
- Preserve stated deadlines exactly. If no deadline is stated, use null.
- Infer category when obvious (e.g., "Work", "Personal", "Groceries", "Project X").
- If there are no tasks, return an empty array [] for action_items.
- Return ONLY valid JSON. No markdown fences, no commentary."""


def _get_client() -> genai.Client:
    load_dotenv(override=True)
    key = (os.getenv("GEMINI_API_KEY") or "").strip()
    if not key or key == "your_gemini_api_key_here":
        raise HTTPException(
            status_code=401,
            detail="GEMINI_API_KEY is not configured. Set it in backend/.env",
        )
    return genai.Client(api_key=key)


def extract_tasks_from_text(text: str) -> dict:
    client = _get_client()

    response_schema = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "summary": types.Schema(type=types.Type.STRING),
            "action_items": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "task": types.Schema(type=types.Type.STRING),
                        "deadline": types.Schema(
                            type=types.Type.STRING,
                            nullable=True,
                        ),
                        "priority": types.Schema(
                            type=types.Type.STRING,
                            enum=["High", "Medium", "Low"],
                        ),
                        "category": types.Schema(
                            type=types.Type.STRING,
                            nullable=True,
                        ),
                    },
                    required=["task", "priority"],
                ),
            ),
        },
        required=["summary", "action_items"],
    )

    user_prompt = f"{SYSTEM_PROMPT}\n\nTranscript to analyze:\n{text}"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_schema,
            ),
        )
        content = response.text
        parsed = json.loads(content)
        ExtractActionsResponse(**parsed)
        return parsed
    except (json.JSONDecodeError, ValidationError) as e:
        raise HTTPException(
            status_code=422,
            detail=f"Failed to parse valid tasks from AI response: {e}",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {e}")
