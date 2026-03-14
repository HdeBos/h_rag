"""Module containing API endpoints."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from h_rag.api.routers import chat, knowledge_bases
from h_rag.services.startup import StartupService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan function to check service health on startup."""
    startup_service = StartupService()
    await startup_service.initalize_environment()
    await startup_service.check_object_storage()
    await startup_service.check_llm()
    yield


app = FastAPI(title="HRAG API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://frontend:8501"],  # Streamlit frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(knowledge_bases.router)
