# Data workspace

Esta árvore separa os estágios do pipeline. Os dados reais, checkpoints e artefatos pesados não são versionados no Git.

```text
data/
├── raw/         # snapshots imutáveis e metadados de origem
├── interim/     # episódios extraídos antes da curadoria final
└── processed/   # splits prontos para treino e avaliação
```

Cada execução de mineração deve produzir um manifesto contendo fonte, licença, commit de origem, versão do extrator, hashes dos arquivos e filtros aplicados. Dados sensíveis ou de clientes devem permanecer em storage privado.
