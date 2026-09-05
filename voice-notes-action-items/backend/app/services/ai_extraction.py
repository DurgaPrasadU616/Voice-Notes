import os
import json
from openai import OpenAI
from pydantic import ValidationError
from app.models import ExtractActionsResponse

SYSTEM_PROMPT = """You are an AI assistant that extracts structured tasks from voice note transcripts.
Your output must be a valid JSON object following this exact schema:
{
  "summary": "string",
  "action_items": [
    {
      "task": "string",
      "deadline": "string or null",
      "priority": "High" | "Medium" | "Low",
      "category": "string or null"
    }
  ]
}
Rules:
- NEVER invent tasks. Only extract tasks explicitly stated or clearly implied by the user's intent.
- Preserve stated deadlines exactly. If no deadline is stated, use null.
- Infer category when obvious (e.g., "Work", "Personal", "Groceries", "Project X").
- If there are no tasks, return an empty array [] for action_items.
"""

from fastapi import HTTPException
from dotenv import load_dotenv
from google import genai
from google.genai import types

def extract_tasks_from_text(text: str) -> dict:
    load_dotenv(override=True)
    gemini_key = (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip()
    
    # 1. Primary: Google Gemini
    if gemini_key and gemini_key not in ("your_gemini_api_key_here", "your_api_key_here"):
        client = genai.Client(api_key=gemini_key)
        models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash"]
        last_err = None
        
        for model_name in models_to_try:
            for attempt in range(2):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=f"{SYSTEM_PROMPT}\n\nTranscript to analyze:\n{text}",
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                        )
                    )
                    content = response.text
                    parsed_content = json.loads(content)
                    
                    # Validate with Pydantic
                    ExtractActionsResponse(**parsed_content)
                    return parsed_content
                except (json.JSONDecodeError, ValidationError) as e:
                    last_err = ValueError("Failed to extract valid tasks from text.")
                    continue
                except Exception as e:
                    last_err = e
                    break
        if last_err:
            raise last_err

    # 2. Fallback: OpenAI if OPENAI_API_KEY is configured
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if openai_key and openai_key not in ("your_openai_api_key_here", "your_openai_api_key"):
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        for attempt in range(2):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": text}
                    ],
                    response_format={"type": "json_object"}
                )
                content = response.choices[0].message.content
                parsed_content = json.loads(content)
                ExtractActionsResponse(**parsed_content)
                return parsed_content
            except (json.JSONDecodeError, ValidationError) as e:
                if attempt == 1:
                    raise ValueError("Failed to extract valid tasks from text.") from e
                continue

    raise HTTPException(
        status_code=401,
        detail="Gemini API key is missing. Please configure GEMINI_API_KEY in backend/.env"
    )
