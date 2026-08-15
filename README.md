# DocDrift

**Documentation that evolves with your system.**

[![CI](https://github.com/paulotvlincelia/docdrift/actions/workflows/ci.yml/badge.svg)](https://github.com/paulotvlincelia/docdrift/actions/workflows/ci.yml)
[![Project status: research preview](https://img.shields.io/badge/status-research%20preview-f59e0b)](docs/roadmap.md)
[![Model: Gemma 4 E2B](https://img.shields.io/badge/model-Gemma%204%20E2B-4285F4)](docs/adr/0003-gemma-4-e2b.md)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB)](pyproject.toml)
[![GitHub Discussions](https://img.shields.io/github/discussions/paulotvlincelia/docdrift)](https://github.com/paulotvlincelia/docdrift/discussions)

DocDrift is an open research and engineering project for keeping **requirements, architectural decisions, code, tests, and documentation aligned throughout the SDLC**.

The project is building a specialized, locally deployable model based on [`google/gemma-4-E2B-it`](https://huggingface.co/google/gemma-4-E2B-it). Given a versioned change episode, the model determines whether documentation must change, identifies the affected documents, surfaces unresolved conflicts, and proposes minimal evidence-backed patches.

> DocDrift is not another documentation generator. It is an experiment in making documentation continuity enforceable.

## Why DocDrift?

Documentation usually starts correct and drifts over time. A feature is adjusted directly in code. An ADR is superseded but remains referenced. A hotfix changes operational behavior. A requirement is renegotiated during implementation. Each individual action makes sense, yet the documentation slowly stops describing the product that actually exists.

Frameworks and agent instructions help only when people remember to use them. DocDrift explores a different approach:

```text
capture every relevant change
    -> reconstruct its SDLC context
    -> reason about documentation impact
    -> validate the proposed update
    -> enforce or escalate the result
```

## The core contract

DocDrift consumes a [`ChangeEnvelope`](schemas/change-envelope.schema.json) containing the relevant requirement, ADR, issue or pull request, code/test/schema diffs, candidate documents, and project policy.

It produces a validated [`DocumentationSyncResult`](schemas/documentation-sync-result.schema.json) with one of four decisions:

| Decision | Meaning |
|---|---|
| `UPDATE` | The documentation is affected and there is enough evidence to propose a patch. |
| `NO_CHANGE` | The change does not alter a documented claim. |
| `NEEDS_DECISION` | Requirements, decisions, implementation, or docs conflict. A human must decide. |
| `INSUFFICIENT_CONTEXT` | The system cannot decide safely with the available evidence. |

This distinction matters. A useful synchronizer must learn when **not** to write.

## How it works

```mermaid
flowchart LR
    A["Requirement, ADR, PR, commit or release"] --> B["Context collection"]
    B --> C["ChangeEnvelope"]
    C --> D["DocDrift-Gemma-4-E2B"]
    D --> E["DocumentationSyncResult"]
    E --> F["Deterministic validation"]
    F --> G{"Decision"}
    G -->|"UPDATE"| H["Documentation patch / PR"]
    G -->|"NO_CHANGE"| I["Auditable pass"]
    G -->|"NEEDS_DECISION"| J["Human decision gate"]
    G -->|"INSUFFICIENT_CONTEXT"| K["Retrieve more context"]
    H --> L["Reviewer feedback"]
    I --> L
    J --> L
    L --> M["Next dataset version"]
```

The model performs semantic judgment and patch generation. Deterministic code remains responsible for event capture, context assembly, schema validation, evidence checks, patch application, permissions, and merge policy.

## Project status

DocDrift is currently a **research preview**. The repository contains the initial architecture, data contracts, curation strategy, training plan, evaluation framework, and validation scaffolding.

It does **not** yet contain a released dataset, fine-tuned adapter, production GitHub integration, or benchmark results. Those artifacts will only be published with reproducible evaluation and documented provenance.

## Repository map

| Path | Purpose |
|---|---|
| [`docs/product`](docs/product/vision.md) | Product vision, users, scope, and success criteria |
| [`docs/architecture`](docs/architecture/system.md) | System boundaries and data flow |
| [`docs/dataset`](docs/dataset/specification.md) | Dataset contract, mining, curation, and dataset card |
| [`docs/training`](docs/training/strategy.md) | Gemma 4 E2B fine-tuning strategy and model card |
| [`docs/evaluation`](docs/evaluation/plan.md) | Metrics, splits, challenge set, and promotion gates |
| [`docs/operations`](docs/operations/enforcement.md) | Hooks, CI gates, rollout modes, and auditability |
| [`docs/adr`](docs/adr) | Architecture Decision Records for DocDrift itself |
| [`schemas`](schemas) | Versioned JSON Schemas for model input and output |
| [`examples`](examples) | Small contract examples used by tests and tooling |
| [`configs`](configs) | Draft dataset, training, and evaluation configurations |

## Quick start

The current CLI validates DocDrift contracts while the training and runtime pipelines are being built.

```bash
git clone https://github.com/paulotvlincelia/docdrift.git
cd docdrift

python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'

pytest
docdrift validate \
  examples/change-envelope.json \
  examples/documentation-sync-result.json
```

Expected output:

```text
contracts valid
```

Apple Silicon contributors can also run the local [MLX smoke test](docs/training/local-apple-silicon.md) to validate Gemma 4 inference and LoRA training on Metal.

## Research plan

DocDrift is being developed in evidence-driven stages:

1. establish zero-shot, few-shot, and deterministic baselines;
2. build a repository-disjoint challenge set;
3. mine license-aware change episodes from public repositories;
4. curate Silver and Gold examples, including negative and abstention cases;
5. fine-tune Gemma 4 E2B with QLoRA;
6. evaluate grounding, impact detection, patch quality, latency, and memory;
7. integrate with GitHub in non-blocking observation mode;
8. graduate carefully toward documentation gates.

Follow the detailed [roadmap](docs/roadmap.md) and join the [Discussions](https://github.com/paulotvlincelia/docdrift/discussions) to help shape priorities.

## Where contributions can have the most impact

DocDrift needs more than model training. Contributions are welcome in:

- mining and reconstructing real change episodes;
- license and provenance tracking;
- ADR, requirement, and documentation parsers;
- repository-aware retrieval and co-change analysis;
- evaluation cases from real SDLC failures;
- patch validation and grounding metrics;
- Portuguese and multilingual technical documentation;
- integrations with GitHub, GitLab, Jira, Linear, and documentation platforms;
- privacy, security, and prompt-injection defenses;
- technical writing and community education.

Start with [CONTRIBUTING.md](CONTRIBUTING.md), browse issues labeled [`good first issue`](https://github.com/paulotvlincelia/docdrift/labels/good%20first%20issue), or propose a research direction in Discussions.

## Principles

- **Evidence before edits.** Every changed claim should point to its source.
- **Abstention is a valid result.** The model must not invent product or architecture decisions.
- **Minimal patches.** Preserve unaffected content, authorship, and document structure.
- **Context is versioned.** Inputs, outputs, model versions, and policies must be reproducible.
- **The model proposes; code verifies.** Enforcement and authorization remain deterministic.
- **Community data deserves governance.** Provenance, licensing, privacy, and removal processes are part of the product.

## Naming

- Project and CLI: **DocDrift** / `docdrift`
- Dataset: **DocDrift-ChangeEpisodes**
- Initial model: **DocDrift-Gemma-4-E2B**

## License

The repository license is being finalized before the first public release. Dataset and model artifacts may require separate licenses and notices based on their sources. Until a license is added, standard copyright restrictions apply.

## Stay involved

- Share a real documentation-drift failure in [Discussions](https://github.com/paulotvlincelia/docdrift/discussions).
- Open a dataset or evaluation proposal using the issue templates.
- Watch or star the repository to follow the first benchmark and fine-tuning experiments.
- Review the [architecture](docs/architecture/system.md) and challenge assumptions early.

If software evolution is continuous, its documentation should be too.
