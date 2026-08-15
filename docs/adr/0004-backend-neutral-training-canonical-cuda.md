# ADR-0004: contrato backend-neutral e promoção canônica em CUDA

- Status: aceito
- Data: 2026-08-15

## Contexto

Apple Silicon permite que colaboradores executem experimentos de baixo custo com MLX. O ecossistema de treinamento e publicação usado como referência pelo projeto, porém, é baseado em Transformers, PEFT e CUDA. Tornar apenas um desses ambientes oficial excluiria colaboradores ou criaria artifacts cuja compatibilidade não foi demonstrada.

Colab reduz a barreira de acesso a CUDA, mas suas imagens, GPUs, cotas e sessões não são uma base suficiente para reprodutibilidade. Também não devemos equiparar um upload bem-sucedido ao Hugging Face com uma promoção de qualidade.

## Decisão

O DocDrift define um contrato de execução independente de backend. MLX, CUDA local e Colab podem produzir experimentos e candidatos acompanhados de manifests.

Na fase inicial, todo candidato a release será reproduzido por um estágio canônico CUDA, executado preferencialmente em Colab a partir de código revisado. Depois, uma avaliação limpa e independente decide se o artefato pode ser promovido de staging para uma release versionada no Hugging Face.

Adapters de frameworks diferentes não são considerados intercambiáveis sem conversão suportada e verificação de equivalência. Colab é o executor de referência substituível; commits, revisões imutáveis, manifests, hashes e gates são a fonte de verdade.

## Consequências

### Positivas

- contribuições locais continuam úteis e comparáveis;
- o caminho de promoção usa o ecossistema CUDA de referência;
- trocar o provedor de GPU não muda o contrato;
- uploads e releases ficam separados;
- ambiente, dados e artifacts tornam-se auditáveis.

### Custos

- candidatos locais selecionados precisam de reprodução canônica;
- duas implementações exigem testes de paridade semântica;
- o pipeline precisa persistir manifests e checkpoints fora do runtime;
- promoção exige um estágio adicional de avaliação e revisão.

## Alternativas rejeitadas

### Aceitar qualquer adapter local diretamente

Rejeitada porque formatos, quantização e módulos-alvo podem divergir e porque o ambiente local não é controlado pelo projeto.

### Tornar Colab a única forma de treinar

Rejeitada porque excluiria hardware local útil, criaria dependência de um serviço com recursos variáveis e dificultaria migração para outro runner.

### Exigir igualdade bit a bit entre backends

Rejeitada porque kernels e aceleradores distintos podem ser não determinísticos. A paridade será medida por contratos, métricas e tolerâncias explícitas.
