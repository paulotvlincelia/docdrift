# Treinamento local em Apple Silicon

Este é um backend suportado para desenvolvimento, profiling, avaliação e fine-tuning experimental. Resultados locais podem propor candidatos, mas a promoção segue o [modelo operacional](operating-model.md): reprodução canônica em CUDA, avaliação limpa e staging antes do Hugging Face.

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
4. recarrega o adapter e executa uma nova inferência;
5. grava adapter, logs e manifest em `artifacts/mlx-smoke/<run-id>/`.

Os exemplos em `examples/training-smoke/` são sintéticos e servem somente para verificar o pipeline. Eles não devem ser incluídos em resultados de qualidade ou publicados como dataset DocDrift.

## Autenticação no Hugging Face

Checkpoints públicos podem ser baixados sem autenticação, com limites menores. Para publicar ou acessar um repositório privado:

```bash
.venv/bin/hf auth login
.venv/bin/hf auth whoami
```

Informe o token somente no prompt seguro da CLI. Nunca grave tokens em arquivos versionados, comandos de shell, exemplos ou relatórios.

## Limites iniciais

- batch 1 e gradient accumulation;
- contexto de 512 tokens no smoke test, aumentando somente após medir memória;
- LoRA em poucas camadas no teste de compatibilidade;
- sem sweeps ou fine-tuning completo no MacBook Air;
- runs oficiais devem fixar modelo, revisão, dataset, configuração e ambiente.

O smoke test comprova compatibilidade, não qualidade do modelo. A promoção de um adapter continua sujeita ao plano de avaliação do projeto.

O manifest resolve e registra a revisão imutável do modelo, commit e estado do Git, hashes de configuração, dataset, lockfile e adapter, versões do runtime e memória disponível. Caminhos locais são removidos do comando e do `adapter_config.json`. O estado permanece `experimental`, mesmo quando o smoke test passa.

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
