from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from agent import ask_llm

app = FastAPI()
templates = Jinja2Templates(directory="templates")



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
    prompt = "\n".join(
        [msg.replace("User:", "User:").replace("Agent:", "Assistant:") for msg in conversation_history]
    )
    prompt += "\nAssistant:"

    agent_reply = ask_llm(prompt)

    conversation_history.append(f"Agent: {agent_reply}")
    return await index(request)
