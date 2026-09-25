# CHANGELOG — V1.2.37

## Excel de conferência das DIRFs

- Adicionada exportação **Excel — Conferência das DIRFs** na aba Exportação.
- O arquivo reproduz a demonstração horizontal: cada CNPJ selecionado ocupa duas colunas, **Remuneração** e **Previdência**.
- Valores vêm exclusivamente dos campos documentais extraídos da DIRF (`rendimento_tributavel` e `previdencia_oficial`).
- Valores são gravados como números no Excel, com visual brasileiro `#.##0,00`, **sem `R$`**, permitindo cópia/cola e cálculos posteriores.
- Somente os CNPJs selecionados para a análise são incluídos.
- O Excel não mistura valores calculados pelo motor previdenciário.
- Mantida a lógica de cálculo da V1.2.36 sem alteração.

## Validação

- Testes de fumaça existentes da V1.2.x preservados e executados.
