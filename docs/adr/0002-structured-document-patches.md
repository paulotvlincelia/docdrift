# ADR-0002: Patches documentais estruturados

- Status: Aceito
- Data: 2026-08-15

## Contexto

Unified diffs são compactos, mas modelos pequenos podem produzir headers, offsets e contexto incorretos. Reescrever o documento completo dificulta revisão e preservação de autoria.

## Decisão

Usar operações estruturadas `replace`, `insert_before`, `insert_after` e `delete`, ancoradas em texto exato e no hash do documento anterior.

## Consequências

- O runtime consegue validar ambiguidade antes de modificar arquivos.
- O modelo aprende edição mínima.
- Mudanças muito amplas podem exigir várias operações.
- Uma camada determinística poderá converter as operações em unified diff para revisão no Git.
