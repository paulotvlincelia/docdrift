from pathlib import Path

from docdrift.validation import load_json, validate_document

ROOT = Path(__file__).resolve().parents[1]


def test_change_envelope_example_matches_schema() -> None:
    document = load_json(ROOT / "examples" / "change-envelope.json")
    validate_document(document, "change-envelope")


def test_sync_result_example_matches_schema() -> None:
    document = load_json(ROOT / "examples" / "documentation-sync-result.json")
    validate_document(document, "documentation-sync-result")
