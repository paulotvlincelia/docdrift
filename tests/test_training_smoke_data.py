import json
from pathlib import Path

import yaml


def test_mlx_smoke_configuration() -> None:
    config = yaml.safe_load(
        Path("configs/training/mlx-gemma-4-e2b-smoke.yaml").read_text(encoding="utf-8")
    )

    assert config["model"] == "mlx-community/gemma-4-e2b-it-4bit"
    assert config["fine_tune_type"] == "lora"
    assert config["mask_prompt"] is True
    assert config["max_seq_length"] <= 512


def test_smoke_jsonl_is_valid_and_marked_synthetic() -> None:
    data_dir = Path("examples/training-smoke")
    for split in ("train", "valid", "test"):
        rows = [
            json.loads(line)
            for line in (data_dir / f"{split}.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        assert rows
        assert all({"prompt", "completion"} <= row.keys() for row in rows)
        assert all("smoke-" in row["prompt"] for row in rows)
