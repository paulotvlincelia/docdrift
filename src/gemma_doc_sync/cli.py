"""Small contract-validation CLI used before the training pipeline exists."""

from __future__ import annotations

import argparse
from pathlib import Path

from gemma_doc_sync.validation import load_json, validate_document


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gemma-doc-sync")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate input and output JSON files")
    validate.add_argument("change_envelope", type=Path)
    validate.add_argument("sync_result", type=Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "validate":
        validate_document(load_json(args.change_envelope), "change-envelope")
        validate_document(load_json(args.sync_result), "documentation-sync-result")
        print("contracts valid")


if __name__ == "__main__":
    main()
