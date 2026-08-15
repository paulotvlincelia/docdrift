import hashlib
import json
import sys
from pathlib import Path

import pytest

from scripts.run_mlx_smoke import parse_args, sanitize_adapter_config, sanitize_command, sha256_file


def test_parse_args_rejects_empty_smoke(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["run_mlx_smoke.py", "--skip-inference", "--skip-training"],
    )

    with pytest.raises(SystemExit) as exc_info:
        parse_args()

    assert exc_info.value.code == 2


def test_sha256_file(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.bin"
    artifact.write_bytes(b"docdrift")

    assert sha256_file(artifact) == hashlib.sha256(b"docdrift").hexdigest()


def test_sanitize_command_hides_local_paths(tmp_path: Path) -> None:
    command = [str(tmp_path / ".venv/bin/tool"), "--output", str(tmp_path / "artifact")]

    sanitized = sanitize_command(command, tmp_path)

    assert sanitized == ["tool", "--output", "<repo>/artifact"]


def test_sanitize_adapter_config_removes_local_paths(tmp_path: Path) -> None:
    path = tmp_path / "adapter_config.json"
    path.write_text(
        json.dumps({"model": "/private/cache/model", "adapter_path": "/private/run/adapters"}),
        encoding="utf-8",
    )

    sanitize_adapter_config(path, "owner/model", "abc123")

    assert json.loads(path.read_text(encoding="utf-8")) == {
        "model": "owner/model",
        "model_revision": "abc123",
        "adapter_path": "adapters",
    }
