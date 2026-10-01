"""Security Studio — FastAPI entrypoint"""
from fastapi import FastAPI

from src.api.routes import router

app = FastAPI(title="CloudForge Security Studio", version="0.1.0")
app.include_router(router)
