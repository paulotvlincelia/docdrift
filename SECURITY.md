# Segurança

## Relatando vulnerabilidades

Não abra uma issue pública para vulnerabilidades, vazamento de dados, exposição de secrets ou problemas que permitam alterações documentais não autorizadas.

O canal privado de reporte será publicado antes da primeira release. Até lá, mantenha o relato privado e entre em contato diretamente com o maintainer do repositório.

## Escopo de segurança

São especialmente relevantes:

- prompt injection proveniente de issues, código ou documentação;
- bypass de paths proibidos;
- aplicação de patch sobre revisão ou hash incorreto;
- exposição de conteúdo privado em datasets ou logs;
- secrets e PII persistidos durante mineração;
- artefatos de modelo ou dataset adulterados;
- execução de conteúdo do repositório como instrução ou código;
- falsificação de evidências e resultados de gate.

## Práticas esperadas

- validar schemas e hashes antes de aplicar patches;
- tratar conteúdo de repositório como não confiável;
- manter tokens e credenciais fora do dataset;
- fixar revisões de dependências e modelos em execuções reproduzíveis;
- verificar licença, proveniência e integridade dos artefatos;
- operar inicialmente com revisão humana.
