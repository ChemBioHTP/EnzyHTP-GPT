from types import SimpleNamespace

import pytest

pytest.importorskip("openai")

from services.openai_response_service import OpenAIResponsesService


def test_run_tool_loop_executes_function_and_submits_output(monkeypatch):
    service = object.__new__(OpenAIResponsesService)
    service.conversation_id = "conv_1"
    service.latest_response_id = None
    service.latest_tool_call_result = {}

    called_payload = {}

    class MappedFunction:
        def __init__(self):
            self.tool_function_callable_kwargs = {"extra": "v"}
            self.mapped_callable = lambda x, extra: (True, f"{x}-{extra}")

    monkeypatch.setattr(service, "_find_function", lambda _name: MappedFunction())

    first_response = SimpleNamespace(conversation="conv_1")
    second_response = SimpleNamespace(conversation="conv_1")

    calls = [
        ("", [{"name": "f", "arguments": '{"x":"1"}', "call_id": "call_1"}]),
        ("done", []),
    ]

    def fake_extract(_response):
        return calls.pop(0)

    def fake_create_response(*, input_payload, conversation_id=None):
        called_payload["input_payload"] = input_payload
        called_payload["conversation_id"] = conversation_id
        return second_response

    monkeypatch.setattr(service, "_extract_text_and_calls", fake_extract)
    monkeypatch.setattr(service, "_create_response", fake_create_response)

    final_response = service._run_tool_loop(first_response)

    assert final_response is second_response
    assert service.latest_tool_call_result["f"] is True
    assert called_payload["conversation_id"] == "conv_1"
    assert called_payload["input_payload"][0]["type"] == "function_call_output"
    assert called_payload["input_payload"][0]["call_id"] == "call_1"
    assert called_payload["input_payload"][0]["output"] == "1-v"


def test_run_tool_loop_raises_on_exceeded_limit(monkeypatch):
    service = object.__new__(OpenAIResponsesService)
    service.conversation_id = "conv_1"
    service.latest_response_id = None
    service.latest_tool_call_result = {}

    monkeypatch.setattr(
        service,
        "_extract_text_and_calls",
        lambda _response: ("", [{"name": "f", "arguments": "{}", "call_id": "call_1"}]),
    )
    monkeypatch.setattr(service, "_create_response", lambda **_kwargs: SimpleNamespace(conversation="conv_1"))
    monkeypatch.setattr(service, "_find_function", lambda _name: None)

    with pytest.raises(Exception) as exc_info:
        service._run_tool_loop(SimpleNamespace(conversation="conv_1"))

    assert "tool-calling loop limit" in str(exc_info.value)


def test_normalize_conversation_id_supports_object():
    service = object.__new__(OpenAIResponsesService)
    normalized = service._normalize_conversation_id(SimpleNamespace(id="conv_obj_1"))
    assert normalized == "conv_obj_1"


def test_create_response_uses_previous_response_id_when_no_conversation(monkeypatch):
    service = object.__new__(OpenAIResponsesService)
    service.model = "gpt-4o"
    service.instructions = "inst"
    service.tools = []
    service.response_tools = []
    service.openai_args_dict = {}
    service.latest_response_id = "resp_prev_1"

    captured = {}

    class DummyResponses:
        @staticmethod
        def create(**kwargs):
            captured.update(kwargs)
            return SimpleNamespace(id="resp_new_1", conversation=None, output=[])

    service.client = SimpleNamespace(responses=DummyResponses())
    service._create_response(input_payload="hello", conversation_id=None)

    assert captured["previous_response_id"] == "resp_prev_1"
    assert "conversation" not in captured


def test_ensure_conversation_context_creates_conversation():
    service = object.__new__(OpenAIResponsesService)
    service.conversation_mode = True
    service.conversation_id = None
    service.client = SimpleNamespace(
        conversations=SimpleNamespace(
            create=lambda: SimpleNamespace(id="conv_new_1")
        )
    )

    service._ensure_conversation_context()

    assert service.conversation_id == "conv_new_1"


