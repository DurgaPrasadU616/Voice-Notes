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

def extract_tasks_from_text(text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
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
            
            # Validate with Pydantic
            ExtractActionsResponse(**parsed_content)
            return parsed_content
            
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt == 1:
                raise ValueError("Failed to extract valid tasks from text.") from e
            continue
    
    raise ValueError("Failed to extract valid tasks from text after retries.")
