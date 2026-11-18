"""Edge TTS speech synthesis service."""

import asyncio
import logging
import random
from pathlib import Path

import edge_tts

from app.core.config import Settings

logger = logging.getLogger(__name__)


class TTSEngine:
    def __init__(self, settings: Settings) -> None:
        self._voice = settings.tts_voice
        self._rate = settings.tts_rate
        self._max_retries = settings.tts_max_retries

    async def synthesize(self, text: str, output_path: Path) -> None:
        for attempt in range(self._max_retries):
            try:
                communicator = edge_tts.Communicate(
                    text,
                    self._voice,
                    rate=self._rate,
                )
                await communicator.save(str(output_path))
                if not output_path.exists() or output_path.stat().st_size == 0:
                    raise RuntimeError("TTS generated an empty audio file")
                return
            except Exception as exc:
                if attempt == self._max_retries - 1:
                    raise
                wait_time = (2**attempt) + random.uniform(0.5, 1.5)
                logger.warning(
                    "TTS failed (%s); retrying in %.1fs",
                    type(exc).__name__,
                    wait_time,
                )
                await asyncio.sleep(wait_time)
