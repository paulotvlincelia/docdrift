"""Validation helpers for the versioned input and output contracts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = PROJECT_ROOT / "schemas"
if not SCHEMA_ROOT.is_dir():
    SCHEMA_ROOT = Path(__file__).resolve().parent.parent / "gemma_doc_sync_contracts"

SCHEMAS = {
    "change-envelope": SCHEMA_ROOT / "change-envelope.schema.json",
    "documentation-sync-result": SCHEMA_ROOT / "documentation-sync-result.schema.json",
}


def load_json(path: Path) -> Any:
    """Load a UTF-8 JSON document."""
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_document(document: Any, schema_name: str) -> None:
    """Validate a document against one of the repository schemas."""
    schema_path = SCHEMAS[schema_name]
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(document)
