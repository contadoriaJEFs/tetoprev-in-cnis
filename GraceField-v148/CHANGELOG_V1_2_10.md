# V1.2.10 — Escopo explícito da Apuração

## Alterações

- A guia **🧮 Apuração** agora permite definir explicitamente o período da apuração.
- Opções de período: todo o histórico, intervalo personalizado ou um ano.
- A guia apresenta explicitamente os **declarantes utilizados**.
- O usuário pode selecionar/desselecionar declarantes por nome + CNPJ.
- A consolidação é realizada somente com os declarantes e competências dentro do escopo selecionado.
- O detalhamento de cada competência identifica os declarantes efetivamente consolidados.
- A extração RAW permanece intacta e não é alterada pela seleção do escopo da apuração.
- Mantida a separação do 13º em relação às competências mensais.
- Mantida a lógica de consolidação para N vínculos.

## Validação

- Smoke tests: OK.
- Testes de apuração conjunta: OK.
- Testes de classificação na verificação: OK.
