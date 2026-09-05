import os
from google import genai
from google.genai import types
from fastapi import HTTPException
from dotenv import load_dotenv

def transcribe_audio_file(file_path: str, mime_type: str = "audio/webm") -> str:
    load_dotenv(override=True)
    gemini_key = (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip()
    
    # 1. Primary: Google Gemini
    if gemini_key and gemini_key not in ("your_gemini_api_key_here", "your_api_key_here"):
        clean_mime = mime_type.split(";")[0].strip() if mime_type else "audio/webm"
        if clean_mime in ("audio/x-m4a", "audio/m4a"):
            clean_mime = "audio/mp4"

        client = genai.Client(api_key=gemini_key)
        with open(file_path, "rb") as f:
            audio_bytes = f.read()

        models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash"]
        last_err = None
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[
                        types.Part.from_bytes(
                            data=audio_bytes,
                            mime_type=clean_mime,
                        ),
                        "Generate an accurate, verbatim transcription of all spoken words in this audio file. Return ONLY the transcribed text. Do not add formatting, preambles, or conversational commentary."
                    ]
                )
                return (response.text or "").strip()
            except Exception as e:
                last_err = e
                continue
        if last_err:
            raise last_err

    # 2. Fallback: OpenAI Whisper if OPENAI_API_KEY is configured
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if openai_key and openai_key not in ("your_openai_api_key_here", "your_openai_api_key"):
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        return transcription.text

    raise HTTPException(
        status_code=401,
        detail="Gemini API key is missing. Please configure GEMINI_API_KEY in backend/.env"
    )
