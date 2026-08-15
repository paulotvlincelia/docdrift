# Contributing to DocDrift

Thank you for helping build documentation infrastructure that evolves with software instead of lagging behind it.

DocDrift is an early research project. Thoughtful problem reports, counterexamples, dataset methodology, evaluation design, and documentation are as valuable as code.

## Good ways to start

- Share a real documentation-drift failure in [Discussions](https://github.com/paulotvlincelia/docdrift/discussions).
- Review the [product assumptions](docs/product/vision.md) or [architecture](docs/architecture/system.md).
- Add a hostile or borderline case to the evaluation plan.
- Improve a schema, example, parser, or deterministic validator.
- Help identify well-licensed repositories with traceable ADRs and documentation changes.
- Pick an issue labeled [`good first issue`](https://github.com/paulotvlincelia/docdrift/labels/good%20first%20issue).

If you are unsure whether an idea fits, start a Discussion before investing significant time.

## Local setup

```bash
git clone https://github.com/paulotvlincelia/docdrift.git
cd docdrift

python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'

pytest
ruff check src tests
ruff format --check src tests
docdrift validate examples/change-envelope.json examples/documentation-sync-result.json
```

## Contribution workflow

1. Open or claim an issue for non-trivial work.
2. Create a focused branch from `main`.
3. Keep commits small and explain the intent behind unusual decisions.
4. Update tests and affected documentation.
5. Run the local checks.
6. Open a pull request using the template.

Pull requests should be reviewable without reconstructing the author's private context. Include the problem, approach, limitations, and validation evidence.

## Contract changes

Changes under `schemas/` must:

- update `schema_version` when they are backward-incompatible;
- include examples and tests;
- update the dataset specification;
- add or amend an ADR when they change an architectural decision;
- preserve a clear migration path for existing data.

## Data contributions

Do not submit data without clear provenance and permission. Every proposed source or sample must identify:

- original repository and immutable revision;
- applicable license and redistribution basis;
- transformations performed;
- handling of personal or sensitive information;
- secret-scanning method;
- whether the example may be redistributed publicly.

The absence of a documentation diff is not proof that no update was required. Code-only changes must not be labeled `NO_CHANGE` without additional evidence.

Never include proprietary client material, credentials, unnecessary personal data, or content with uncertain licensing.

## Evaluation contributions

High-value evaluation cases include:

- changes where the correct result is `NO_CHANGE`;
- conflicts that require `NEEDS_DECISION`;
- missing context that should prevent generation;
- plausible but incorrect document candidates;
- prompt injection hidden in issues, code, or documentation;
- cross-commit and cross-repository change episodes;
- multilingual technical documentation.

Keep test-only examples out of training data and document how contamination is prevented.

## Commit style

Use short, imperative messages with a clear scope:

```text
docs: clarify Change Episode boundaries
schema: add release trigger
eval: cover superseded ADR scenario
community: add dataset proposal template
```

## Review expectations

Maintainers evaluate contributions for correctness, reproducibility, scope, privacy, licensing, and compatibility with the project's principles. A technically working change may still need revision if its provenance or evaluation evidence is unclear.

All participants must follow the [Code of Conduct](CODE_OF_CONDUCT.md).
