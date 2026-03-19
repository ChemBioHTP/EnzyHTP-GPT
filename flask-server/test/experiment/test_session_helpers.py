from experiment.models import Experiment


def _build_experiment_stub():
    experiment = object.__new__(Experiment)
    experiment.id = "exp_stub"
    experiment.thread_id_list = []
    experiment.current_thread_id = ""
    experiment.conversation_id_list = []
    experiment.current_conversation_id = ""
    experiment.openai_runtime = "assistants"
    experiment.chat_messages = []
    experiment.current_assistant_type = 0

    def _fake_update_attributes(mapper, editable_attrs=None):
        _ = editable_attrs
        for key, value in mapper.items():
            setattr(experiment, key, value)
        return list(mapper.keys()), [], [], ""

    experiment.update_attributes = _fake_update_attributes
    return experiment


def test_append_session_id_responses_updates_both_tracks():
    experiment = _build_experiment_stub()

    experiment.append_session_id("conv_123", runtime="responses")

    assert experiment.current_conversation_id == "conv_123"
    assert "conv_123" in experiment.conversation_id_list
    assert experiment.current_thread_id == "conv_123"
    assert "conv_123" in experiment.thread_id_list
    assert experiment.openai_runtime == "responses"


def test_get_primary_session_id_prefers_conversation_for_responses():
    experiment = _build_experiment_stub()
    experiment.current_thread_id = "thread_old"
    experiment.current_conversation_id = "conv_new"

    session_id = experiment.get_primary_session_id(runtime="responses")

    assert session_id == "conv_new"


def test_get_question_analyzer_session_id_prefers_chat_metadata():
    experiment = _build_experiment_stub()
    experiment.thread_id_list = ["thread_old_first"]
    experiment.conversation_id_list = ["conv_old_first"]
    experiment.chat_messages = [
        {"role": "assistant", "text_value": "qa output", "assistant_type": 0, "session_id": "conv_qa_1"},
        {"role": "assistant", "text_value": "metrics output", "assistant_type": 1, "session_id": "conv_metrics_1"},
    ]

    session_id = experiment.get_question_analyzer_session_id(runtime="responses")

    assert session_id == "conv_qa_1"


def test_get_question_analyzer_session_id_uses_latest_chat_metadata():
    experiment = _build_experiment_stub()
    experiment.chat_messages = [
        {"role": "assistant", "text_value": "qa output old", "assistant_type": 0, "session_id": "conv_qa_1"},
        {"role": "assistant", "text_value": "metrics output", "assistant_type": 1, "session_id": "conv_metrics_1"},
        {"role": "assistant", "text_value": "qa output new", "assistant_type": 0, "session_id": "conv_qa_2"},
    ]

    session_id = experiment.get_question_analyzer_session_id(runtime="responses")

    assert session_id == "conv_qa_2"


def test_get_latest_assistant_output_with_stage_filter():
    experiment = _build_experiment_stub()
    experiment.chat_messages = [
        {"role": "assistant", "text_value": "qa output 1", "assistant_type": 0},
        {"role": "assistant", "text_value": "metrics output", "assistant_type": 1},
        {"role": "assistant", "text_value": "qa output 2", "assistant_type": 0},
    ]

    latest_qa_output = experiment.get_latest_assistant_output(assistant_type=0)

    assert latest_qa_output == "qa output 2"


def test_get_messages_by_session_id_filters_role_and_session():
    experiment = _build_experiment_stub()
    experiment.chat_messages = [
        {"role": "user", "text_value": "q1", "session_id": "conv_a"},
        {"role": "assistant", "text_value": "a1", "session_id": "conv_a"},
        {"role": "assistant", "text_value": "a2", "session_id": "conv_b"},
        {"role": "system", "text_value": "ignore", "session_id": "conv_a"},
    ]

    messages = experiment.get_messages_by_session_id("conv_a")

    assert messages == [
        {"role": "user", "text_value": "q1"},
        {"role": "assistant", "text_value": "a1"},
    ]


def test_clear_chat_threads_resets_fields_when_some_session_deletions_fail(monkeypatch):
    from experiment import models as experiment_models

    experiment = _build_experiment_stub()
    experiment.current_assistant_type = 2
    experiment.current_thread_id = "thread_current"
    experiment.thread_id_list = ["thread_current", "thread_old"]
    experiment.current_conversation_id = "conv_current"
    experiment.conversation_id_list = ["conv_current", "conv_old"]
    experiment.chat_messages = [{"role": "assistant", "text_value": "foo"}]

    class _FakeLogger:
        def __init__(self):
            self.warning_calls = []

        def warning(self, message):
            self.warning_calls.append(message)

    fake_logger = _FakeLogger()

    def _fake_delete_threads(openai_secret_key, thread_id_list, base_url=None):
        assert openai_secret_key == "sk-test"
        assert base_url is None
        assert set(thread_id_list) == {"thread_current", "thread_old", "conv_current", "conv_old"}
        return False, ["thread_current", "conv_current"]

    monkeypatch.setattr(experiment_models, "_LOGGER", fake_logger)
    monkeypatch.setattr(
        experiment_models.OpenAIAssistant,
        "delete_threads",
        staticmethod(_fake_delete_threads),
    )

    is_successful = experiment.clear_chat_threads("sk-test")

    assert is_successful is False
    assert experiment.current_assistant_type == 0
    assert experiment.current_thread_id is None
    assert experiment.thread_id_list == []
    assert experiment.current_conversation_id is None
    assert experiment.conversation_id_list == []
    assert experiment.chat_messages == []
    assert len(fake_logger.warning_calls) == 1
