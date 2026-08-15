# Mineração e curadoria

## Fontes

O dataset combinará:

1. corpora públicos de diffs para adaptação à compreensão de mudanças;
2. episódios minerados de repositórios públicos com code/doc co-change;
3. exemplos gold revisados por pessoas com experiência em engenharia, produto ou arquitetura;
4. feedback de uso real que possa ser legalmente reaproveitado.

## Critérios de seleção de repositórios

- licença clara e compatível com redistribuição e criação do dataset;
- histórico de pull requests ou commits compreensível;
- documentação versionada junto ao código;
- preferência por ADRs, requisitos ou design docs rastreáveis;
- diversidade de linguagens, arquiteturas e maturidade;
- exclusão de mirrors, forks inativos e repositórios dominados por bots.

## Pipeline de mineração

```text
descobrir repositórios
    -> registrar licença e proveniência
    -> clonar snapshot imutável
    -> extrair PRs/commits/issues
    -> classificar arquivos
    -> agrupar Change Episodes
    -> separar code/test/schema/doc/ADR diffs
    -> construir candidatos positivos e negativos
    -> remover secrets e PII
    -> executar filtros de qualidade
    -> revisão/amostragem humana
    -> publicar manifesto e splits
```

## Formação de episódios

Preferência de agrupamento:

1. pull request merged;
2. issue ou ticket compartilhado;
3. sequência de commits na mesma branch e janela temporal;
4. release ou hotfix explicitamente identificado.

Um merge commit não deve ser tratado automaticamente como um único exemplo se combinar intenções independentes.

## Weak labels

Um `doc_diff` humano observado pode iniciar um candidato `UPDATE`, mas não é automaticamente ground truth. A atualização pode estar incompleta, excessiva ou incorreta.

Da mesma forma:

```text
ausência de doc_diff != NO_CHANGE
```

PRs sem alteração documental devem receber uma das etiquetas de curadoria:

- `confirmed_no_change`;
- `possible_missing_documentation`;
- `unknown`.

Somente o primeiro grupo alimenta diretamente a classe `NO_CHANGE`.

## Níveis de qualidade

| Tier | Origem | Uso |
|---|---|---|
| Bronze | mineração automática | exploração, retrieval e pré-adaptação |
| Silver | heurísticas fortes e validação automática | SFT com peso reduzido |
| Gold | revisão humana e evidência verificada | SFT principal e avaliação |

## Revisão gold

Cada episódio gold deve responder:

1. O contexto é suficiente?
2. Qual comportamento observável mudou?
3. Quais documentos contêm afirmações afetadas?
4. O ADR está vigente e coerente com a implementação?
5. O patch é mínimo e factual?
6. Alguma decisão humana está sendo implicitamente inventada?

Casos ambíguos devem ter adjudicação por uma segunda pessoa.

## Privacidade e segurança

- Executar scanners de secrets antes de gravar o exemplo processado.
- Remover nomes, emails e identificadores pessoais não necessários.
- Não coletar repositórios sem licença identificável para redistribuição.
- Manter uma denylist de repositórios e um processo de remoção.
- Publicar hashes e proveniência suficientes para auditoria sem republicar conteúdo proibido.

## Versionamento

Cada release do dataset deve registrar:

- versão semântica;
- commit do pipeline;
- snapshot das fontes;
- regras de inclusão e exclusão;
- distribuição por classe, linguagem, tipo documental e licença;
- taxa de concordância humana;
- limitações e riscos conhecidos;
- hashes de cada split.
