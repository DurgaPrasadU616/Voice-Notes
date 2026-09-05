"""
Standalone test to verify GEMINI_API_KEY works.
Run: python test_gemini.py
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GEMINI_API_KEY", "").strip()
if not key or key == "your_gemini_api_key_here":
    print("FAIL: GEMINI_API_KEY is not set or still placeholder.")
    print("Set it in backend/.env")
    sys.exit(1)

from google import genai

client = genai.Client(api_key=key)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say exactly: hello from gemini",
)
print(f"OK: {response.text.strip()}")
