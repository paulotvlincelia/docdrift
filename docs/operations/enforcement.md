# Enforcement no SDLC

## Objetivo

Garantir que a verificação documental aconteça independentemente da ferramenta usada para alterar o software. O enforcement é responsabilidade dos hooks e gates; o modelo fornece a análise semântica.

O modelo nunca aprova um merge. Ele produz uma decisão estruturada que o runtime valida e que a política da organização interpreta. Confidence serve para telemetria e triagem, nunca para ignorar evidência, validações, revisão humana ou proteção de branch.

## Pontos de integração

### Pull request

Executar quando o PR for aberto ou receber novos commits. Publicar um check com:

- decisão de impacto;
- documentos candidatos;
- conflitos;
- patch proposto;
- evidências e versão do modelo.

### Pre-merge

Branch protection exige um resultado válido. Políticas iniciais:

| Resultado | Ação |
|---|---|
| `UPDATE` | patch documental incluído ou exceção aprovada |
| `NO_CHANGE` | check aprovado e justificativa registrada |
| `NEEDS_DECISION` | merge bloqueado até decisão registrada |
| `INSUFFICIENT_CONTEXT` | reexecutar recuperação ou revisão humana |

Antes de avaliar a política acima, o runtime rejeita resultados fora do schema, evidências inexistentes, hashes ou anchors obsoletos, paths proibidos e patches não aplicáveis. Uma falha de validação não pode ser convertida em aprovação por threshold de confidence.

### Post-merge

Reconciliar o resultado previsto com o commit efetivamente merged. Isso captura alterações feitas após a última execução do PR.

### Release

Executar auditoria agregada dos episódios desde a release anterior e produzir relatório de pendências documentais.

## Modo de adoção

1. `observe`: apenas registra resultados;
2. `comment`: comenta PRs, sem bloquear;
3. `soft-gate`: exige acknowledgement humano;
4. `hard-gate`: bloqueia classes críticas configuradas.

O projeto deve medir falsos positivos antes de habilitar `hard-gate`.

## Exceções

Exceções precisam conter:

- autor e timestamp;
- justificativa;
- escopo;
- prazo ou condição de expiração;
- referência para issue de acompanhamento, quando aplicável.

Um texto livre como `no docs needed` não é evidência suficiente em modo estrito.

## Auditabilidade

Cada execução registra:

- hash do `ChangeEnvelope`;
- versão do schema;
- modelo, adapter e configuração de inferência;
- resultado bruto e resultado validado;
- validações executadas;
- decisão humana posterior;
- patch final merged.

## Ameaças específicas

- prompt injection em issues, comentários, documentação ou código;
- conteúdo malicioso tentando alterar a política do projeto;
- contexto truncado sem sinalização;
- execução sobre base ou target incorretos;
- patch aplicado em documento diferente do analisado;
- uso de versão desatualizada do ADR;
- loops em que o patch documental dispara nova atualização indefinidamente.

Políticas e instruções do runtime não devem ser montadas como conteúdo indistinto vindo do repositório. Dados não confiáveis devem ser delimitados e tratados como evidência, nunca como instrução.
