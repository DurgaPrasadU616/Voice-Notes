import os
from openai import OpenAI

def transcribe_audio_file(file_path: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    return transcription.text
