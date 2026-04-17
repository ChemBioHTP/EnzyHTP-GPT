from types import SimpleNamespace

import pytest

pytest.importorskip("openai")

from services.openai_response_service import OpenAIResponsesService, ResponseRunError


class DummyClient:
    api_key = "sk-valid"


def test_ask_gpt_maps_response_run_error(monkeypatch):
    service = object.__new__(OpenAIResponsesService)
    service.client = DummyClient()
    service.model = "gpt-4o"
    service.conversation_id = "conv_1"
    service.conversation_mode = False
    service.latest_response_id = None
    service.latest_tool_call_result = {}

    monkeypatch.setattr(service, "_create_response", lambda **_kwargs: SimpleNamespace(conversation="conv_1"))
    monkeypatch.setattr(service, "_run_tool_loop", lambda _response: (_ for _ in ()).throw(ResponseRunError("tool_loop_limit", "boom")))

    is_valid, status_code, message = service.ask_gpt("hi")

    assert is_valid is False
    assert status_code == 500
    assert "OpenAI response run failed" in message


def test_ask_gpt_returns_default_key_error():
    service = object.__new__(OpenAIResponsesService)
    service.client = SimpleNamespace(api_key="5511667")

    is_valid, status_code, message = service.ask_gpt("hi")

    assert is_valid is False
    assert status_code == 500
    assert "Secret Key does not exist" in message
