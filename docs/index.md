# Documentação do DocDrift

Esta documentação registra o produto, os contratos e as decisões do projeto. Mudanças que alterem comportamento, dados, treinamento ou critérios de qualidade devem atualizar os documentos correspondentes.

## Produto

- [Visão e escopo](product/vision.md)

## Arquitetura

- [Arquitetura do sistema](architecture/system.md)
- [Enforcement no SDLC](operations/enforcement.md)

## Machine learning

- [Especificação do dataset](dataset/specification.md)
- [Mineração e curadoria](dataset/curation.md)
- [Dataset card (rascunho)](dataset/dataset-card.md)
- [Estratégia de fine-tuning](training/strategy.md)
- [Modelo operacional de treinamento e promoção](training/operating-model.md)
- [Treinamento local em Apple Silicon](training/local-apple-silicon.md)
- [Model card (rascunho)](training/model-card.md)
- [Plano de avaliação](evaluation/plan.md)

## Decisões

- [ADR-0001: Change Episode como unidade do dataset](adr/0001-change-episode-as-dataset-unit.md)
- [ADR-0002: Patches estruturados como saída](adr/0002-structured-document-patches.md)
- [ADR-0003: Gemma 4 E2B como modelo inicial](adr/0003-gemma-4-e2b.md)
- [ADR-0004: contrato backend-neutral e promoção canônica em CUDA](adr/0004-backend-neutral-training-canonical-cuda.md)

## Planejamento

- [Roadmap](roadmap.md)

## Comunidade

- [Como contribuir](../CONTRIBUTING.md)
- [Governança](../GOVERNANCE.md)
- [Suporte](../SUPPORT.md)
- [Segurança](../SECURITY.md)
- [Código de conduta](../CODE_OF_CONDUCT.md)
