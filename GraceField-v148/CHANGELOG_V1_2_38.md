# CHANGELOG — V1.2.38

## Exportações

- Reorganizada a aba **Exportação** em três blocos:
  - **Relatórios**;
  - **Dados para levar à planilha**;
  - **Arquivos técnicos**.
- Mantida a exportação **Excel — Conferência das DIRFs** no formato horizontal, por CNPJ, com Remuneração e Previdência extraídas.
- Adicionada exportação **Excel — Competência + Acima do teto**.
- O novo Excel contém somente:
  - Competência;
  - Diferença final (Acima do teto).
- A diferença final é o valor efetivamente apurado como contribuição recolhida acima do limite, limitado a zero quando não houver excesso.
- Os valores são gravados como números do Excel, com formato brasileiro `#.##0,00`, sem `R$`, para facilitar cópia/cola em outras planilhas.
- Congelamento da primeira linha e filtro automático no novo arquivo.

## Cálculo

- Nenhuma regra do motor previdenciário foi alterada.
- Testes da V1.2.x preservados e executados.
