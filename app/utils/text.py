"""Text normalization helpers."""

import re

_HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
_WHITESPACE_PATTERN = re.compile(r"\s+")


def clean_text(value: str) -> str:
    """Remove HTML-like tags and collapse whitespace."""

    without_tags = _HTML_TAG_PATTERN.sub("", value)
    return _WHITESPACE_PATTERN.sub(" ", without_tags).strip()
