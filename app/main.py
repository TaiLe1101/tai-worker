"""FastAPI application factory and process lifecycle."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.endpoints import router
from app.core.config import get_settings
from app.services.translator import TranslationService
from app.services.tts_engine import TTSEngine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    translator = TranslationService(settings)
    app.state.translator = translator
    app.state.tts_engine = TTSEngine(settings)
    try:
        yield
    finally:
        translator.close()


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )
    application.include_router(router)
    return application


app = create_app()
