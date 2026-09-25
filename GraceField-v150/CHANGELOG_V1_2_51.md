# V1.2.51 — Correção de reabertura do modal CNIS

## Modal de evidência documental

- Corrigido o comportamento do botão **Ver CNIS**.
- O modal de evidência CNIS passa a ser aberto diretamente pelo clique no botão.
- Removida a persistência do alvo do modal em `st.session_state`.
- O modal não reaparece automaticamente a cada rerun da aplicação.
- Alterações em campos como termo inicial, competência ou demais controles não reabrem o modal CNIS.
- O modal somente é exibido quando o usuário clicar novamente em **Ver CNIS**.

## Regra preservada

- Nenhuma alteração no motor previdenciário.
- Nenhuma alteração na classificação CNIS implementada na V1.2.50.
- Nenhuma alteração na extração ou nas evidências documentais.
