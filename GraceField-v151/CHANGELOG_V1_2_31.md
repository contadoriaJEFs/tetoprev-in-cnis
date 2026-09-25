# CHANGELOG — V1.2.31

## Correções

### 1. Confirmação explícita da classificação previdenciária
- Adicionado botão **CONFIRMAR CLASSIFICAÇÃO** em cada fonte.
- A classificação já exibida no seletor pode ser confirmada diretamente, sem precisar trocar para outra alíquota e retornar.
- A confirmação grava `classificacao_final`, `origem_classificacao=usuario`, `nivel_confianca=confirmada`, data/hora e usuário confirmador.
- O seletor continua permitindo alterar a classificação antes ou depois da confirmação.

### 2. Sincronização dos declarantes com a Apuração
- As fontes efetivamente incluídas no agrupamento passam automaticamente para a seleção de declarantes da Apuração.
- O multiselect permanece disponível para exclusões/inclusões manuais.
- Após uma alteração manual, a escolha do usuário é preservada.
- O motor previdenciário não foi alterado.

## Preservação
- A V1.2.31 foi construída sobre a estrutura completa da base V1.2.30/base V1.2.23.
- Nenhum arquivo funcional da base foi removido.
