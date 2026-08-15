#!/usr/bin/env python3
"""Run a reproducible Gemma 4 inference and LoRA smoke test on Apple Silicon."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TypedDict

MODEL_ID = "mlx-community/gemma-4-e2b-it-4bit"


class StepResult(TypedDict):
    name: str
    command: list[str]
    elapsed_seconds: float
    returncode: int
    log: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=MODEL_ID)
    parser.add_argument("--config", default="configs/training/mlx-gemma-4-e2b-smoke.yaml")
    parser.add_argument("--skip-inference", action="store_true")
    parser.add_argument("--skip-training", action="store_true")
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: Path, root: Path) -> dict[str, object]:
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def sanitize_command(command: list[str], root: Path) -> list[str]:
    home = str(Path.home())
    root_text = str(root)
    sanitized = [Path(command[0]).name]
    for argument in command[1:]:
        sanitized.append(argument.replace(root_text, "<repo>").replace(home, "<home>"))
    return sanitized


def git_metadata(root: Path) -> dict[str, object]:
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    dirty = bool(
        subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    )
    return {"commit": commit, "dirty": dirty}


def package_versions(names: tuple[str, ...]) -> dict[str, str]:
    versions: dict[str, str] = {}
    for name in names:
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = "not-installed"
    return versions


def runtime_metadata() -> dict[str, object]:
    import mlx.core as mx
    import psutil

    return {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "machine": platform.machine(),
        "mlx_device": str(mx.default_device()),
        "metal_available": mx.metal.is_available(),
        "memory_bytes": psutil.virtual_memory().total,
        "packages": package_versions(("mlx", "mlx-lm", "huggingface-hub", "pyyaml")),
    }


def prepare_model(model_id: str) -> tuple[Path, dict[str, object]]:
    from huggingface_hub import HfApi, snapshot_download

    info = HfApi().model_info(model_id)
    if not info.sha:
        raise RuntimeError(f"Hugging Face did not return an immutable revision for {model_id}")

    snapshot = Path(snapshot_download(model_id, revision=info.sha))
    tracked_files = []
    for name in ("config.json", "tokenizer.json", "tokenizer_config.json", "chat_template.jinja"):
        path = snapshot / name
        if path.exists():
            tracked_files.append(
                {
                    "path": name,
                    "sha256": sha256_file(path),
                    "size_bytes": path.stat().st_size,
                }
            )

    card = info.card_data
    return snapshot, {
        "id": model_id,
        "revision": info.sha,
        "license": getattr(card, "license", None) if card else None,
        "metadata_files": tracked_files,
    }


def run_step(
    name: str,
    command: list[str],
    cwd: Path,
    log_path: Path,
) -> StepResult:
    print(f"\n$ {' '.join(sanitize_command(command, cwd))}", flush=True)
    started = time.monotonic()
    with log_path.open("w", encoding="utf-8") as log:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        assert process.stdout is not None
        for line in process.stdout:
            print(line, end="", flush=True)
            log.write(line)
        returncode = process.wait()

    return {
        "name": name,
        "command": sanitize_command(command, cwd),
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "returncode": returncode,
        "log": log_path.relative_to(cwd).as_posix(),
    }


def sanitize_adapter_config(path: Path, model_id: str, revision: str) -> None:
    config = json.loads(path.read_text(encoding="utf-8"))
    config["model"] = model_id
    config["model_revision"] = revision
    config["adapter_path"] = "adapters"
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    bin_dir = Path(sys.executable).parent
    generate = bin_dir / "mlx_lm.generate"
    lora = bin_dir / "mlx_lm.lora"

    if platform.system() != "Darwin" or platform.machine() != "arm64":
        raise SystemExit("This smoke test requires an Apple Silicon Mac.")
    for executable in (generate, lora):
        if not executable.exists():
            raise SystemExit(
                "Install the environment with: "
                "uv sync --no-editable --extra dev --extra mac-training"
            )

    config_path = root / args.config
    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir = root / "artifacts" / "mlx-smoke" / run_id
    adapter_dir = run_dir / "adapters"
    logs_dir = run_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=False)
    adapter_relative = adapter_dir.relative_to(root)
    steps: list[StepResult] = []

    dataset_files = sorted((root / "examples" / "training-smoke").glob("*.jsonl"))
    manifest: dict[str, Any] = {
        "schema_version": "0.1.0",
        "run_id": run_id,
        "state": "experimental",
        "status": "running",
        "code": git_metadata(root),
        "configuration": file_record(config_path, root),
        "dataset": {
            "kind": "synthetic-smoke-only",
            "files": [file_record(path, root) for path in dataset_files],
        },
        "environment": runtime_metadata(),
        "lockfile": file_record(root / "uv.lock", root),
        "steps": steps,
        "artifacts": [],
    }
    manifest_path = run_dir / "report.json"
    return_code = 1

    try:
        model_path, model_record = prepare_model(args.model)
        manifest["model"] = model_record
        pinned_model = str(model_path)

        if not args.skip_inference:
            step = run_step(
                "base-inference",
                [
                    str(generate),
                    "--model",
                    pinned_model,
                    "--prompt",
                    "Responda somente com: ambiente MLX operacional.",
                    "--max-tokens",
                    "24",
                    "--temp",
                    "0",
                    "--seed",
                    "42",
                ],
                root,
                logs_dir / "base-inference.log",
            )
            steps.append(step)
            if step["returncode"]:
                raise RuntimeError("Base inference failed; inspect its log.")

        if not args.skip_training:
            step = run_step(
                "lora-training",
                [
                    str(lora),
                    "--config",
                    args.config,
                    "--model",
                    pinned_model,
                    "--adapter-path",
                    adapter_relative.as_posix(),
                ],
                root,
                logs_dir / "lora-training.log",
            )
            steps.append(step)
            if step["returncode"]:
                raise RuntimeError("LoRA training failed; inspect its log.")

            adapter_config = adapter_dir / "adapter_config.json"
            sanitize_adapter_config(
                adapter_config,
                args.model,
                str(model_record["revision"]),
            )
            step = run_step(
                "adapter-reload",
                [
                    str(generate),
                    "--model",
                    pinned_model,
                    "--adapter-path",
                    adapter_relative.as_posix(),
                    "--prompt",
                    "Classifique como NO_CHANGE: renome de variável sem mudança de comportamento.",
                    "--max-tokens",
                    "48",
                    "--temp",
                    "0",
                    "--seed",
                    "42",
                ],
                root,
                logs_dir / "adapter-reload.log",
            )
            steps.append(step)
            if step["returncode"]:
                raise RuntimeError("The trained adapter could not be reloaded; inspect its log.")

        manifest["artifacts"] = [
            file_record(path, root) for path in sorted(adapter_dir.glob("*")) if path.is_file()
        ]
        manifest["status"] = "passed"
        return_code = 0
    except Exception as exc:
        manifest["status"] = "failed"
        manifest["error"] = {"type": type(exc).__name__, "message": str(exc)}
    finally:
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"\nReport: {manifest_path}", flush=True)

    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
