"""HTTP endpoints for the worker API."""

import asyncio
import logging
import tempfile
from pathlib import Path
from typing import Annotated
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.core.security import require_api_key
from app.schemas.tts import HealthResponse, ProcessTTSRequest
from app.services.translator import TranslationService, TranslationUnavailableError
from app.services.tts_engine import TTSEngine

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(require_api_key)])


def get_translator(request: Request) -> TranslationService:
    return request.app.state.translator


def get_tts_engine(request: Request) -> TTSEngine:
    return request.app.state.tts_engine


@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health() -> HealthResponse:
    return HealthResponse()


@router.post(
    "/process-tts",
    response_class=Response,
    responses={
        200: {
            "content": {"audio/mpeg": {}},
            "description": "Generated MP3 audio",
        },
        502: {"description": "Speech synthesis failed"},
    },
    tags=["TTS"],
)
async def process_tts(
    payload: ProcessTTSRequest,
    translator: Annotated[TranslationService, Depends(get_translator)],
    tts_engine: Annotated[TTSEngine, Depends(get_tts_engine)],
) -> Response:
    # Provider SDKs are synchronous; keep them outside the event loop.
    try:
        translated_text = await asyncio.to_thread(translator.translate, payload.text)
    except TranslationUnavailableError:
        logger.error("Translation unavailable; TTS was not started")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Không thể dịch nội dung sang tiếng Việt; vui lòng thử lại",
        ) from None

    # Closing NamedTemporaryFile before Edge writes is required on Windows.
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_path = Path(temp_file.name)

    try:
        await tts_engine.synthesize(translated_text, temp_path)
        audio = await asyncio.to_thread(temp_path.read_bytes)
    except Exception as exc:
        logger.exception("TTS rendering failed (%s)", type(exc).__name__)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Không thể tạo giọng đọc; vui lòng thử lại",
        ) from None
    finally:
        temp_path.unlink(missing_ok=True)

    return Response(
        content=audio,
        media_type="audio/mpeg",
        headers={
            "X-Translated-Text": quote(translated_text, safe=""),
            "Cache-Control": "no-store",
        },
    )
