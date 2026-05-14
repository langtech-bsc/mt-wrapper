from fastapi import FastAPI
from .config import settings
from .routers import google, deepl, custom

app = FastAPI(title="MT Adapter API")

app.include_router(google.router, tags=["google"])
app.include_router(deepl.router, tags=["deepl"])
app.include_router(custom.router, tags=["custom"])

@app.get("/health", tags=["system"])
def health_check():
    return {
        "status": "ok", 
        "model": settings.salamandra_model,
        "backend_url": settings.salamandra_url
    }
