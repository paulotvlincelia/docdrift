#!/usr/bin/env python3
"""Run a small Gemma 4 inference and LoRA compatibility check on Apple Silicon."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

MODEL_ID = "mlx-community/gemma-4-e2b-it-4bit"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=MODEL_ID)
    parser.add_argument("--config", default="configs/training/mlx-gemma-4-e2b-smoke.yaml")
    parser.add_argument("--skip-inference", action="store_true")
    parser.add_argument("--skip-training", action="store_true")
    return parser.parse_args()


def run(command: list[str], cwd: Path) -> dict[str, object]:
    print(f"\n$ {' '.join(command)}", flush=True)
    started = time.monotonic()
    completed = subprocess.run(command, cwd=cwd, check=False)
    elapsed = round(time.monotonic() - started, 3)
    if completed.returncode:
        raise subprocess.CalledProcessError(completed.returncode, command)
    return {"command": command, "elapsed_seconds": elapsed, "returncode": 0}


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    # Keep the virtual-environment path instead of resolving its Python symlink
    # to the macOS framework installation.
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

    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir = root / "artifacts" / "mlx-smoke" / run_id
    adapter_dir = run_dir / "adapters"
    run_dir.mkdir(parents=True, exist_ok=False)

    report: dict[str, object] = {
        "run_id": run_id,
        "model": args.model,
        "platform": platform.platform(),
        "python": platform.python_version(),
        "steps": [],
    }

    try:
        if not args.skip_inference:
            report["steps"].append(
                run(
                    [
                        str(generate),
                        "--model",
                        args.model,
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
                )
            )

        if not args.skip_training:
            report["steps"].append(
                run(
                    [
                        str(lora),
                        "--config",
                        args.config,
                        "--model",
                        args.model,
                        "--adapter-path",
                        str(adapter_dir),
                    ],
                    root,
                )
            )
    except subprocess.CalledProcessError as exc:
        report["error"] = {"returncode": exc.returncode, "command": exc.cmd}
        return_code = exc.returncode
    else:
        report["status"] = "passed"
        return_code = 0
    finally:
        report_path = run_dir / "report.json"
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"\nReport: {report_path}", flush=True)

    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
