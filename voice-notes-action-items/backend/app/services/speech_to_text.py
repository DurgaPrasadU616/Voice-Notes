import os
from google import genai
from google.genai import types
from fastapi import HTTPException
from dotenv import load_dotenv


def _get_client() -> genai.Client:
    load_dotenv(override=True)
    key = (os.getenv("GEMINI_API_KEY") or "").strip()
    if not key or key == "your_gemini_api_key_here":
        raise HTTPException(
            status_code=401,
            detail="GEMINI_API_KEY is not configured. Set it in backend/.env",
        )
    return genai.Client(api_key=key)


def transcribe_audio_file(file_path: str, mime_type: str = "audio/webm") -> str:
    client = _get_client()

    clean_mime = mime_type.split(";")[0].strip() if mime_type else "audio/webm"
    if clean_mime in ("audio/x-m4a", "audio/m4a"):
        clean_mime = "audio/mp4"

    with open(file_path, "rb") as f:
        audio_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=audio_bytes, mime_type=clean_mime),
            "Transcribe this audio exactly. Return only the transcript text with no commentary, labels, or formatting.",
        ],
    )

    text = (response.text or "").strip()
    if not text:
        raise HTTPException(status_code=422, detail="No speech detected in the audio.")
    return text
