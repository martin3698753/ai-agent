import os
import requests
import time

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = "gemma3:4b"

def ask_llm(prompt):
    url = f"{OLLAMA_URL}/api/generate"
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json().get("response", "No response")

    except requests.exceptions.ConnectionError:
        return "❌ Ollama není dostupná (Connection refused)."

    except requests.exceptions.RequestException as e:
        if response.status_code == 500:
            return "❌ Ollama běží, ale model není načten. Spusť ho ručně: `ollama run gemma3:4b` nebo `curl`."
        return f"⚠️ Chyba při komunikaci s Ollamou: {e}"
