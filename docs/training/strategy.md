# Estratégia de fine-tuning

## Modelo base

Checkpoint inicial: `google/gemma-4-E2B-it`.

Usaremos a variante instruction-tuned porque a tarefa é seguir um contrato, classificar situações e gerar edição estruturada. A variante base somente será comparada se os experimentos mostrarem que o comportamento prévio do checkpoint `-it` limita o domínio.

O ambiente de treino deve usar `transformers>=5.10.1`, versão mínima indicada na documentação de inferência do Gemma 4 no momento da criação deste repositório. A versão exata será fixada no lockfile de cada experimento reproduzível.

## Hipótese

Um modelo E2B fine-tunado com exemplos de alta qualidade pode superar o checkpoint original em:

- classificação de impacto documental;
- uso disciplinado de evidências;
- produção de patches mínimos e válidos;
- abstenção diante de conflito;
- consistência de formato.

## Baselines obrigatórios

Antes de qualquer treino:

1. checkpoint original com prompt mínimo;
2. checkpoint original com prompt e few-shot;
3. checkpoint original com o mesmo retrieval previsto para produção;
4. heurísticas determinísticas para `NO_CHANGE` e seleção de documentos.

O modelo fine-tunado deve ser comparado com os mesmos inputs e limites de geração.

## Currículo proposto

### Etapa 1 — compreensão de mudanças

Adaptação opcional com dados limpos de diff para classificação e sumarização factual. Esta etapa só será mantida se melhorar o conjunto de avaliação específico.

### Etapa 2 — impact analysis

SFT para produzir decisão, tipos de mudança, documentos impactados, conflitos e evidências, sem gerar patches.

### Etapa 3 — patch generation

SFT condicionado a exemplos `UPDATE`, usando documento anterior e plano de impacto gold.

### Etapa 4 — treino conjunto

Mistura das tarefas com tags explícitas:

```text
<task>analyze_documentation_impact</task>
<task>generate_documentation_patch</task>
```

### Etapa 5 — preferências

Opcionalmente aplicar DPO/ORPO com pares como:

- patch mínimo versus reescrita excessiva;
- abstenção correta versus decisão inventada;
- evidência válida versus justificativa genérica;
- documento correto versus documento apenas semanticamente semelhante.

## Técnica inicial

- QLoRA em 4 bits;
- adapters LoRA em módulos selecionados após inspeção do checkpoint;
- gradient checkpointing;
- treino textual na primeira versão;
- sequências curtas e médias antes de experimentar contextos longos;
- loss apenas nos tokens de saída do assistente;
- seeds e versões de dependências registradas;
- checkpoints escolhidos por métricas da tarefa, não somente training loss.

O suporte a contexto longo não implica treinar no comprimento máximo. O custo de ativação e a distribuição dos exemplos devem orientar o comprimento, inicialmente entre 4K e 16K tokens.

## Configuração inicial

Uma configuração de intenção está em [`configs/training/qlora-gemma-4-e2b.yaml`](../../configs/training/qlora-gemma-4-e2b.yaml). Parâmetros ainda não medidos são marcados como experimentais e devem ser atualizados depois do primeiro profile de memória.

## Mistura de dados

A composição de cada execução deve ser registrada. Ponto inicial para experimentação:

| Classe | Proporção alvo |
|---|---:|
| UPDATE | 45% |
| NO_CHANGE | 25% |
| NEEDS_DECISION | 20% |
| INSUFFICIENT_CONTEXT | 10% |

Essas proporções não representam a produção. Elas aumentam a exposição a comportamentos críticos; a calibração final deve usar uma avaliação com distribuição realista.

## Artefatos de uma execução

- configuração resolvida;
- commit do código;
- versão e hash do dataset;
- checkpoint e revisão do modelo base;
- tokenizer e chat template;
- ambiente de hardware/software;
- logs e curvas;
- adapters/checkpoint final;
- relatório de avaliação;
- model card com limitações.
