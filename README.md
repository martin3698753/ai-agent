# AI Agent Project

This repository provides a small FastAPI server that exposes a chat page backed by a local [llama.cpp](https://github.com/ggerganov/llama.cpp) model. The model is loaded using `llama-cpp-python`.

## Requirements

- Python 3.11+
- A GGUF model file compatible with `llama.cpp`

Install the dependencies:

```bash
pip install -r app/requirements.txt
```

Place your GGUF model in `app/models` and set the `MODEL_PATH` environment variable to its path if it differs from the default. The default is `./models/google_gemma-3-4b-it-qat-Q4_0.gguf`.

## Running

Start the FastAPI server with uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir app
```

Visit `http://localhost:8000` in your browser to chat with the model.

