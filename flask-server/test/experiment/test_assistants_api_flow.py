from types import SimpleNamespace
from json import loads

from experiment.views import AssistantsApi
from experiment import views as experiment_views


class _ExperimentStub:
    def __init__(
        self,
        messages,
        question_session_id="conv_qa",
        scientific_question="",
        chat_messages=None,
        experiment_id="exp-test",
    ):
        self._messages = messages
        self._question_session_id = question_session_id
        self.scientific_question = scientific_question
        self.chat_messages = chat_messages if chat_messages is not None else list()
        self.id = experiment_id
        self.updated_mappers = []

    def get_question_analyzer_session_id(self, runtime=None):
        _ = runtime
        return self._question_session_id

    def get_messages_by_session_id(self, session_id):
        _ = session_id
        return list(self._messages)

    def update_attributes(self, mapper):
        self.updated_mappers.append(mapper)
        for key, value in mapper.items():
            setattr(self, key, value)
        return list(mapper.keys()), [], [], ""

    def get_latest_assistant_output(self, assistant_type=None):
        _ = assistant_type
        return "qa-local-latest"


class _QuestionSummarizerStub:
    def __init__(self, openai_secret_key, conversation_mode, experiment, model=None, base_url=None):
        _ = openai_secret_key
        _ = conversation_mode
        _ = model
        _ = base_url
        self.experiment = experiment
        self.prompt_seen = None

    def ask_gpt(self, prompt):
        self.prompt_seen = prompt
        return True, 200, "normalized scientific question"


def test_get_scientific_question_prefers_local_messages(monkeypatch):
    experiment = _ExperimentStub(messages=[{"role": "assistant", "text_value": "qa output"}])
    user = SimpleNamespace(openai_secret_key="sk-test")

    def _unexpected_remote_fetch(*args, **kwargs):
        raise AssertionError("Remote fetch should not be used when local session messages exist")

    monkeypatch.setattr(experiment_views, "QuestionSummarizerAssistant", _QuestionSummarizerStub)
    monkeypatch.setattr(
        experiment_views.OpenAIAssistant,
        "get_thread_messages",
        staticmethod(_unexpected_remote_fetch),
    )

    scientific_question = AssistantsApi.get_scientific_question(user=user, experiment=experiment)

    assert scientific_question == "normalized scientific question"
    assert experiment.scientific_question == "normalized scientific question"
    assert experiment.updated_mappers[-1] == {"scientific_question": "normalized scientific question"}


def test_get_scientific_question_falls_back_to_latest_local_output(monkeypatch):
    experiment = _ExperimentStub(messages=[], question_session_id="conv_qa", scientific_question="")
    user = SimpleNamespace(openai_secret_key="sk-test")

    monkeypatch.setattr(
        experiment_views.OpenAIAssistant,
        "get_thread_messages",
        staticmethod(lambda openai_secret_key, thread_id, base_url=None: (False, [])),
    )

    scientific_question = AssistantsApi.get_scientific_question(user=user, experiment=experiment)

    assert scientific_question == "qa-local-latest"
    assert experiment.scientific_question == "qa-local-latest"
    assert experiment.updated_mappers[-1] == {"scientific_question": "qa-local-latest"}


def test_get_scientific_question_uses_full_local_qa_transcript_across_sessions(monkeypatch):
    class _CaptureSummarizer(_QuestionSummarizerStub):
        prompt_seen = None

        def ask_gpt(self, prompt):
            _CaptureSummarizer.prompt_seen = prompt
            return True, 200, "normalized scientific question"

    experiment = _ExperimentStub(
        messages=[{"role": "assistant", "text_value": "only-latest-session-message"}],
        question_session_id="resp_qa_2",
        chat_messages=[
            {"role": "user", "text_value": "study catalytic effect for substrate X", "assistant_type": 0, "session_id": "resp_qa_1"},
            {"role": "assistant", "text_value": "please provide more details", "assistant_type": 0, "session_id": "resp_qa_1"},
            {"role": "user", "text_value": "focus on kcat and pocket gating", "assistant_type": 0, "session_id": "resp_qa_2"},
            {"role": "assistant", "text_value": "understood", "assistant_type": 0, "session_id": "resp_qa_2"},
            {"role": "assistant", "text_value": "metrics stage content", "assistant_type": 1, "session_id": "resp_metrics_1"},
        ],
    )
    user = SimpleNamespace(openai_secret_key="sk-test")

    monkeypatch.setattr(experiment_views, "QuestionSummarizerAssistant", _CaptureSummarizer)

    scientific_question = AssistantsApi.get_scientific_question(user=user, experiment=experiment)

    assert scientific_question == "normalized scientific question"
    prompt_messages = loads(_CaptureSummarizer.prompt_seen)
    assert len(prompt_messages) == 4
    assert [item["role"] for item in prompt_messages] == ["user", "assistant", "user", "assistant"]
    assert any("kcat" in item["text_value"] for item in prompt_messages)
