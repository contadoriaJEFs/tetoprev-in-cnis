## V1.2.51
- Corrigida a reabertura automática do modal **Evidência documental — CNIS** em cada rerun do Streamlit.
- O modal agora é aberto diretamente pelo botão **Ver CNIS**, sem persistir seu alvo em `session_state`.
- Alterações no termo inicial ou em outros campos não reabrem o modal.

## V1.2.42 — Tabela de apuração ampliada

- Tabela principal da Apuração com altura de 780 px, permitindo visualizar aproximadamente 24 competências antes da rolagem.
- Alteração exclusivamente visual; motor de cálculo preservado.

# V1.2.31

- Adicionada confirmação explícita da classificação previdenciária, permitindo confirmar a opção já selecionada sem alternar para outra alíquota.
- A confirmação grava a classificação como decisão do usuário, com origem e nível de confiança confirmada.
- Corrigida a seleção de declarantes na Apuração: as fontes incluídas no Agrupamento/Classificação passam a ser selecionadas automaticamente quando o conjunto de declarantes muda.
- Mantido o seletor de declarantes para inclusão/exclusão manual.
- A desmarcação manual não é sobrescrita a cada rerun.
- Motor previdenciário e regras de cálculo preservados.

## V1.2.30
- Atualização do título visível da aplicação para V1.2.30.
- Ajustes de hierarquia visual das etapas e blocos auxiliares.
- Correção do import `TA_RIGHT` para geração do relatório PDF.

# V1.2.30

- Reorganização visual da navegação principal.
- Guias com destaque visual e indicação clara da etapa ativa.
- Identificação dos autos recolhível.
- Declarações identificadas recolhível.
- Consulta para Excel recolhível.
- Correção do import de `TA_RIGHT` para geração do relatório PDF.

# Changelog — Extrator DIRF + Motor Previdenciário


## V1.2.29
- Ajustado o cabeçalho da Demonstração horizontal: “Competência” ocupa as duas linhas em azul escuro, com texto branco e fonte de 11 pt.
- Mantidos CNPJs em azul escuro e Remuneração/Previdência em azul claro.
- Mantidas competências e tipo do Resultado consolidado sem negrito.
- Mantida a última coluna “Acima do teto” em negrito.
- Destacado em negrito o valor do Total acima do teto.
- Aumentada para 12 pt a identificação dos autos.
- Reordenado o relatório: item 3 Demonstração horizontal e item 4 Resultado consolidado, encerrando o relatório.


## V1.2.28
- Resultado consolidado do PDF: competências e valores com tipografia regular.
- Coluna “Acima do teto” em negrito no resultado consolidado.
- Valor do “Total acima do teto” destacado em negrito.
- Identificação dos autos ampliada para 12 pt.
- Demonstração horizontal preservada em paisagem.
- Cabeçalho “Competência” com tratamento próprio e CNPJ em azul escuro.


## V1.2.27
- Ajuste do relatório PDF conforme revisão visual.
- Removida a coluna **Status** do item 3 — Resultado consolidado.
- Aumentada a tipografia do relatório, priorizando leitura em A4 paisagem.
- Reforçado o cabeçalho **COMPETÊNCIA** da Demonstração horizontal para impedir desaparecimento visual.
- Mantida a identificação dos vínculos por CNPJ na Demonstração horizontal.
- Mantida a estrutura Remuneração / Previdência por CNPJ.
- Mantidos motor previdenciário, regras de apuração, classificação, deduplicação e seleção de 13º.

## V1.2.26
- Ajustes anteriores de relatório, persistência e interface.

## V1.2.37
- Excel horizontal de conferência das DIRFs selecionadas, com valores numéricos sem R$ e formato brasileiro.
