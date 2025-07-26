import requests
from utils.api_keys import GROQ_API_KEY

GEMINI_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_llama(prompt: str) -> str:
    """
    Sends a prompt to Gemini via Groq and returns the response.
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama3-70b-8192",  
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000,
        "stream": False
    }

    response = requests.post(GEMINI_URL, headers=headers, json=body)
    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"]
