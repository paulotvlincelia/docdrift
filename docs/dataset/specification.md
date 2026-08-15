# Especificação do dataset

## Nome de trabalho

`Change-Episode-to-Documentation`.

O nome definitivo do dataset poderá acompanhar a marca pública do projeto, por exemplo `DocDrift-ChangeEpisodes`.

## Unidade de observação

A unidade é um **Change Episode**: conjunto ordenado de eventos relacionados a uma única intenção de mudança, desde sua formulação até o estado de implementação considerado para sincronização documental.

Um episódio pode conter um ou vários commits e não precisa possuir todos os tipos de artefato.

## Contratos

- Entrada: [`change-envelope.schema.json`](../../schemas/change-envelope.schema.json)
- Saída: [`documentation-sync-result.schema.json`](../../schemas/documentation-sync-result.schema.json)

## Campos essenciais de entrada

| Grupo | Conteúdo |
|---|---|
| Identidade | ID estável, repositório, revisão base e revisão alvo |
| Evento | tipo, origem, timestamp e referências externas |
| Intenção | issue/PR, requisito anterior e requisito posterior |
| Decisão | ADRs anteriores, posteriores e seus status |
| Implementação | diffs de código, testes, schemas e configurações |
| Documentação | documentos candidatos no estado anterior |
| Política | tipos de documento, owners, ações e paths permitidos |
| Recuperação | método, score, ranking e informação sobre truncamento |

## Campos essenciais do target

- decisão global;
- tipos de mudança;
- documentos impactados e justificativa;
- evidências usadas;
- conflitos detectados;
- patches estruturados;
- lacunas de contexto;
- confiança por componente, usada apenas para análise e não como garantia factual.

## Taxonomia inicial de mudanças

```text
behavioral
architectural
api_contract
data_model
operational
security
configuration
dependency
performance
deprecation
refactor_only
documentation_only
```

## Tipos documentais iniciais

```text
readme
architecture
adr
requirement
api_reference
runbook
deployment
security
testing
changelog
user_guide
```

## Formato de patch

Cada patch é uma sequência ordenada de operações:

- `replace`: substitui uma ocorrência exata;
- `insert_after`: insere após uma âncora exata;
- `insert_before`: insere antes de uma âncora exata;
- `delete`: remove uma ocorrência exata.

Cada operação inclui `old_text` ou `anchor`, `new_text` quando aplicável e o hash SHA-256 do documento anterior. Operações ambíguas ou não aplicáveis são rejeitadas pelo runtime.

## Classes de exemplos

O corpus deve conter quatro classes balanceadas por risco, não necessariamente por quantidade:

### UPDATE

Há uma afirmação documental afetada e evidência suficiente para atualizá-la.

### NO_CHANGE

A mudança é interna ou não altera nenhuma afirmação documental. Essa classe deve conter refatorações, formatação, testes sem mudança de contrato e alterações sem impacto externo confirmado.

### NEEDS_DECISION

Existe contradição entre intenção, decisão, implementação ou documentação. O target descreve o conflito, mas não escolhe unilateralmente qual fonte deve prevalecer.

### INSUFFICIENT_CONTEXT

Faltam documentos, requisitos, diff completo ou outra evidência essencial.

## Regras contra vazamento

- Nunca incluir `documentation_after` no input.
- Não usar mensagens que reproduzam literalmente o target sem marcá-las como fonte legítima.
- Separar treino, validação e teste por repositório.
- Manter um teste temporal posterior às revisões usadas no treino.
- Deduplicar forks, cherry-picks e commits equivalentes.
- Evitar que versões quase idênticas do mesmo episódio atravessem splits.

## Exemplo mínimo

Os arquivos [`examples/change-envelope.json`](../../examples/change-envelope.json) e [`examples/documentation-sync-result.json`](../../examples/documentation-sync-result.json) formam um par válido para testes de contrato, não um exemplo suficiente para treino.
