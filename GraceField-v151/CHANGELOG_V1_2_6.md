# CHANGELOG V1.2.6

## Classificação previdenciária — refinamento da interface

- Reorganizada a aba **Classificação** em cartões visuais por fonte/vínculo.
- Removida a coluna redundante **Incluído** da tabela-resumo inferior.
- Explicitado que **Alíquota efetiva observada** é apenas diagnóstico da DIRF e não define a classificação.
- Renomeado conceitualmente o campo de decisão para **Grupo previdenciário**.
- Opções do grupo passaram a ter descrição amigável:
  - Não definido — requer confirmação;
  - 11% — contribuição fixa;
  - 20% — contribuição fixa;
  - Progressiva — aplicar tabela histórica.
- Mantida a persistência da classificação durante a sessão.
- Mantida a alimentação da aba **Verificação** pela classificação selecionada.
- Mantido `nao_definido` como trava de segurança contra classificação silenciosa.
- Mantida a preservação integral do RAW.
- Mantido o detalhamento por competência da aba **Verificação** sem alterações.
