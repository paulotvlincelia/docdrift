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

## Modelo operacional de treino, promoção e consumo

DocDrift separa três caminhos para evitar que conveniência local seja confundida com promoção oficial do modelo.

```text
Desenvolvimento local / contributor
    Apple Silicon
        -> MLX-LM
        -> LoRA/QLoRA experimental
        -> smoke tests e evals locais

Promoção canônica
    Colab/CUDA
        -> receita reproduzível de treino
        -> evals oficiais
        -> gates de promoção
        -> Hugging Face

Consumo e QA manual opcional
    artefato promovido
        -> formato compatível de inferência
        -> LM Studio
        -> exploração manual, demo e teste da API local
```

### O que é obrigatório

Para um adapter ou checkpoint ser considerado candidato oficial do projeto, ele deve passar pelo caminho canônico de promoção em CUDA/Colab (ou por outro backend futuramente declarado equivalente), usando configuração versionada, dataset identificado, seed, revisão do modelo base e suíte oficial de avaliação. A publicação no Hugging Face ocorre somente depois desses gates.

O objetivo não é tratar Colab como infraestrutura permanente, mas ter uma referência reproduzível e acessível para colaboradores que não possuam Apple Silicon ou hardware local suficiente. O projeto pode promover outro backend a canônico quando houver equivalência demonstrada e documentação reproduzível.

### O que é suportado, mas não obrigatório

MLX-LM é o caminho de desenvolvimento local para Apple Silicon. Ele pode ser usado para profiling, smoke tests, iteração de hiperparâmetros e até treinos completos quando o colaborador tiver recursos. Resultados MLX são evidência útil, porém não substituem automaticamente a execução canônica antes de uma promoção.

LM Studio fica depois do treino. Ele é uma camada opcional de inferência e QA manual para carregar um artefato compatível, testar prompts, comportamento conversacional e integração via API local. Ele não é parte da receita de fine-tuning do DocDrift e não participa dos gates quantitativos oficiais.

### Por que manter essa separação

- evita acoplar a reprodutibilidade do projeto a um único tipo de hardware;
- permite contribuição local rápida sem rebaixar os critérios de promoção;
- reduz diferenças silenciosas entre backends de treino;
- mantém os resultados oficiais comparáveis;
- permite usar ferramentas de consumo como LM Studio sem confundi-las com o pipeline de pesquisa.

Toda conversão necessária para consumir um adapter promovido no LM Studio deve ser tratada como um artefato derivado e rastreável. A versão publicada no Hugging Face permanece a referência de proveniência do experimento.

## Configuração inicial

Uma configuração de intenção está em [`configs/training/qlora-gemma-4-e2b.yaml`](../../configs/training/qlora-gemma-4-e2b.yaml). Parâmetros ainda não medidos são marcados como experimentais e devem ser atualizados depois do primeiro profile de memória.

O fluxo de desenvolvimento e smoke test em Macs Apple Silicon está documentado em [`local-apple-silicon.md`](local-apple-silicon.md). Ele usa MLX e uma configuração deliberadamente pequena; não substitui a receita CUDA de uma execução oficial.

O ciclo completo de experimento, reprodução canônica, avaliação e publicação está definido no [`modelo operacional`](operating-model.md). Colab/CUDA é o executor de referência inicial para candidatos a release, mas o contrato é backend-neutral e permite experimentos locais. Adapters MLX não são promovidos como adapters PEFT sem reprodução ou conversão validada.

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
