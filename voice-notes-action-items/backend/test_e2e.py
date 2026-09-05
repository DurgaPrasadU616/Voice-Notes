import requests
import json
import os

BASE_URL = "http://localhost:8000"
test_results = []

def run_test(name, condition):
    try:
        res = condition()
        test_results.append(f"| {name} | Pass | {res} |")
    except Exception as e:
        test_results.append(f"| {name} | Fail | {str(e)} |")

# 1. Health
def test_health():
    r = requests.get(f"{BASE_URL}/health")
    if r.status_code == 200 and r.json().get("status") == "ok":
        return "Returns 200 OK {'status': 'ok'}"
    raise Exception(f"Failed with {r.status_code} {r.text}")
run_test("GET /health", test_health)

# 3. Non audio file
def test_non_audio():
    files = {"audio": ("test.txt", "this is not audio", "text/plain")}
    r = requests.post(f"{BASE_URL}/api/transcribe", files=files)
    if r.status_code == 400:
        return "Clean 400 error for text/plain"
    raise Exception(f"Failed with {r.status_code} {r.text}")
run_test("POST /api/transcribe (non-audio)", test_non_audio)

# 4. Extract Actions (with tasks)
def test_extract_tasks():
    payload = {"text": "Finish the report by Friday and call Alex tomorrow."}
    r = requests.post(f"{BASE_URL}/api/extract-actions", json=payload)
    if r.status_code == 200:
        data = r.json()
        if len(data.get("action_items", [])) == 2:
            return "Returned valid JSON matching schema"
    raise Exception(f"Failed with {r.status_code} {r.text}")
run_test("POST /api/extract-actions (with tasks)", test_extract_tasks)

# 5. Extract Actions (no tasks)
def test_extract_no_tasks():
    payload = {"text": "Today I went to the park and saw a bird."}
    r = requests.post(f"{BASE_URL}/api/extract-actions", json=payload)
    if r.status_code == 200:
        data = r.json()
        if len(data.get("action_items", [])) == 0:
            return "Returned empty action_items"
    raise Exception(f"Failed with {r.status_code} {r.text}")
run_test("POST /api/extract-actions (no tasks)", test_extract_no_tasks)

# 9. CORS
def test_cors():
    headers = {"Origin": "https://random-hacker.com"}
    r = requests.options(f"{BASE_URL}/api/tasks", headers=headers)
    if r.status_code == 400 or "access-control-allow-origin" not in r.headers:
        return "Blocked invalid origin"
    raise Exception("CORS allowed invalid origin")
run_test("CORS check", test_cors)

for res in test_results:
    print(res)
