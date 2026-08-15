# Roadmap

## Fase 0 — fundação

- [x] visão e limites do produto;
- [x] arquitetura inicial;
- [x] schemas de entrada e saída;
- [x] exemplo validável;
- [x] estratégia inicial de dataset, treino e avaliação;
- [x] escolher marca e nome público;
- [ ] definir licença do código e do futuro dataset.

## Fase 1 — baseline e benchmark

- [ ] implementar serialização no chat template do Gemma 4;
- [ ] executar baseline zero-shot e few-shot;
- [ ] criar challenge set gold inicial;
- [ ] implementar métricas de classificação, retrieval e patch;
- [ ] medir memória, latência e comprimento de contexto;
- [ ] publicar relatório de baseline.

## Fase 2 — mineração

- [ ] definir política de licenças permitidas;
- [ ] implementar descoberta e snapshot de repositórios;
- [ ] extrair commits, PRs, issues, ADRs e documentos;
- [ ] agrupar Change Episodes;
- [ ] detectar e remover secrets/PII;
- [ ] produzir dataset bronze e relatório de qualidade;
- [ ] construir ferramenta de revisão gold.

## Fase 3 — fine-tuning

- [x] definir contrato backend-neutral e estágio canônico CUDA;
- [ ] publicar notebook Colab versionado como orquestrador fino;
- [x] gerar manifest experimental e hashes no smoke test MLX;
- [ ] estabilizar o schema do manifest e implementá-lo na execução CUDA canônica;
- [ ] realizar experimento pequeno de QLoRA;
- [ ] comparar task-specific versus multitask;
- [ ] ajustar mistura de classes;
- [ ] executar ablações de contexto;
- [ ] avaliar preference tuning;
- [ ] publicar adapter, configuração e model card.

## Fase 4 — integração SDLC

- [ ] implementar adapter GitHub;
- [ ] implementar context retriever;
- [ ] aplicar e validar patches em branch isolada;
- [ ] operar em modo `observe`;
- [ ] capturar feedback de revisores;
- [ ] promover gradualmente para `soft-gate`.

## Fase 5 — release pública

- [x] documentação inicial de contribuição e governança;
- [x] política inicial de segurança e remoção de dados;
- [x] dataset card em rascunho;
- [x] model card em rascunho;
- [ ] escolher e publicar a licença do repositório;
- [ ] demo reprodutível;
- [ ] benchmark público com splits sem vazamento.
