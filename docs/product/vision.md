# Visão do produto

## Problema

Equipes alteram requisitos, decisões e código por múltiplos caminhos: frameworks agentivos, IDEs, CLIs, hotfixes, pull requests e automações. A documentação inicial pode ser boa, mas perde alinhamento quando o processo depende de alguém lembrar de atualizá-la.

O problema central é a ausência de continuidade e enforcement entre os artefatos do SDLC, não a ausência de ferramentas capazes de redigir Markdown.

## Visão

Criar um modelo pequeno, aberto e especializado que interprete episódios de mudança no SDLC, identifique o impacto documental e produza patches mínimos, explicáveis e sustentados por evidências.

O modelo inicial será obtido por fine-tuning do `google/gemma-4-E2B-it`. O sistema deve ser executável localmente ou em infraestrutura controlada, sem depender de um modelo de fronteira no runtime.

## Usuários

- equipes de produto e engenharia que mantêm documentação como código;
- arquitetos responsáveis por ADRs e documentação arquitetural;
- maintainers de projetos open source;
- organizações que precisam de rastreabilidade entre requisito, decisão, implementação e operação;
- equipes modernizando sistemas brownfield.

## Jobs to be done

1. Quando um requisito ou ADR mudar, identificar os documentos potencialmente afetados antes da implementação.
2. Quando código ou testes mudarem, comparar o comportamento implementado com as decisões e documentos existentes.
3. Quando houver evidência suficiente, propor um patch documental mínimo.
4. Quando houver contradição, impedir que o sistema invente uma decisão e encaminhar o conflito.
5. Antes do merge ou release, produzir uma decisão verificável sobre impacto documental.

## Resultados suportados

| Resultado | Significado |
|---|---|
| `UPDATE` | Existe impacto e evidência suficiente para gerar patch. |
| `NO_CHANGE` | O episódio não altera afirmações documentadas. |
| `NEEDS_DECISION` | Há conflito ou decisão de produto/arquitetura ainda não tomada. |
| `INSUFFICIENT_CONTEXT` | O pacote não contém evidência suficiente. |

## Não objetivos iniciais

- gerar toda a documentação de um produto do zero;
- substituir product managers, arquitetos ou technical writers;
- inferir intenção organizacional apenas pelo código;
- modificar documentos sem trilha de auditoria;
- memorizar o conteúdo corrente de cada projeto nos pesos do modelo;
- suportar todos os formatos e ferramentas de ALM na primeira versão.

## Princípios

1. **Evidência antes de edição:** todo patch deve apontar para as fontes que o justificam.
2. **Abstenção é sucesso:** pedir decisão é preferível a consolidar uma interpretação inventada.
3. **Edição mínima:** preservar texto não afetado, autoria e estrutura dos documentos.
4. **Contexto versionado:** entradas e saídas devem ser reproduzíveis.
5. **Modelo propõe, código verifica:** schemas, paths, hashes e patches são validados deterministicamente.
6. **Feedback vira dado:** decisões de revisão alimentam futuras versões do dataset.

## Critérios de sucesso do MVP

- classificar corretamente os quatro resultados em projetos não vistos;
- recuperar documentos impactados com recall suficiente para uso como gate assistido;
- produzir JSON válido e patches aplicáveis de forma consistente;
- não criar afirmações sem evidência presente no `ChangeEnvelope`;
- operar em hardware compatível com a proposta de um modelo E2B;
- demonstrar ganho mensurável sobre o checkpoint original.
