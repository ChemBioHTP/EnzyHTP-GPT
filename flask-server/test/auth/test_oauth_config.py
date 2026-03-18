from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load_oauth_config_module():
    module_path = Path(__file__).resolve().parents[2] / "auth" / "oauth_config.py"
    module_spec = spec_from_file_location("oauth_config_for_test", str(module_path))
    oauth_config = module_from_spec(module_spec)
    module_spec.loader.exec_module(oauth_config)
    return oauth_config


def test_oauth_provider_cfg_is_lazy_loaded(monkeypatch):
    called = {"count": 0}

    class DummyResponse:
        status_code = 200

        @staticmethod
        def json():
            return {"authorization_endpoint": "https://example.com/auth"}

    def fake_get(*_args, **_kwargs):
        called["count"] += 1
        return DummyResponse()

    monkeypatch.setattr("requests.get", fake_get)

    oauth_config = _load_oauth_config_module()
    assert called["count"] == 0

    provider_cfg = oauth_config.get_provider_cfg("GOOGLE")
    assert called["count"] == 1
    assert provider_cfg.get("authorization_endpoint") == "https://example.com/auth"
