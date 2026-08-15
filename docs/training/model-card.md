# Model Card — DocDrift-Gemma-4-E2B

> Status: rascunho pré-treinamento. Os campos de resultados serão preenchidos após uma execução reproduzível.

## Modelo

- Modelo base planejado: `google/gemma-4-E2B-it`
- Método inicial: QLoRA
- Versão do adapter: não disponível
- Licença do modelo base: [Apache 2.0](https://huggingface.co/google/gemma-4-E2B-it)
- Licença do adapter: a definir em conjunto com a licença do repositório

## Uso pretendido

Analisar um `ChangeEnvelope`, classificar impacto documental, apontar conflitos e, quando sustentado por evidências, produzir patches estruturados sobre documentos candidatos.

## Fora do escopo

- aplicar patches sem validação e autorização externas;
- escolher unilateralmente entre requisitos, ADRs e código conflitantes;
- gerar aconselhamento jurídico, regulatório ou de segurança sem revisão especializada;
- processar secrets ou informações pessoais como dados de treino;
- funcionar como fonte única de verdade do projeto.

## Dados de treino

Ainda não disponíveis. A versão final referenciará a release exata do dataset e sua dataset card.

## Avaliação

O modelo será comparado com o checkpoint original em splits por repositório, holdout temporal e challenge set. Métricas e gates estão em [Plano de avaliação](../evaluation/plan.md).

## Resultados

| Métrica | Baseline | Fine-tuned |
|---|---:|---:|
| Impact macro F1 | TBD | TBD |
| UPDATE recall | TBD | TBD |
| NEEDS_DECISION recall | TBD | TBD |
| Evidence precision | TBD | TBD |
| Patch apply rate | TBD | TBD |
| Unsupported claim rate | TBD | TBD |

## Limitações esperadas

- capacidade limitada para mudanças muito distribuídas ou ambíguas;
- sensibilidade à qualidade do retrieval;
- risco de seguir instruções maliciosas presentes no contexto;
- confiança numérica não calibrada por padrão;
- desempenho variável entre linguagens e estilos documentais;
- contexto longo não elimina omissões do collector.

## Recomendações de implantação

- validar todas as saídas contra schema;
- verificar evidências, hashes, paths e aplicabilidade do patch;
- iniciar em modo `observe` ou `comment`;
- manter revisão humana para conflitos e mudanças críticas;
- registrar versão do modelo, input e decisão final;
- monitorar drift por projeto e tipo documental.
