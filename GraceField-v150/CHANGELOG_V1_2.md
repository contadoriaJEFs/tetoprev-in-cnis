# CHANGELOG — V1.2.1

## Agrupamento inteligente de fontes

### Interface
- A fonte pagadora é identificada visualmente pelo nome; CNPJ fica como informação secundária.
- Código DIRF e descrição são exibidos junto à fonte.
- Inclusão/remoção continua sendo manual e persistida durante a sessão.

### Seleção inicial
- 5706, 5557, 6800, 6813 e 8053, quando exclusivos da fonte, são tratados como não previdenciários para a seleção inicial.
- Fonte sem remuneração mensal e sem Previdência Oficial também não é sugerida.
- Fontes com remuneração e/ou Previdência Oficial permanecem sugeridas para análise.

### Preservação de dados
- Nenhum registro é eliminado do RAW.
- A desmarcação afeta apenas as camadas de agrupamento, classificação/apuração e demonstração.
- Foi incluído botão para incluir todas as fontes, permitindo recuperar fontes inicialmente excluídas.

### Verificação
- Seleção de fonte na guia de verificação usa nome + CNPJ, evitando a lista de CNPJs isolados.

## Compatibilidade
- A base histórica 2017–2026 permanece.
- A lógica 11%/20% permanece.
- PROGRESSIVA continua separada do motor principal até a validação dos múltiplos vínculos.


## V1.2.2 — correções de fluxo e interface
- A guia 🧩 Classificação passa a exibir exclusivamente as fontes selecionadas em 🔗 Agrupamento de vínculos.
- Fontes não selecionadas continuam preservadas no RAW/auditoria, mas não recebem classificação nem entram na camada de cálculo.
- O resumo do agrupamento consolida cada CNPJ uma única vez, mesmo quando há nomes declarantes repetidos para o mesmo CNPJ.
- Corrigida a chave da guia 🔎 Verificação para a opção Manual / total da competência, evitando TypeError quando não existe CNPJ selecionado.
- Versão da aplicação atualizada para V1.2.2.
