#! python3
# -*- encoding: utf-8 -*-
"""Check current OpenAI runtime and installed SDK version."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if (str(PROJECT_ROOT) not in sys.path):
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    runtime = os.environ.get("OPENAI_RUNTIME", "assistants").strip().lower()
    payload = {
        "configured_runtime": runtime,
        "effective_runtime": runtime,
        "sdk_version": None,
        "sdk_importable": False,
        "services_importable": False,
    }

    try:
        import openai  # pylint: disable=import-outside-toplevel

        payload["sdk_importable"] = True
        payload["sdk_version"] = getattr(openai, "__version__", None)
    except Exception as exc:
        payload["sdk_error"] = str(exc)

    try:
        from services import get_openai_runtime  # pylint: disable=import-outside-toplevel

        payload["services_importable"] = True
        payload["effective_runtime"] = get_openai_runtime()
    except Exception as exc:
        payload["services_error"] = str(exc)

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
