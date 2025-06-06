"""Utility for interacting with a local Llama.cpp model."""

import os
from llama_cpp import Llama

# Model path can be overridden via environment variable
MODEL_PATH = os.getenv("MODEL_PATH", "./models/google_gemma-3-4b-it-qat-Q4_0.gguf")

# Initialise a single model instance so it can be reused across requests
# Provide a clearer error when the model file is missing
if not os.path.isfile(MODEL_PATH):
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}. Set the MODEL_PATH environment variable"
    )

llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=2)


def ask_llm(prompt: str, *, max_tokens: int = 512) -> str:
    """Generate a response from the local Llama model."""
    try:
        output = llm(prompt, max_tokens=max_tokens, stop=["User:", "Assistant:"], echo=False)
        return output["choices"][0]["text"].strip()
    except Exception as e:
        return f"[chyba: {e}]"
