# AI Agent Project

This repository provides a small FastAPI chat server backed by a
local [llama.cpp](https://github.com/ggerganov/llama.cpp) model. The server and
model can run either together or as two separate containers.

## Requirements

- Python 3.11+
- A GGUF model file compatible with `llama.cpp`

Install the dependencies:

```bash
pip install -r app/requirements.txt
```

Place your GGUF model in `app/models` and set the `MODEL_PATH` environment variable to its path if it differs from the default. The default is `./models/google_gemma-3-4b-it-qat-Q4_0.gguf`.

## Running

### Local run

Start the FastAPI server with uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir app
```

Visit `http://localhost:8000` in your browser to chat with the model.

### Docker Compose

To run the server and the model in separate containers:

```bash
docker compose up --build
```

The chat UI will be available on port `8000` and the LLM service on `8001`.

