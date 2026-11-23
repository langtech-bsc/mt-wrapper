# MT Adapter

A translation API adapter and wrapper that exposes standard machine translation interfaces (Google Cloud Translate v2, DeepL v2) as well as custom endpoints, routing the requests to an underlying OpenAI-compatible LLM. The adapter is specifically tailored for translation models like [SalamandraTA](https://huggingface.co/BSC-LT/salamandraTA-7b-instruct).

## Features

The adapter provides compatibility layers for standard translation APIs, allowing drop-in replacement in applications expecting those services:

- **Google Cloud Translate API v2** (`/language/translate/v2`)
- **DeepL API v2** (`/v2/translate`)
- **Custom API** (`/api/v1/post-edit`, `/api/v1/grammar-check`)

## Language codes

SalamandraTA is prompted with English language *names*. The adapter therefore converts the codes sent by Google Translate / DeepL clients (`es`, `CA`, `EN-GB`, `pt-BR`, `zh-Hans`, `nb`, ...) into names (`Spanish`, `Catalan`, `English`, `Portuguese`, `Chinese`, `Norwegian Bokmål`) before building the prompt; see `app/languages.py`. Values that are not a known code (e.g. `Catalan`) are passed through unchanged. If no source language is given, the model is told the source is "Unknown".

## Environment Variables

The service is configured using the following environment variables (which can also be provided via a `.env` file):

| Variable | Default | Description |
|----------|---------|-------------|
| `SALAMANDRA_URL` | `http://localhost:8000/v1` | URL to the OpenAI-compatible completion endpoint |
| `SALAMANDRA_MODEL` | `BSC-LT/salamandraTA-7b-instruct` | Model identifier to pass in requests |
| `SALAMANDRA_API_KEY` | `""` | Optional API key for the underlying LLM service |

## Running the Service

### Using Docker Compose (Recommended)

You can run the adapter using the provided `docker-compose.yml` file:

```bash
docker-compose up -d
```

This will pull the latest image and expose the API on port `8000`.

### Running Locally

Ensure you have Python 3.11+ installed.

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Endpoints Overview

- `POST /language/translate/v2`: Google Cloud Translate API compatibility.
- `POST /v2/translate`: DeepL API compatibility (supports both JSON and form data).
- `POST /api/v1/post-edit`: Post-editing machine translation output given source and translation text.
- `POST /api/v1/grammar-check`: Grammar checking and fixing for a given sentence.
- `GET /health`: System health check endpoint.

## Architecture

The application is built with **FastAPI** and uses **HTTPX** for asynchronous requests to the underlying LLM backend. It translates the payload expected by each respective API into a simple prompt specifically designed for the model to execute translation, post-editing, or grammar-checking tasks.

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
