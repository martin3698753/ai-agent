from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import uvicorn
import requests
import os
import html

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = "gemma3:4b"

conversation_history = []

class Message(BaseModel):
    user_input: str

@app.get("/", response_class=HTMLResponse)
async def index():
    history_html = "<br><br>".join(html.escape(msg) for msg in conversation_history)
    return HTMLResponse(content=f"""
    <html>
        <head><title>Agent Chat</title></head>
        <body>
            <h2>AI Agent Chat</h2>
            <form method="post" action="/chat">
                <textarea name="user_input" rows="4" cols="50"></textarea><br>
                <input type="submit" value="Send">
            </form>
            <h3>Conversation:</h3>
            <div>{history_html}</div>
        </body>
    </html>
    """)

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    form = await request.form()
    user_input = form["user_input"]
    conversation_history.append(f"<b>You:</b> {user_input}")

    prompt = "\n".join([msg.replace("<b>You:</b>", "User:").replace("<b>Agent:</b>", "Assistant:") for msg in conversation_history])

    payload = {
        "model": MODEL,
        "prompt": prompt + f"\nUser: {user_input}\nAssistant:",
        "stream": False
    }
    try:
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=30)
        response.raise_for_status()
        agent_reply = response.json().get("response", "[no response]")
    except Exception as e:
        agent_reply = f"[error: {e}]"

    conversation_history.append(f"<b>Agent:</b> {agent_reply}")
    return await index()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
