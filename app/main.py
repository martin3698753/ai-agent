import os
import time
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from agent import ask_llm

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory conversation history shared across all users.
conversation_history = []



@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the current chat history."""
    return templates.TemplateResponse("chat.html", {"request": request, "history": conversation_history})

@app.post("/chat", response_class=HTMLResponse)
async def chat(
    request: Request,
    user_input: str = Form(...),
    image: UploadFile | None = File(None),
):
    """Handle a chat message and optional image upload."""

    entry = {"role": "user", "text": user_input}
    if image and image.filename:
        os.makedirs("static/uploads", exist_ok=True)
        filename = f"{int(time.time())}_{image.filename}"
        file_path = os.path.join("static", "uploads", filename)
        with open(file_path, "wb") as f:
            f.write(await image.read())
        entry["image"] = "/" + file_path

    conversation_history.append(entry)

    prompt_parts = []
    for msg in conversation_history:
        if msg["role"] == "user":
            if msg.get("image"):
                prompt_parts.append(f"User: <image:{msg['image']}> {msg['text']}")
            else:
                prompt_parts.append(f"User: {msg['text']}")
        else:
            prompt_parts.append(f"Assistant: {msg['text']}")

    prompt = "\n".join(prompt_parts) + "\nAssistant:"

    agent_reply = ask_llm(prompt)

    conversation_history.append({"role": "agent", "text": agent_reply})
    return await index(request)
