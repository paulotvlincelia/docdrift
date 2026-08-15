# Governance

DocDrift is currently a maintainer-led early-stage project. Governance is designed to stay lightweight while decisions, datasets, and releases remain auditable.

## Roles

### Community members

Anyone who uses DocDrift, joins Discussions, reports a problem, or shares feedback.

### Contributors

People whose code, data methodology, evaluation cases, research, design, or documentation has been accepted into the project.

### Reviewers

Trusted contributors who regularly review a specific area such as schemas, dataset governance, training, evaluation, security, or integrations.

### Maintainers

People responsible for repository administration, releases, security response, final merge decisions, and enforcement of project policies. The initial maintainer is Paulo Tavares (`@paulotvlincelia`).

## Decision process

- Small implementation decisions happen in pull requests.
- Product and research directions begin in Discussions or issues.
- Changes to durable architecture or contracts require an ADR.
- Dataset releases require provenance, licensing, privacy, and evaluation review.
- Model releases require a completed model card and reproducible evaluation report.

Maintainers seek rough consensus. When consensus cannot be reached, the responsible maintainer records the decision and rationale publicly. Decisions can be revisited when new evidence appears.

## Becoming a reviewer or maintainer

Sustained, constructive contributions matter more than commit count. Candidates should demonstrate sound judgment, respect for data governance, reliable review, and alignment with the Code of Conduct.

Existing maintainers nominate and approve new reviewers and maintainers. As the community grows, this process will evolve through an ADR.

## Dataset governance

Requests to correct or remove dataset material take priority over feature work. Releases must preserve source provenance and provide a documented removal path. Public data is not automatically appropriate training data.

## Conflicts of interest

Reviewers must disclose relevant personal, employer, research, or financial conflicts and recuse themselves when impartial review is not possible.
