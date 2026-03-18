#! python3
# -*- encoding: utf-8 -*-
"""Facade to select OpenAI runtime implementation."""

from __future__ import annotations

from typing import Any

from config import OPENAI_RUNTIME
from .openai_response_service import OpenAIResponsesService
from .openai_service import OpenAIAssistant

RUNTIME_ASSISTANTS = "assistants"
RUNTIME_RESPONSES = "responses"


def get_openai_runtime() -> str:
    if (OPENAI_RUNTIME == RUNTIME_RESPONSES):
        return RUNTIME_RESPONSES
    return RUNTIME_ASSISTANTS


def build_openai_agent(*args: Any, **kwargs: Any):
    """Build an OpenAI agent implementation based on runtime config."""
    if (get_openai_runtime() == RUNTIME_RESPONSES):
        return OpenAIResponsesService(*args, **kwargs)
    return OpenAIAssistant(*args, **kwargs)


class OpenAIRuntimeFacade:
    """Convenient namespace for runtime-related helpers."""

    @staticmethod
    def runtime() -> str:
        return get_openai_runtime()

    @staticmethod
    def build(*args: Any, **kwargs: Any):
        return build_openai_agent(*args, **kwargs)
