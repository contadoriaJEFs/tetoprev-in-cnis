# Changelog — V1.2.20

## Deduplicação documental conservadora

Correção para PDFs em que o advogado/documento juntado contém a mesma declaração DIRF repetida em páginas diferentes do mesmo arquivo.

### O que foi implementado

- O RAW continua preservando **todas as ocorrências extraídas**.
- Cada bloco recebe uma assinatura documental baseada no conteúdo integral da declaração.
- A página não participa da assinatura; portanto, a mesma declaração repetida em outra página é reconhecida como a mesma declaração.
- A primeira ocorrência, pela menor página, é marcada como `CANONICO`.
- As ocorrências posteriores idênticas são marcadas como `DUPLICATA_DOCUMENTAL`.
- A duplicata continua visível na auditoria e no JSON.
- Somente registros canônicos entram em:
  - agrupamento;
  - classificação;
  - verificação;
  - apuração;
  - demonstração horizontal.
- A identidade do vínculo continua sendo o CNPJ, independentemente de página/bloco.
- Uma declaração que tenha qualquer diferença material em seus dados não é eliminada pela deduplicação.

### Teste com o PDF do caso

No arquivo `0031059-48.2026.4.05.8300_DIRF.pdf` foram identificados 16 blocos, sendo 8 declarações únicas e 8 cópias integrais. Assim, os valores de setembro/outubro do FUNDO MUNICIPAL DE SAUDE — CNPJ 10.392.418/0001-45 — deixam de ser somados duas vezes.