def test_ensure_conversation_context_replaces_legacy_thread_id():
    service = object.__new__(OpenAIResponsesService)
    service.conversation_mode = True
    service.conversation_id = "thread_legacy_1"
    service.client = SimpleNamespace(
        conversations=SimpleNamespace(
            create=lambda: SimpleNamespace(id="conv_new_legacy_replaced")
        )
    )

    service._ensure_conversation_context()

    assert service.conversation_id == "conv_new_legacy_replaced"


def test_thread_setter_clears_latest_response_id():
    service = object.__new__(OpenAIResponsesService)
    service.conversation_id = "conv_1"
    service.latest_response_id = "resp_1"

    service.thread = None

    assert service.conversation_id is None
    assert service.latest_response_id is None


def test_ask_gpt_uses_created_conversation_id(monkeypatch):
    service = object.__new__(OpenAIResponsesService)
    service.client = SimpleNamespace(
        api_key="sk-valid",
        conversations=SimpleNamespace(create=lambda: SimpleNamespace(id="conv_new_2")),
    )
    service.model = "gpt-4o"
    service.instructions = "inst"
    service.tools = []
    service.response_tools = []
    service.openai_args_dict = {}
    service.conversation_mode = True
    service.conversation_id = None
    service.latest_response_id = None
    service.latest_tool_call_result = {}
    service.messages = []

    called = {}

    def fake_create_response(*, input_payload, conversation_id=None):
        called["conversation_id"] = conversation_id
        return SimpleNamespace(
            id="resp_2",
            conversation=SimpleNamespace(id="conv_new_2"),
            output=[],
            output_text="done",
        )

    monkeypatch.setattr(service, "_create_response", fake_create_response)
    monkeypatch.setattr(service, "_run_tool_loop", lambda response: response)
    monkeypatch.setattr(service, "_extract_text_and_calls", lambda _response: ("done", []))

    is_valid, status_code, response_text = service.ask_gpt("hello")

    assert is_valid is True
    assert status_code == 200
    assert response_text == "done"
    assert called["conversation_id"] == "conv_new_2"


def test_create_response_normalizes_assistants_function_tool_shape():
    service = object.__new__(OpenAIResponsesService)
    service.model = "gpt-4o"
    service.instructions = "inst"
    service.tools = [{"type": "function", "function": {"name": "f", "parameters": {"type": "object"}}}]
    service.response_tools = OpenAIResponsesService._normalize_tools_for_responses(service.tools)
    service.openai_args_dict = {}
    service.latest_response_id = None

    captured = {}

    class DummyResponses:
        @staticmethod
        def create(**kwargs):
            captured.update(kwargs)
            return SimpleNamespace(id="resp_new_2", conversation=None, output=[])

    service.client = SimpleNamespace(responses=DummyResponses())
    service._create_response(input_payload="hello", conversation_id=None)

    assert captured["tools"][0]["type"] == "function"
    assert captured["tools"][0]["name"] == "f"
    assert "function" not in captured["tools"][0]


def test_create_response_ignores_legacy_assistant_thread_id():
    service = object.__new__(OpenAIResponsesService)
    service.model = "gpt-4o"
    service.instructions = "inst"
    service.tools = []
    service.response_tools = []
    service.openai_args_dict = {}
    service.latest_response_id = "resp_prev_legacy"

    captured = {}

    class DummyResponses:
        @staticmethod
        def create(**kwargs):
            captured.update(kwargs)
            return SimpleNamespace(id="resp_new_legacy", conversation=None, output=[])

    service.client = SimpleNamespace(responses=DummyResponses())
    service._create_response(input_payload="hello", conversation_id="thread_legacy_2")

    assert captured["previous_response_id"] == "resp_prev_legacy"
    assert "conversation" not in captured
