# Dataset Card — Change-Episode-to-Documentation

> Status: rascunho. Nenhum dataset foi publicado ainda.

## Resumo

Dataset destinado ao fine-tuning e avaliação de modelos que sincronizam documentação com mudanças do SDLC. Cada exemplo associa um `ChangeEnvelope` a um `DocumentationSyncResult` revisado.

## Tarefas

- classificação de impacto documental;
- detecção de conflitos entre artefatos;
- recuperação/ranking de documentos impactados;
- geração de patches documentais estruturados;
- abstenção por conflito ou contexto insuficiente.

## Idiomas e linguagens

A composição será publicada por release. O objetivo inicial é suportar documentação em inglês e português e código de múltiplas linguagens, sujeito à disponibilidade de dados licenciados e revisados.

## Estrutura

Os exemplos seguem os schemas versionados em [`schemas/`](../../schemas/). Splits são separados por família de repositório e incluem holdout temporal.

## Fontes

As fontes exatas, licenças e revisões serão publicadas em manifests por release. Nenhuma fonte sem licença identificável será incluída no corpus redistribuído.

## Curadoria

O pipeline e os níveis Bronze, Silver e Gold estão descritos em [Mineração e curadoria](curation.md).

## Dados pessoais e sensíveis

O pipeline deve remover secrets e PII desnecessária. A publicação incluirá resultados dos scanners, limitações conhecidas e processo de remoção de exemplos.

## Limitações esperadas

- viés em direção a projetos open source com boa disciplina documental;
- sub-representação de documentação corporativa e requisitos formais;
- weak labels extraídos de histórico podem reproduzir documentação incompleta;
- co-change não implica relação semântica;
- ausência de doc diff não comprova ausência de impacto;
- padrões de documentação variam por organização e domínio.

## Licença

Ainda não definida. A licença do dataset poderá diferir da licença do código e deverá respeitar as licenças e termos das fontes.

## Manutenção e remoção

Antes da release pública serão documentados maintainer, canal de contato, política de correções, processo de opt-out e frequência de novas versões.
