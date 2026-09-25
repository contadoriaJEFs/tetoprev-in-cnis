# V1.2.13 — Verificação simplificada

## Alteração

A guia **Verificação** deixa de apresentar a contribuição previdenciária calculada e a diferença entre DIRF e cálculo como resultados da análise.

### Mantido
- Previdência Oficial extraída da DIRF;
- Remuneração;
- Metodologia;
- Tabela histórica;
- status de análise;
- análise específica do 13º;
- período e fonte selecionados;
- detalhamento por competência;
- cópia para Excel.

### Removido da apresentação da Verificação
- coluna **Calculada**;
- coluna **Diferença**;
- métricas de calculada/diferença;
- exibição da comparação numérica DIRF × calculada.

### Regra de arquitetura

A Verificação é uma camada de conferência/análise. O cálculo previdenciário consolidado definitivo ocorre exclusivamente na **Apuração**, onde os valores são somados por tipo (Progressiva, 11% e 20%), o teto é aplicado e somente então é determinado o eventual valor acima do teto.

A Previdência Oficial da DIRF continua sendo preservada como dado original e continua participando da Apuração, inclusive quando a remuneração da fonte for R$ 0,00.
