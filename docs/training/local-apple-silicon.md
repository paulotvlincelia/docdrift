# Treinamento local em Apple Silicon

Este caminho existe para desenvolvimento, profiling e smoke tests. As execuções oficiais podem continuar em CUDA/Colab até que equivalência e conversão de adapters sejam demonstradas.

## Papel deste ambiente no pipeline

O fluxo Apple Silicon é um ambiente suportado de desenvolvimento, não o gate canônico de promoção do modelo.

```text
Apple Silicon contributor
    -> MLX-LM
    -> LoRA/QLoRA experimental
    -> smoke tests e evals locais

Candidate for promotion
    -> Colab/CUDA
    -> receita reproduzível
    -> evals oficiais
    -> Hugging Face

Optional manual QA
    -> artefato promovido em formato compatível
    -> LM Studio
    -> inferência, demo e testes locais de comportamento/API
```

Um colaborador com hardware local suficiente pode executar treinos maiores ou completos com MLX-LM. Esses resultados são válidos como experimentos e podem orientar o projeto, mas um artefato só deve ser apresentado como release/candidato oficial depois de passar pelo caminho de promoção definido em [`strategy.md`](strategy.md).

## Instalação

No macOS com Apple Silicon:

```bash
uv sync --no-editable --extra dev --extra mac-training
source .venv/bin/activate
```

As dependências ficam na `.venv`; modelos baixados pelo Hugging Face ficam no cache do usuário e não são versionados pelo Git.

Usamos `--no-editable` neste ambiente porque o Python 3.13.7 ignora o arquivo `.pth` oculto gerado pelo backend Hatch para instalações editáveis. Depois de alterar o pacote `docdrift`, execute novamente o comando de sincronização. Esse contorno não afeta o treinamento MLX.

## Smoke test do Gemma 4 E2B

```bash
.venv/bin/python scripts/run_mlx_smoke.py
```

O comando:

1. baixa ou reutiliza `mlx-community/gemma-4-e2b-it-4bit`;
2. executa uma geração curta na GPU Metal;
3. treina um adapter LoRA por cinco iterações;
4. grava adapter e relatório em `artifacts/mlx-smoke/<run-id>/`.

Os exemplos em `examples/training-smoke/` são sintéticos e servem somente para verificar o pipeline. Eles não devem ser incluídos em resultados de qualidade ou publicados como dataset DocDrift.

## Autenticação no Hugging Face

Checkpoints públicos podem ser baixados sem autenticação, com limites menores. Para publicar ou acessar um repositório privado:

```bash
.venv/bin/hf auth login
.venv/bin/hf auth whoami
```

Informe o token somente no prompt seguro da CLI. Nunca grave tokens em arquivos versionados, comandos de shell, exemplos ou relatórios.

## LM Studio para inferência e QA manual

LM Studio é opcional e fica deliberadamente fora da receita de treinamento. Depois que um modelo ou adapter for aprovado e existir um artefato compatível de inferência, ele pode ser carregado no LM Studio para:

- exploração manual de casos do challenge set;
- demonstrações locais do DocDrift;
- inspeção qualitativa de respostas e abstention behavior;
- testes de integração por API local;
- comparação humana entre modelo base e versão promovida.

Esses testes não substituem as métricas e gates automatizados do projeto. Uma sessão no LM Studio pode revelar regressões ou casos interessantes, mas não é evidência suficiente para promover um modelo.

Se for necessária conversão ou quantização para consumo no LM Studio, o artefato derivado deve registrar sua origem, versão do modelo promovido e processo de conversão. O artefato publicado pelo pipeline oficial permanece a referência de proveniência.

## Limites iniciais

- batch 1 e gradient accumulation;
- contexto de 512 tokens no smoke test, aumentando somente após medir memória;
- LoRA em poucas camadas no teste de compatibilidade;
- sem sweeps ou fine-tuning completo no MacBook Air;
- runs oficiais devem fixar modelo, revisão, dataset, configuração e ambiente.

O smoke test comprova compatibilidade, não qualidade do modelo. A promoção de um adapter continua sujeita ao plano de avaliação do projeto.

## Baseline inicial do projeto

Smoke test executado em 15 de agosto de 2026 num MacBook Air M5 com GPU de 10 núcleos e 32 GB de memória unificada:

| Medida | Resultado |
|---|---:|
| MLX / MLX-LM | 0.32.0 / 0.31.3 |
| Modelo quantizado em cache | 3,3 GB |
| Memória de inferência | 2,673 GB |
| Geração aquecida | 81,4 tokens/s |
| Parâmetros treináveis LoRA | 0,852 M (0,018%) |
| Pico de memória no treino | 3,176 GB |
| Treino após aquecimento | 182–200 tokens/s |
| Cinco iterações, incluindo validação | 10,0 s |
| Tamanho do adapter smoke | 6,5 MB |

Os números são um teste curto com contexto pequeno e cache já preenchido. Não representam throughput sustentado, qualidade do adapter nem desempenho com exemplos reais mais longos.

O checkpoint antigo `mlx-community/Gemma4-E2B-IT-Text-int4` não deve ser usado neste fluxo: na revisão testada, seus pesos de KV compartilhados eram incompatíveis com o carregador do MLX-LM 0.31.3. O checkpoint configurado acima carregou, treinou e recarregou o adapter com sucesso.
