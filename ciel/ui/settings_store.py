from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


DEFAULT_SETTINGS: Dict[str, Any] = {
    "backend": "hf",
    "hf": {
        "lite_model": "phi-3-mini-3.8b",
        "standard_model": "mistral-7b-instruct",
        "science_model": "qwen2.5-7b-instruct",
        "analysis_model": "phi-3-mini-3.8b",
        "validator_model": "mistral-7b-instruct",
        "device": None,
    },
    "gguf": {
        "models_dir": "",
        "lite_model_path": "",
        "standard_model_path": "",
        "science_model_path": "",
        "n_ctx": 2048,
        "n_threads": 4,
        "n_gpu_layers": 0,
        "system_prompt": "",
        "install_profile": "standard",
        "install_url": "",
        "install_sha256": "",
    },
    "chat": {
        "mode": "standard",
        "memory": "echo",
        "profile": "standard",
    },
    "realtime": {
        "timer_interval_ms": 500,
    },
    "window": {
        "width": 1400,
        "height": 800,
    },
}


def _deep_merge(base: Dict[str, Any], patch: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = dict(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def settings_path() -> Path:
    cfg_dir = Path.home() / ".config" / "ciel"
    try:
        cfg_dir.mkdir(parents=True, exist_ok=True)
        return cfg_dir / "control_center.json"
    except Exception:
        return Path.cwd() / "control_center.json"


def load_settings() -> Dict[str, Any]:
    path = settings_path()
    if not path.exists():
        return dict(DEFAULT_SETTINGS)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return dict(DEFAULT_SETTINGS)
        return _deep_merge(DEFAULT_SETTINGS, data)
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(settings: Dict[str, Any]) -> None:
    path = settings_path()
    payload = json.dumps(settings, ensure_ascii=False, indent=2)

    tmp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        tmp_path.write_text(payload, encoding="utf-8")
        tmp_path.replace(path)
    except Exception:
        try:
            path.write_text(payload, encoding="utf-8")
        except Exception:
            return


__all__ = ["DEFAULT_SETTINGS", "load_settings", "save_settings", "settings_path"]
