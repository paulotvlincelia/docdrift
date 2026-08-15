#!/usr/bin/env python3
"""Run the packaged Gemma 4 inference and LoRA smoke workflow."""

from pathlib import Path

from docdrift.mlx_smoke import main

if __name__ == "__main__":
    raise SystemExit(main(repo_root=Path(__file__).resolve().parents[1]))
