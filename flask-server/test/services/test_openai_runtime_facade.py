import pytest

pytest.importorskip("openai")

import services.openai_runtime_facade as facade


class DummyResponses:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class DummyAssistants:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


def test_get_openai_runtime_responses(monkeypatch):
    monkeypatch.setattr(facade, "OPENAI_RUNTIME", "responses")
    assert facade.get_openai_runtime() == "responses"


def test_get_openai_runtime_default_assistants(monkeypatch):
    monkeypatch.setattr(facade, "OPENAI_RUNTIME", "unknown")
    assert facade.get_openai_runtime() == "assistants"


def test_build_openai_agent_uses_responses(monkeypatch):
    monkeypatch.setattr(facade, "OpenAIResponsesService", DummyResponses)
    monkeypatch.setattr(facade, "OpenAIAssistant", DummyAssistants)
    monkeypatch.setattr(facade, "get_openai_runtime", lambda: "responses")

    obj = facade.build_openai_agent("k", assistant_name="x")
    assert isinstance(obj, DummyResponses)


def test_build_openai_agent_uses_assistants(monkeypatch):
    monkeypatch.setattr(facade, "OpenAIResponsesService", DummyResponses)
    monkeypatch.setattr(facade, "OpenAIAssistant", DummyAssistants)
    monkeypatch.setattr(facade, "get_openai_runtime", lambda: "assistants")

    obj = facade.build_openai_agent("k", assistant_name="x")
    assert isinstance(obj, DummyAssistants)


def test_responses_implements_agent_post_process_contract():
    from services.openai_response_service import OpenAIResponsesService

    service = object.__new__(OpenAIResponsesService)
    assert service.pre_process("input") == "input"
    assert service.post_process("output", is_finishing=False) == "output"
