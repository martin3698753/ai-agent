from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import os

MODEL_PATH = os.getenv("MODEL_PATH", "./models/google_gemma-3-4b-it-qat-Q4_0.gguf")

if not os.path.isfile(MODEL_PATH):
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}. Set the MODEL_PATH environment variable"
    )

llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=2)

app = FastAPI()

class Prompt(BaseModel):
    prompt: str
    max_tokens: int = 512

@app.post("/generate")
async def generate(p: Prompt):
    output = llm(p.prompt, max_tokens=p.max_tokens, stop=["User:", "Assistant:"], echo=False)
    return {"text": output["choices"][0]["text"].strip()}
