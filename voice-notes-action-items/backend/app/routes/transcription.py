import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from app.services.speech_to_text import transcribe_audio_file
from app.limiter import limiter

router = APIRouter()

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB

@router.post("/transcribe")
@limiter.limit("5/minute")
async def transcribe(request: Request, audio: UploadFile = File(...)):
    if not audio.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio file.")
    
    file_size = 0
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".webm")
    try:
        while chunk := await audio.read(1024 * 1024):
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                temp_file.close()
                os.unlink(temp_file.name)
                raise HTTPException(status_code=400, detail="File size exceeds 25MB limit.")
            temp_file.write(chunk)
        temp_file.close()
        
        content_type = audio.content_type or "audio/webm"
        transcript = transcribe_audio_file(temp_file.name, mime_type=content_type)
        return {"transcript": transcript}
    finally:
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
