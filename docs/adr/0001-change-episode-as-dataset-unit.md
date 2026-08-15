# ADR-0001: Change Episode como unidade do dataset

- Status: Aceito
- Data: 2026-08-15

## Contexto

Um único commit raramente contém todo o contexto de uma mudança. Requisitos e ADRs podem mudar antes da implementação, e a documentação pode ser atualizada em outro commit ou no fechamento da release.

## Decisão

Usar `Change Episode` como unidade canônica. Um episódio agrega eventos relacionados por pull request, issue, branch, release ou intenção verificada e preserva o estado anterior e posterior relevante.

## Consequências

- A mineração é mais complexa que pares `diff -> texto`.
- O dataset representa melhor o ciclo real.
- Torna-se possível modelar contradições e decisões intermediárias.
- Splits e deduplicação precisam operar no nível do episódio e do repositório.
