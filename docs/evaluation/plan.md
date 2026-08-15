# Plano de avaliação

## Objetivo

Medir se o fine-tuning melhora o sistema na tarefa específica sem degradar segurança, precisão ou capacidade de abstenção.

## Splits

### Repository-disjoint

Nenhum repositório pode aparecer simultaneamente em treino e teste. Forks e mirrors são tratados como o mesmo grupo.

### Temporal holdout

Para alguns repositórios, treinar apenas com episódios anteriores a uma data/release e testar em mudanças posteriores.

### Challenge set

Conjunto pequeno, manual e estável com casos adversariais, conflitos e contexto insuficiente. Não deve ser usado para ajustar prompts repetidamente sem registrar a contaminação.

## Camadas de avaliação

### 1. Validade estrutural

- JSON parseável;
- conformidade com schema;
- enumerações e campos obrigatórios;
- paths e hashes válidos;
- operações de patch aplicáveis.

### 2. Análise de impacto

- macro F1 das quatro decisões;
- recall de `UPDATE`;
- precisão de `NO_CHANGE`;
- recall de `NEEDS_DECISION`;
- F1 multilabel de tipos de mudança;
- recall@k e MRR de documentos impactados.

### 3. Grounding

- precision das referências de evidência;
- percentual de afirmações suportadas;
- taxa de evidências inexistentes;
- taxa de contradição com requisito ou ADR vigente.

### 4. Qualidade do patch

- patch apply rate;
- exact match em operações simples;
- similaridade estrutural com patch gold;
- preservação de conteúdo não afetado;
- completude factual;
- edição mínima;
- avaliação humana pareada.

### 5. Operação

- latência p50/p95;
- memória máxima;
- tokens de entrada e saída;
- taxa de encaminhamento humano;
- aceitação de patches sem edição;
- taxa de rollback ou correção posterior.

## Custos assimétricos

Um falso `NO_CHANGE` pode deixar documentação incorreta. Um falso `UPDATE` cria ruído e reduz confiança. A matriz de custo deve ser configurável, mas inicialmente:

```text
falso NO_CHANGE > patch desnecessário > INSUFFICIENT_CONTEXT correto
decisão inventada em conflito = falha crítica
```

## Cenários mínimos do challenge set

1. requisito mudou e código ainda não;
2. código divergiu legitimamente do ADR;
3. código divergiu acidentalmente;
4. refatoração sem impacto observável;
5. contrato de API mudou sem documentação;
6. ADR substituído ainda é citado;
7. hotfix contradiz runbook;
8. documentação já estava incorreta antes da mudança;
9. mudança distribuída entre múltiplos commits;
10. candidato documental semanticamente semelhante, mas pertencente a outro componente;
11. ausência do documento necessário;
12. prompt injection presente em issue, comentário ou arquivo do repositório.

## Gate para declarar ganho

Uma versão não é promovida apenas por melhorar a média. Ela deve:

- superar o baseline na métrica primária definida para o experimento;
- não aumentar falhas críticas;
- manter validade estrutural próxima de 100%;
- demonstrar ganho em repositórios não vistos;
- passar por revisão humana cega em uma amostra representativa;
- possuir relatório reproduzível.

## Gate de promoção entre backends

Resultados produzidos em MLX, Colab ou CUDA local usam os mesmos splits e contratos, mas não precisam ser idênticos bit a bit. Antes da promoção, o candidato deve:

- ser reproduzido no estágio canônico definido no [modelo operacional](../training/operating-model.md), salvo conversão explicitamente suportada;
- ser carregado e avaliado em processo limpo, separado do estado do treino;
- permanecer dentro das tolerâncias registradas para métricas e falhas críticas;
- registrar backend, acelerador, versões, seeds e hashes no manifest;
- passar por um download de staging e uma inferência de verificação.
