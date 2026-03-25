import requests
import json
import sys

def test_health():
    try:
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code == 200:
            print("✅ Backend Health Check: PASSED")
        else:
            print(f"❌ Backend Health Check: FAILED (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Backend Health Check: FAILED (Error: {e})")

def test_summarize():
    payload = {
        "text": "This is a long piece of text that needs to be summarized. It should contain more than fifty characters to pass the validation check implemented in the backend. Machine learning is a field of inquiry devoted to understanding and building methods that 'learn', that is, methods that leverage data to improve performance on some set of tasks."
    }
    try:
        response = requests.post("http://localhost:8000/api/summarize", json=payload)
        if response.status_code == 200:
            print("✅ Summarize Endpoint: SUCCESS")
            print("Summary:", response.json().get("summary"))
        elif response.status_code == 429:
            print("ℹ️ Summarize Endpoint: RATE LIMITED (Expected behavior if tested too fast)")
        elif response.status_code == 500 or response.status_code == 502:
            print(f"❌ Summarize Endpoint: SERVER ERROR ({response.status_code}) - Check if MISTRAL_API_KEY is valid.")
            print("Detail:", response.json().get("detail"))
        else:
            print(f"❌ Summarize Endpoint: FAILED (Status: {response.status_code})")
            print("Detail:", response.json().get("detail"))
    except Exception as e:
        print(f"❌ Summarize Endpoint: FAILED (Error: {e})")

if __name__ == "__main__":
    print("--- Mistral Summarizer Backend Verification ---")
    test_health()
    test_summarize()
