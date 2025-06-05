from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from llama_cpp import Llama
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

MODEL_PATH = "./models/google_gemma-3-4b-it-qat-Q4_0.gguf"
llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=4)

conversation_history = []

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    history = [
        {"role": "user" if "User:" in msg else "agent",
         "label": "Ty" if "User:" in msg else "Agent",
         "text": msg.split(":", 1)[1].strip()}
        for msg in conversation_history
    ]
    return templates.TemplateResponse("chat.html", {"request": request, "history": history})

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, user_input: str = Form(...)):
    conversation_history.append(f"User: {user_input}")
    prompt = "\n".join([msg.replace("User:", "User:").replace("Agent:", "Assistant:") for msg in conversation_history])
    prompt += f"\nUser: {user_input}\nAssistant:"

    try:
        output = llm(prompt, max_tokens=512, stop=["User:", "Assistant:"], echo=False)
        agent_reply = output["choices"][0]["text"].strip()
    except Exception as e:
        agent_reply = f"[chyba: {e}]"

    conversation_history.append(f"Agent: {agent_reply}")
    return await index(request)
