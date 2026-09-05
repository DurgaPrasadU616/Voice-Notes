import os
from openai import OpenAI
from fastapi import HTTPException

def transcribe_audio_file(file_path: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or api_key in ("your_openai_api_key_here", "your_openai_api_key"):
        raise HTTPException(
            status_code=401,
            detail="OpenAI API key is missing or set to placeholder. Please configure your OPENAI_API_KEY in backend/.env"
        )
    client = OpenAI(api_key=api_key)
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    return transcription.text
