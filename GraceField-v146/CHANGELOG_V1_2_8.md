# V1.2.8 — Classificação automática + edição pelo usuário

- Criado `classificador_previdenciario.py` com regras determinísticas e auditáveis.
- Cada fonte selecionada recebe `classificacao_sugerida`, `nivel_confianca`, `evidencias`, `regra_classificacao` e `versao_regra`.
- Padrões estáveis próximos de 11% ou 20% podem ser sugeridos automaticamente com alta confiança.
- Variação de taxas compatível com faixas progressivas pode gerar sugestão progressiva.
- Evidência insuficiente permanece `nao_definido` ou com confiança baixa/média, exigindo confirmação.
- A classificação final continua editável individualmente.
- Alterações feitas pelo usuário são registradas como `origem_classificacao = usuario`.
- Metadados de classificação são preservados na exportação JSON.
- Motor de extração não foi alterado.
