# ADR-0003: Gemma 4 E2B como modelo inicial

- Status: Aceito
- Data: 2026-08-15

## Contexto

O projeto busca um modelo aberto, especializado e executável em infraestrutura controlada. A tarefa exige compreensão de código, instruções estruturadas e contexto amplo, mas não deve depender de um modelo de fronteira em produção.

## Decisão

Usar `google/gemma-4-E2B-it` como checkpoint inicial e QLoRA como primeira técnica de adaptação.

## Consequências

- O escopo das tarefas e o contrato de contexto precisam ser disciplinados para um modelo E2B.
- Baselines devem demonstrar se o modelo possui capacidade suficiente antes de expandir o dataset.
- A arquitetura permanece independente do checkpoint; um modelo alternativo pode ser comparado sem alterar os contratos.
- A configuração definitiva de LoRA depende de inspeção do checkpoint e profiling de memória.
