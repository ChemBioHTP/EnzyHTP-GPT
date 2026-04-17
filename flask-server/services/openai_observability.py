#! python3
# -*- encoding: utf-8 -*-
"""Utility helpers for OpenAI runtime observability."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from json import dumps
from logging import Logger
from typing import Any, Dict
from flask import current_app, has_app_context


@dataclass
class OpenAIMeta:
    """Normalized metadata for OpenAI requests and responses."""

    openai_runtime: str
    model: str
    response_id: str | None = None
    conversation_id: str | None = None
    tool_call_count: int = 0
    openai_error_code: str | None = None


def _safe_json(data: Dict[str, Any]) -> str:
    try:
        return dumps(data, ensure_ascii=False, default=str)
    except Exception:
        return str(data)


def log_openai_meta(logger: Logger, event: str, meta: OpenAIMeta, **kwargs) -> None:
    """Log OpenAI metadata as one-line JSON for downstream parsing."""
    payload: Dict[str, Any] = {
        "event": event,
        "openai": asdict(meta),
    }
    if kwargs:
        payload.update(kwargs)
    log_line = _safe_json(payload)
    if has_app_context():
        current_app.logger.info(log_line)
        return
    logger.info(log_line)
