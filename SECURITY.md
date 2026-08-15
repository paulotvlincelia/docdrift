# Security Policy

DocDrift processes code, requirements, architectural decisions, and documentation. These inputs may be sensitive or intentionally malicious, so security is part of the core design rather than a deployment afterthought.

## Reporting a vulnerability

Do not open a public issue for vulnerabilities, leaked data, exposed secrets, or bypasses that could produce unauthorized documentation changes.

Until a dedicated private reporting address is published, use GitHub's private vulnerability reporting feature for this repository. Include reproduction steps, affected revisions, impact, and any suggested mitigation.

## Relevant security issues

- prompt injection from issues, comments, code, or documentation;
- bypass of forbidden paths or repository policy;
- patch application against the wrong revision or hash;
- private content exposed through datasets, logs, or model artifacts;
- secrets or unnecessary personal information retained during mining;
- poisoned datasets, adapters, or evaluation artifacts;
- untrusted repository content executed as code or instructions;
- fabricated evidence or gate results;
- cross-tenant or cross-repository context leakage.

## Expected deployment controls

- validate schemas, paths, hashes, and patch applicability;
- treat repository content as untrusted evidence, never runtime instructions;
- scan and redact data before persistence;
- pin model, dependency, dataset, and code revisions;
- verify provenance and integrity of downloaded artifacts;
- start integrations in non-blocking observation mode;
- require human review for conflicts and high-impact changes.

Security support commitments and version coverage will be added with the first release.
