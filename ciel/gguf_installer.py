from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any, Callable, Optional
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ProgressCallback = Callable[[int, Optional[int]], Any]


def _normalise_sha256(value: str) -> str:
    raw = (value or "").strip().lower()
    if raw.startswith("sha256:"):
        raw = raw.split(":", 1)[1].strip()
    return raw


def sha256_file(path: str | Path, *, chunk_size: int = 1024 * 1024) -> str:
    file_path = Path(path)
    h = hashlib.sha256()
    with file_path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def _default_models_dir() -> Path:
    env_dir = os.getenv("CIEL_GGUF_MODELS_DIR")
    if env_dir:
        return Path(env_dir)
    repo_root = Path(__file__).resolve().parent.parent
    return repo_root / "llm" / "models"


def _infer_filename(url: str) -> str:
    parsed = urlparse(url)
    name = Path(parsed.path or "").name
    if not name:
        return "model.gguf"
    return name


def download_file(
    url: str,
    dest_path: str | Path,
    *,
    expected_sha256: str | None = None,
    progress: ProgressCallback | None = None,
    timeout_s: int = 60,
) -> Path:
    dest = Path(dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)

    expected = _normalise_sha256(expected_sha256) if expected_sha256 else None

    if dest.is_file():
        if expected is None:
            return dest
        try:
            if sha256_file(dest) == expected:
                return dest
        except Exception:
            pass

    tmp_path = dest.with_suffix(dest.suffix + ".tmp")
    try:
        if tmp_path.exists():
            tmp_path.unlink()
    except Exception:
        pass

    h = hashlib.sha256()
    downloaded = 0
    total: Optional[int] = None

    req = Request(url, headers={"User-Agent": "CIEL/gguf-installer"})
    with urlopen(req, timeout=timeout_s) as resp:
        try:
            header = resp.headers.get("Content-Length")
            if header:
                total = int(header)
        except Exception:
            total = None

        with tmp_path.open("wb") as fh:
            while True:
                chunk = resp.read(1024 * 1024)
                if not chunk:
                    break
                fh.write(chunk)
                h.update(chunk)
                downloaded += len(chunk)
                if progress is not None:
                    try:
                        progress(downloaded, total)
                    except Exception:
                        pass

    digest = h.hexdigest()
    if expected is not None and digest != expected:
        try:
            tmp_path.unlink()
        except Exception:
            pass
        raise ValueError(f"SHA256 mismatch: expected {expected}, got {digest}")

    tmp_path.replace(dest)
    return dest


def install_gguf_model(
    *,
    url: str,
    models_dir: str | Path | None = None,
    expected_sha256: str | None = None,
    profile: str | None = None,
    filename: str | None = None,
    progress: ProgressCallback | None = None,
) -> str:
    target_dir = Path(models_dir) if models_dir else _default_models_dir()

    name = (filename or "").strip()
    if not name:
        key = (profile or "").strip().lower()
        if key in {"lite", "standard", "science"}:
            name = f"ciel-{key}.gguf"
        else:
            name = _infer_filename(url)

    if not name.lower().endswith(".gguf"):
        name = name + ".gguf"

    dest = target_dir / name
    path = download_file(url, dest, expected_sha256=expected_sha256, progress=progress)
    return str(path)
