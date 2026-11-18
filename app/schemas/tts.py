"""Request and response schemas for the TTS API."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.utils.text import clean_text


class ProcessTTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10_000)
    target_lang: Literal["vi"] = "vi"

    @field_validator("text")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        normalized = clean_text(value)
        if not normalized:
            raise ValueError("Text is empty after cleaning")
        return normalized


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    protocol: Literal["tai-tts-v1"] = "tai-tts-v1"
