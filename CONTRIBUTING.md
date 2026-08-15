# Contribuindo

Obrigado pelo interesse em melhorar o Gemma Documentation Synchronizer. Nesta fase, as contribuições mais úteis são casos reais anonimizados, revisão dos contratos, heurísticas de mineração e cenários adversariais de avaliação.

## Ambiente local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
ruff check src tests
ruff format --check src tests
```

## Fluxo de contribuição

1. Abra uma issue descrevendo a mudança, exceto para correções pequenas e evidentes.
2. Crie uma branch curta a partir de `main`.
3. Atualize testes e documentação afetada.
4. Execute as validações locais.
5. Abra um pull request descrevendo impacto em dataset, modelo, schemas e documentação.

## Mudanças de contrato

Alterações em `schemas/` devem:

- atualizar `schema_version` quando incompatíveis;
- incluir exemplos e testes;
- atualizar a especificação do dataset;
- registrar uma ADR quando modificarem uma decisão arquitetural.

## Contribuições de dados

Não envie dados sem proveniência ou permissão clara. Toda contribuição deve declarar:

- fonte e revisão original;
- licença aplicável;
- transformações realizadas;
- presença e tratamento de dados pessoais;
- método de remoção de secrets;
- permissão para redistribuição.

Dados proprietários, credenciais, PII desnecessária ou conteúdo cuja licença seja incerta serão recusados.

## Commits

Prefira commits pequenos, com mensagem no imperativo e escopo claro. Exemplos:

```text
docs: clarify Change Episode boundaries
schema: add release trigger
eval: cover superseded ADR scenario
```

## Conduta

Discussões devem ser técnicas, respeitosas e centradas em evidências reproduzíveis. Um código de conduta formal será adotado antes da primeira release pública.
