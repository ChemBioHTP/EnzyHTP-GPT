from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load_migration_module():
    module_path = Path(__file__).resolve().parents[2] / "dev-tools" / "migrate_thread_to_conversation.py"
    spec = spec_from_file_location("migrate_thread_to_conversation", module_path)
    module = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_default_db_name_from_uri_prefers_path_name():
    module = _load_migration_module()

    assert module._default_db_name_from_uri("mongodb://localhost:27017/enzyhtp_gpt") == "enzyhtp_gpt"


def test_default_db_name_from_uri_falls_back_when_path_missing():
    module = _load_migration_module()

    assert module._default_db_name_from_uri("mongodb://localhost:27017") == "enzyhtp_gpt"


def test_build_update_payload_for_legacy_thread_record():
    module = _load_migration_module()

    payload = module._build_update_payload({
        "id": "exp1",
        "current_thread_id": "thread_123",
        "thread_id_list": ["thread_123"],
    })

    assert payload == {
        "current_conversation_id": None,
        "conversation_id_list": [],
        "openai_runtime": "assistants_legacy",
    }


def test_build_update_payload_for_new_record_defaults_to_responses():
    module = _load_migration_module()

    payload = module._build_update_payload({
        "id": "exp2",
    })

    assert payload == {
        "current_conversation_id": None,
        "conversation_id_list": [],
        "openai_runtime": "responses",
    }


def test_build_update_payload_is_idempotent_when_fields_exist():
    module = _load_migration_module()

    payload = module._build_update_payload({
        "id": "exp3",
        "current_conversation_id": "conv_1",
        "conversation_id_list": ["conv_1"],
        "openai_runtime": "responses",
    })

    assert payload == {}
