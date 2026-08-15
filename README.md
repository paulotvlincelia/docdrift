# Gemma Documentation Synchronizer

Projeto de fine-tuning do `google/gemma-4-E2B-it` para detectar impacto documental e propor atualizações rastreáveis a partir de mudanças ocorridas ao longo do SDLC.

O objetivo não é apenas gerar documentação. O sistema deve manter consistência entre requisitos, ADRs, código, testes e documentos, distinguindo quatro resultados:

- `UPDATE`: há evidência suficiente para atualizar a documentação;
- `NO_CHANGE`: a mudança não produz impacto documental;
- `NEEDS_DECISION`: requisito, decisão e implementação estão em conflito;
- `INSUFFICIENT_CONTEXT`: faltam evidências para decidir com segurança.

## Princípio central

O modelo aprende **como interpretar contexto de projeto**, não memoriza o estado corrente de cada projeto. Hooks e jobs de CI montam um `ChangeEnvelope` com o contexto versionado; o Gemma produz um `DocumentationSyncResult`; validadores determinísticos verificam schema, evidências e aplicabilidade dos patches.

```text
evento upstream
    -> coleta e recuperação de contexto
    -> ChangeEnvelope
    -> Gemma 4 E2B fine-tunado
    -> DocumentationSyncResult
    -> validações determinísticas
    -> PR documental | decisão humana | nenhuma ação
```

## Estrutura do repositório

```text
.
├── configs/                 # Configurações versionadas de dataset, treino e avaliação
├── data/                    # Áreas locais; conteúdo pesado não entra no Git
├── docs/
│   ├── adr/                 # Decisões arquiteturais deste projeto
│   ├── architecture/        # Arquitetura e limites do sistema
│   ├── dataset/             # Contrato, mineração e curadoria do dataset
│   ├── evaluation/          # Estratégia e métricas de avaliação
│   ├── operations/          # Hooks, gates e operação no SDLC
│   ├── product/             # Visão e escopo do produto
│   └── training/            # Estratégia de fine-tuning
├── examples/                # Exemplos pequenos e versionados dos contratos
├── schemas/                 # JSON Schemas de entrada e saída
├── src/gemma_doc_sync/      # Código do pipeline
└── tests/                   # Validação dos contratos e futuras regressões
```

## Começando

Requer Python 3.11 ou superior.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
python3 -m gemma_doc_sync validate examples/change-envelope.json examples/documentation-sync-result.json
```

## Leitura recomendada

1. [Visão do produto](docs/product/vision.md)
2. [Arquitetura do sistema](docs/architecture/system.md)
3. [Especificação do dataset](docs/dataset/specification.md)
4. [Estratégia de curadoria](docs/dataset/curation.md)
5. [Estratégia de fine-tuning](docs/training/strategy.md)
6. [Plano de avaliação](docs/evaluation/plan.md)
7. [Enforcement no SDLC](docs/operations/enforcement.md)
8. [Roadmap](docs/roadmap.md)

## Estado

Fase inicial: contratos, documentação arquitetural e suíte mínima de validação. O próximo marco é construir um baseline reprodutível do checkpoint sem fine-tuning e iniciar a mineração de episódios de mudança.
