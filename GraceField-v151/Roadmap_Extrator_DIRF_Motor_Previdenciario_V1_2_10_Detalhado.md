# ROADMAP FUNCIONAL E TÉCNICO

## Extrator DIRF + Motor Previdenciário

**Documento-base para discussão com a equipe e validação por
especialista antes de qualquer nova alteração no código.**

**Versão:** consolidação atualizada até a V1.2.10\
**Status:** documento-base atualizado --- descreve o estado do projeto
até a V1.2.10 e orienta as próximas etapas.

------------------------------------------------------------------------

# 1. Objetivo geral do sistema

O sistema está sendo desenvolvido para transformar informações
existentes em arquivos **DIRF** em uma apuração previdenciária capaz de
responder:

> **Durante determinado período, quanto o segurado efetivamente recolheu
> de contribuição previdenciária e quanto desse valor ultrapassou o
> limite máximo de contribuição previdenciária aplicável em cada
> competência?**

O fluxo completo pretendido é:

``` text
ARQUIVO DIRF
      ↓
LEITURA DO PDF
      ↓
EXTRAÇÃO DOS DADOS
      ↓
BASE RAW / DADOS ORIGINAIS
      ↓
IDENTIFICAÇÃO DAS FONTES
      ↓
AGRUPAMENTO DOS VÍNCULOS
      ↓
CLASSIFICAÇÃO PREVIDENCIÁRIA
      ↓
VALIDAÇÃO DAS CLASSIFICAÇÕES EXCEPCIONAIS
      ↓
IDENTIFICAÇÃO DA REGRA PREVIDENCIÁRIA
      ↓
APLICAÇÃO DA TABELA HISTÓRICA
      ↓
APURAÇÃO POR COMPETÊNCIA
      ↓
TRATAMENTO DE MÚLTIPLOS VÍNCULOS
      ↓
COMPARAÇÃO:
CONTRIBUIÇÃO EFETIVA × CONTRIBUIÇÃO MÁXIMA
      ↓
IDENTIFICAÇÃO DO EXCESSO
      ↓
CONSOLIDAÇÃO DO PERÍODO SOLICITADO
      ↓
DEMONSTRAÇÃO
      ↓
RELATÓRIO / EXPORTAÇÃO / AUDITORIA
```

# 2. Princípio fundamental

O sistema **não deverá modificar os dados originais extraídos da DIRF**.

Devem permanecer separados:

### 2.1. Dado original

Aquilo que foi efetivamente encontrado no documento:

-   CNPJ;
-   nome do declarante;
-   código DIRF;
-   competência;
-   rendimento;
-   IRRF;
-   Previdência Oficial;
-   13º;
-   página;
-   processo;
-   demais campos extraídos.

### 2.2. Dado tratado

Resultado da organização:

-   fonte previdenciária;
-   grupo de vínculo;
-   categoria;
-   11%;
-   20%;
-   progressiva;
-   seleção/exclusão.

### 2.3. Dado calculado

Resultado produzido pelo motor:

-   remuneração considerada;
-   contribuição informada;
-   contribuição máxima;
-   diferença;
-   excesso.

A cadeia deverá ser:

``` text
PDF
 ↓
RAW
 ↓
tratamento
 ↓
cálculo
```

e não:

``` text
PDF
 ↓
tratamento destrutivo
 ↓
perda da informação original
```

# 3. FASE 1 --- Upload e processamento do PDF

## 3.1. Entrada

O usuário seleciona um arquivo DIRF em formato:

``` text
PDF
```

Exemplo utilizado nos testes:

`Suzana Marine - DIRFs.pdf`

## 3.2. Processamento

O sistema lê o PDF e percorre suas páginas, procurando estruturar as
informações da DIRF em registros.

## 3.3. Teste realizado

O arquivo de teste possui:

-   **135 páginas**
-   **1.414 registros extraídos**
-   **101 blocos de declaração**

Esses números representam o arquivo testado e **não constituem limite
técnico definitivo**.

## 3.4. Pontos a definir com a equipe

Ainda devem ser formalmente definidos:

-   tamanho máximo do PDF;
-   quantidade máxima recomendada de páginas;
-   quantidade máxima de declarações;
-   limite de memória;
-   comportamento com PDFs muito grandes;
-   PDFs protegidos;
-   PDFs digitalizados/imagem;
-   páginas corrompidas;
-   processamento em lote.

Portanto:

> **135 páginas é a quantidade efetivamente testada, não o limite
> declarado do sistema.**

# 4. FASE 2 --- Extração dos dados da DIRF

O motor atual extrai informações estruturadas.

## 4.1. Identificação do beneficiário

Informações relacionadas ao beneficiário.

## 4.2. Identificação do declarante

-   Nome;
-   CNPJ.

## 4.3. Código DIRF

Exemplos encontrados:

``` text
0561
0588
3533
5928
5706
5557
6800
6813
8053
```

## 4.4. Descrição do código

O código é preservado juntamente com sua descrição/natureza.

## 4.5. Valores mensais

As competências são estruturadas, por exemplo:

``` text
01/2020
02/2020
03/2020
...
12/2020
```

## 4.6. Totais

Também são preservados campos como:

-   Tot;
-   13º.

## 4.7. Previdência Oficial

Campo central para o projeto:

``` text
previdencia_oficial
```

## 4.8. Outros campos

A estrutura atual contempla:

``` text
rendimento_tributavel
irrf
previdencia_oficial
dependentes
pensao_alimenticia
desconto_simplificado
previdencia_complementar
compensacao_judicial_ano_calendario
compensacao_judicial_anos_anteriores
```

Também podem ser preservados:

-   página;
-   arquivo de origem;
-   fundo/clube;
-   número do processo.

# 5. FASE 3 --- Base RAW

Após a extração, os dados são preservados em uma estrutura RAW.

O RAW representa:

> **a fotografia estruturada daquilo que foi encontrado no documento.**

A finalidade é permitir:

-   auditoria;
-   reprocessamento;
-   conferência;
-   correção de classificações sem nova extração;
-   comparação entre versões.

# 6. FASE 4 --- Tela "Extração e filtros"

A tela atual permite explorar os dados.

## 6.1. Filtros

-   Ano;
-   Declarante;
-   CNPJ;
-   Código DIRF;
-   Tipo;
-   Grupo previdenciário;
-   Competência.

## 6.2. Visualização

A tabela apresenta, entre outros:

  Campo         Conteúdo
  ------------- ---------------
  Declarante    Nome da fonte
  CNPJ          CNPJ
  Competência   MM/AAAA
  Rendimentos   Valor
  Imposto       Valor
  Previdência   Valor

## 6.3. Formatação

Competências:

``` text
01/2020
```

Valores:

``` text
R$ 1.234,56
```

Percentuais:

``` text
7,50%
```

CNPJ, quando exibido:

``` text
00.000.000/0000-00
```

# 7. FASE 5 --- Cópia para Excel

Existe atualmente:

> **📋 COPIAR PARA EXCEL**

Sua finalidade principal é a conferência humana.

O Excel não deverá ser requisito para o cálculo definitivo.

Objetivo futuro:

``` text
Sistema → calcula internamente
Excel → confere/exporta
```

# 8. FASE 6 --- Identificação das fontes

A DIRF pode possuir diversas fontes pagadoras.

Cada fonte deverá ser identificada por informações como:

-   nome;
-   CNPJ;
-   código DIRF;
-   descrição;
-   competências;
-   remunerações;
-   Previdência Oficial.

# 9. FASE 7 --- Agrupamento de vínculos

A tela:

> **🔗 Agrupamento de vínculos**

organiza as fontes.

A identificação visual prioriza:

``` text
Nome da fonte
CNPJ
```

Exemplo:

``` text
BAYER S.A.
CNPJ: 18.459.628/0001-15
```

# 10. Seleção inteligente das fontes

O sistema tenta distinguir fontes potencialmente previdenciárias de
fontes claramente não previdenciárias.

Códigos como:

``` text
5706
5557
6800
6813
8053
```

podem representar aplicações financeiras, fundos, mercado etc.

Quando a natureza é claramente incompatível com o objetivo
previdenciário, essas fontes são desmarcadas por padrão.

**Importante:** desmarcar não significa apagar.

# 11. Fontes sem movimentação previdenciária

Fontes sem:

-   remuneração mensal relevante;
-   Previdência Oficial;

podem ser sugeridas como não pertencentes ao fluxo previdenciário
principal.

# 12. Ações do agrupamento

Atualmente existem ações como:

``` text
✓ Selecionar sugeridas
☑ Incluir todas
☐ Limpar seleção
```

Também existe:

> **Outras fontes**

para inclusão manual quando necessário.

# 13. Regra: nada é apagado

Fonte não selecionada:

``` text
NÃO desaparece do RAW.
```

Ela apenas não participa do fluxo previdenciário principal.

# 14. FASE 8 --- Classificação previdenciária

O projeto trabalha com três grandes categorias:

### Categoria 1 --- 11%

``` text
11%
```

### Categoria 2 --- 20%

``` text
20%
```

### Categoria 3 --- Progressiva

``` text
PROGRESSIVA
```

Existe ainda:

``` text
NÃO DEFINIDO
```

para situações ainda não resolvidas.

# 15. Situação atual da classificação

Atualmente a classificação ainda é essencialmente manual na interface.

O usuário pode selecionar a categoria da fonte.

Isso **não representa o modelo final desejado**.

# 16. FASE 9 --- Classificação automática

A próxima etapa deverá fazer o sistema analisar, quando possível:

-   código DIRF;
-   natureza da fonte;
-   existência de Previdência Oficial;
-   padrão de remuneração;
-   histórico;
-   regras cadastradas;
-   classificações previamente confirmadas.

O sistema poderá sugerir:

``` text
11%
20%
PROGRESSIVA
EXCLUÍDA
```

# 17. Princípio da classificação automática

O sistema não deverá inventar uma classificação quando houver dúvida.

Deverá distinguir:

``` text
CLASSIFICAÇÃO AUTOMÁTICA
```

de:

``` text
CLASSIFICAÇÃO CONFIRMADA PELO USUÁRIO
```

Exemplo:

``` text
classificacao = "progressiva"
origem_classificacao = "automatico"
```

ou:

``` text
classificacao = "progressiva"
origem_classificacao = "usuario"
```

# 18. O usuário não deverá classificar CNPJ por CNPJ

Objetivo:

``` text
100 fontes
 ↓
classificação automática
 ↓
casos excepcionais
 ↓
confirmação humana
```

A intenção é minimizar o trabalho manual.

# 19. FASE 10 --- Tabelas previdenciárias históricas

O motor deve determinar a tabela vigente em cada competência.

Não deve existir apenas:

``` text
teto atual
```

para todos os períodos.

A lógica é:

``` text
competência
 ↓
tabela vigente
 ↓
faixas
 ↓
alíquotas
 ↓
teto
```

# 20. Histórico cadastrado

A estrutura atual contempla:

``` text
2017
2018
2019
2020
2021
2022
2023
2024
2025
2026
```

# 21. Exemplo de tabela progressiva

Uma competência pode possuir:

``` text
Faixa 1 → 7,5%
Faixa 2 → 9%
Faixa 3 → 12%
Faixa 4 → 14%
```

O cálculo deverá respeitar as faixas correspondentes.

Não deverá simplesmente fazer:

``` text
remuneração × 14%
```

quando a regra for progressiva.

# 22. Mudanças dentro do ano

O motor deverá considerar alterações de tabela dentro do mesmo ano.

## 2020

``` text
01/2020 – 02/2020
```

versus:

``` text
03/2020 em diante
```

## 2023

``` text
01/2023 – 04/2023
```

versus:

``` text
05/2023 – 12/2023
```

Portanto, a unidade de decisão deve ser a **competência**, não apenas o
ano.

# 23. FASE 11 --- Tela "Verificação"

A tela:

> **🔎 Verificação**

é utilizada para validar o comportamento do motor.

# 24. Seleção do período

O usuário pode escolher:

### Todos os anos disponíveis

``` text
Todos os anos disponíveis
```

### Intervalo

Exemplo:

``` text
2021 a 2022
```

### Um ano

Exemplo:

``` text
2022
```

# 25. Seleção da fonte

Depois de escolher o período, o usuário seleciona a fonte/vínculo.

O sistema carrega o histórico mensal daquela fonte no período.

# 26. Consolidação por competência

Registros correspondentes à mesma:

``` text
fonte + competência
```

são consolidados antes da verificação.

# 27. Resultado da verificação

A tela apresenta informações como:

-   total da remuneração;
-   Previdência DIRF;
-   contribuição calculada;
-   diferença;
-   quantidade de competências compatíveis;
-   competências para análise;
-   competências sem comparação;
-   competências sem tabela.

# 28. Tabela de verificação

A tabela apresenta:

  Campo
  ------------------
  Competência
  Metodologia
  Tabela
  Remuneração
  Previdência DIRF
  Calculada
  Diferença
  Status

# 29. Status

Podem aparecer situações como:

``` text
COMPATÍVEL
PARA ANÁLISE
SEM COMPARAÇÃO
SEM TABELA
```

# 30. Tolerância

A tolerância padrão atual é:

``` text
R$ 0,01
```

O usuário pode definir uma tolerância personalizada.

# 31. Tolerância com maior precisão

A interface permite trabalhar com até três casas decimais quando
necessário.

Exemplo:

``` text
R$ 0,011
```

# 32. Regra de comparação da tolerância

A comparação é realizada utilizando a diferença interna antes do
arredondamento visual.

Exemplo:

``` text
Diferença interna:
R$ 0,011

Exibição:
R$ 0,01
```

Se a tolerância for:

``` text
R$ 0,010
```

o resultado poderá ser:

``` text
PARA ANÁLISE
```

porque:

``` text
0,011 > 0,010
```

# 33. Origem da tolerância

O sistema registra:

``` text
SISTEMA — PADRÃO
```

ou:

``` text
USUÁRIO
```

# 34. Detalhamento por competência

A seção:

> **Detalhamento por competência**

é **obrigatória e deve ser preservada nas próximas versões**.

Cada competência pode ser aberta individualmente.

# 35. Informações do detalhamento

Cada competência deverá permitir visualizar:

-   status;
-   competência;
-   remuneração;
-   contribuição calculada;
-   metodologia;
-   tabela;
-   teto;
-   fonte;
-   tolerância utilizada;
-   origem da tolerância;
-   diferença interna;
-   Previdência DIRF;
-   contribuição calculada;
-   faixas progressivas.

# 36. Importância do detalhamento

O usuário precisa conseguir responder:

> "De onde veio esse valor?"

A cadeia deve ser reconstruível:

``` text
documento
 ↓
fonte
 ↓
competência
 ↓
remuneração
 ↓
regra
 ↓
faixas
 ↓
teto
 ↓
contribuição calculada
 ↓
contribuição informada
 ↓
diferença
```

# 37. FASE 12 --- Validação progressiva

Esta etapa ainda está em desenvolvimento.

O motor deverá ser validado em situações diferentes:

1.  primeira faixa;
2.  duas faixas;
3.  três faixas;
4.  quatro faixas;
5.  remuneração acima do teto;
6.  mudança de tabela;
7.  mudança de regra durante o ano;
8.  múltiplas fontes na mesma competência.

# 38. Validação inteligente

O objetivo é evitar a conferência manual de todas as competências.

O sistema poderá selecionar automaticamente casos representativos:

``` text
primeira faixa
duas faixas
três faixas
quatro faixas
acima do teto
transição de tabela
múltiplos vínculos
```

O especialista valida os casos relevantes.

# 39. FASE 13 --- Múltiplos vínculos

Esta é uma das etapas técnicas mais importantes ainda a consolidar.

O sistema não deverá calcular cada empresa isoladamente quando a regra
exigir consideração conjunta.

Exemplo:

``` text
Empresa A → R$ 4.000
Empresa B → R$ 5.000

Total → R$ 9.000
```

O tratamento deverá considerar as regras aplicáveis à remuneração
conjunta.

# 40. Problema dos múltiplos vínculos

Evitar:

``` text
Empresa A → cálculo independente
Empresa B → cálculo independente
```

quando a regra exigir:

``` text
COMPETÊNCIA
 ↓
TODAS AS FONTES RELEVANTES
 ↓
REMUNERAÇÃO CONSOLIDADA
 ↓
APLICAÇÃO DA REGRA
```

# 41. Contribuição efetivamente informada

O sistema precisa somar as contribuições constantes da DIRF.

Exemplo:

``` text
Fonte A → R$ 671,11
Fonte B → R$ 300,00
Fonte C → R$ 1.008,00
```

Total:

``` text
R$ 1.979,11
```

# 42. FASE 14 --- Motor das categorias 11% e 20%

A lógica atual trabalha com a utilização do teto entre categorias.

Conceitualmente:

``` text
remuneração sujeita a 11%
 ↓
aplicação do teto
 ↓
espaço restante
 ↓
remuneração sujeita a 20%
 ↓
limitação pelo espaço restante
```

# 43. Exemplo conceitual

Se:

``` text
Teto = R$ 7.000
Remuneração 11% = R$ 4.000
```

resta:

``` text
R$ 3.000
```

para utilização da categoria de 20%, conforme a regra adotada pelo
motor.

# 44. Exemplo com remuneração 11% acima do teto

Se:

``` text
Teto = R$ 7.000
Remuneração 11% = R$ 10.000
```

a base fica limitada a:

``` text
R$ 7.000
```

e não resta espaço para a categoria de 20%.

# 45. FASE 15 --- Contribuição máxima

O motor deverá determinar:

> **Qual é a contribuição previdenciária máxima aplicável àquela
> competência?**

Isso depende de:

-   categoria;
-   remuneração;
-   teto;
-   tabela;
-   alíquota;
-   progressividade;
-   múltiplos vínculos;
-   regra da competência.

# 46. FASE 16 --- Comparação central

A operação fundamental será:

``` text
CONTRIBUIÇÃO EFETIVA
-
CONTRIBUIÇÃO MÁXIMA
=
EXCESSO
```

Se:

``` text
efetiva > máxima
```

há excesso.

Se:

``` text
efetiva <= máxima
```

não há excesso.

# 47. Exemplo

``` text
Contribuições efetivas:
R$ 1.500,00

Contribuição máxima:
R$ 1.200,00

Excesso:
R$ 300,00
```

# 48. FASE 17 --- Apuração por competência

O cálculo definitivo deverá produzir uma linha por competência.

Exemplo:

  Competência          Efetiva         Máxima      Excesso
  ------------- -------------- -------------- ------------
  01/2021         R\$ 1.500,00   R\$ 1.200,00   R\$ 300,00
  02/2021           R\$ 900,00     R\$ 900,00     R\$ 0,00
  03/2021         R\$ 1.700,00   R\$ 1.250,00   R\$ 450,00

# 49. FASE 18 --- Período como escopo real do cálculo

O período informado pelo usuário deverá controlar o cálculo definitivo.

Exemplo:

``` text
01/2021 a 12/2022
```

O motor utilizará somente:

``` text
01/2021
02/2021
...
12/2021
01/2022
...
12/2022
```

# 50. Resultado final do período

O sistema deverá apresentar algo como:

``` text
PERÍODO ANALISADO
01/2021 a 12/2022

TOTAL DE CONTRIBUIÇÕES INFORMADAS
R$ X.XXX,XX

TOTAL DE CONTRIBUIÇÕES MÁXIMAS
R$ X.XXX,XX

TOTAL DE CONTRIBUIÇÕES ACIMA DO TETO
R$ X.XXX,XX
```

# 51. FASE 19 --- Demonstração horizontal

A tela:

> **📊 Demonstração**

deverá seguir a lógica da planilha de referência.

Para cada fonte, deverá ser possível apresentar:

``` text
Remuneração
Contribuição
```

e posteriormente os campos consolidados:

``` text
Total de contribuições
Teto
Contribuição máxima
Excesso
```

# 52. Estrutura pretendida

Exemplo:

``` text
Competência

A Remuneração
A Contribuição

B Remuneração
B Contribuição

C Remuneração
C Contribuição

...

Total contribuições
Teto
Contribuição máxima
Excesso
```

# 53. FASE 20 --- Exportação

O sistema deverá manter exportações para:

-   JSON completo;
-   JSON RAW;
-   CSV normalizado;
-   CSV da apuração;
-   validação de totais;
-   tabelas históricas;
-   demonstração.

# 54. JSON completo

Deverá representar o processamento completo, incluindo, conforme a
arquitetura final:

``` text
informações do arquivo
dados RAW
fontes
agrupamentos
classificações
origem da classificação
tabelas utilizadas
configurações
período
resultados
auditoria
```

# 55. JSON RAW

Deverá representar essencialmente:

> aquilo que foi extraído da DIRF.

Sua finalidade é permitir reprocessamento e auditoria.

# 56. CSV normalizado

Deverá ser útil para:

-   Excel;
-   conferência;
-   análise externa;
-   auditoria;
-   comparação.

# 57. CSV da apuração

Deverá permitir exportar a demonstração final por competência:

``` text
Competência
Remuneração
Contribuição DIRF
Contribuição máxima
Excesso
Status
```

# 58. FASE 21 --- Auditoria

Para uma competência específica, deverá ser possível reconstruir:

``` text
Qual documento?
↓
Qual página?
↓
Qual declarante?
↓
Qual CNPJ?
↓
Qual código DIRF?
↓
Qual remuneração?
↓
Qual contribuição?
↓
Qual classificação?
↓
Quem classificou?
↓
Qual tabela?
↓
Qual teto?
↓
Qual regra?
↓
Qual cálculo?
↓
Qual resultado?
```

# 59. Origem da classificação

Deverá permanecer registrada.

Exemplo:

``` text
Fonte:
EMPRESA X

Classificação:
20%

Origem:
AUTOMÁTICA
```

ou:

``` text
Origem:
USUÁRIO
```

# 60. FASE 22 --- Tratamento das exceções

O sistema deverá identificar situações como:

``` text
CLASSIFICAÇÃO PENDENTE
TETO NÃO CADASTRADO
COMPETÊNCIA SEM TABELA
FONTE SEM CLASSIFICAÇÃO
DADOS INSUFICIENTES
SITUAÇÃO QUE EXIGE ANÁLISE
```

# 61. Princípio: automatizar sem ocultar incerteza

A regra será:

### Quando houver segurança

``` text
CALCULAR AUTOMATICAMENTE
```

### Quando houver dúvida

``` text
SINALIZAR
```

### Quando depender de decisão humana

``` text
SOLICITAR CONFIRMAÇÃO
```

### Nunca

``` text
INVENTAR UMA REGRA
```

# 62. FASE 23 --- Validação com a planilha de referência

A planilha de demonstração utilizada no projeto deverá servir como
referência para comparar:

``` text
Sistema
×
Planilha de referência
```

competência por competência.

# 63. Casos de referência identificados

Foram observadas situações importantes:

### Janeiro/2020

Fonte com remuneração/contribuição de 11% junto a fonte de 20%.

### Fevereiro/2022

Remuneração de 11% e remuneração de 20%, com utilização do espaço
restante do teto.

### Março/2022

Remuneração de 11% acima do teto.

### Abril/2022

Remuneração de 11% + remuneração de 20%, utilizando o saldo do teto.

### Janeiro/2024

Remuneração de 11% acima do teto e contribuição efetiva superior ao
máximo.

Esses casos são bons candidatos a testes automatizados.

# 64. FASE 24 --- Testes automatizados

Os testes deverão cobrir:

``` text
extração
estrutura dos registros
totais
classificação
tabelas
teto
11%
20%
progressiva
múltiplos vínculos
arredondamento
tolerância
período
excesso
exportação
```

# 65. FASE 25 --- Testes de regressão

Cada nova versão deverá preservar o funcionamento das anteriores.

Uma alteração visual não pode quebrar o extrator.

Uma alteração no cálculo não pode destruir o RAW.

# 66. FASE 26 --- Separação entre interface e motor

A arquitetura deverá manter separadas:

``` text
INTERFACE
EXTRAÇÃO
CLASSIFICAÇÃO
TABELAS
MOTOR DE CÁLCULO
VALIDAÇÃO
EXPORTAÇÃO
```

# 67. FASE 27 --- O que não deve ser feito

### Não reconstruir o extrator sem necessidade

O motor atual já possui trabalho significativo.

### Não apagar registros considerados irrelevantes

Eles devem permanecer no RAW.

### Não obrigar classificação manual de tudo

O objetivo é automação.

### Não usar uma única tabela para todos os anos

O teto e as regras são históricos.

### Não calcular progressiva simplesmente multiplicando a remuneração pela maior alíquota

As faixas precisam ser respeitadas.

### Não calcular múltiplos vínculos isoladamente quando a regra exigir consolidação

Esse é um ponto crítico.

### Não esconder situações não resolvidas

Elas devem aparecer como exceção.

# 68. FASE 28 --- Fluxo do usuário no sistema final

## PASSO 1 --- Upload

Usuário:

``` text
Seleciona o PDF da DIRF
```

Sistema:

``` text
Lê
↓
processa
↓
extrai
```

## PASSO 2 --- Conferência da extração

Sistema apresenta:

``` text
Arquivo processado
Páginas
Registros
Declarações
Fontes identificadas
```

## PASSO 3 --- Seleção das fontes

Sistema sugere fontes previdenciárias.

Fontes claramente não previdenciárias ficam fora por padrão.

Usuário corrige somente exceções.

## PASSO 4 --- Classificação

Sistema tenta classificar automaticamente:

``` text
11%
20%
PROGRESSIVA
```

Usuário confirma apenas casos necessários.

## PASSO 5 --- Período

Usuário informa:

``` text
01/2021 a 12/2022
```

## PASSO 6 --- Processamento

Sistema:

``` text
identifica competências
↓
seleciona tabela
↓
identifica teto
↓
identifica categorias
↓
consolida vínculos
↓
calcula
```

## PASSO 7 --- Validação

Sistema apresenta:

``` text
competências compatíveis
competências para análise
exceções
```

e mantém o:

> **Detalhamento por competência**

## PASSO 8 --- Apuração

Sistema calcula:

``` text
contribuição efetiva
-
contribuição máxima
=
excesso
```

## PASSO 9 --- Resultado

Apresenta:

``` text
TOTAL CONTRIBUÍDO
R$ ...

TOTAL MÁXIMO
R$ ...

TOTAL ACIMA DO TETO
R$ ...
```

## PASSO 10 --- Demonstração

Usuário pode consultar a demonstração horizontal.

## PASSO 11 --- Exportação

Usuário pode gerar os arquivos de conferência e auditoria.

# 69. FASE 29 --- Resultado profissional pretendido

O resultado final deverá informar:

``` text
PERÍODO:
01/2021 a 12/2022

TOTAL DE REMUNERAÇÕES:
R$ XXX.XXX,XX

TOTAL DE CONTRIBUIÇÕES INFORMADAS:
R$ XX.XXX,XX

TOTAL DE CONTRIBUIÇÕES MÁXIMAS:
R$ XX.XXX,XX

TOTAL ACIMA DO LIMITE:
R$ X.XXX,XX
```

Abaixo deverá existir a memória por competência.

# 70. FASE 30 --- Memória de cálculo

Para cada competência deverá ser possível visualizar:

``` text
Fontes consideradas
Remunerações
Contribuições informadas
Categoria de cada fonte
Tabela utilizada
Faixas
Teto
Base de cálculo
Contribuição máxima
Contribuição efetiva
Excesso
Status
```

# 71. FASE 31 --- Resultado consolidado

Exemplo:

``` text
01/2021 → excesso X
02/2021 → excesso Y
03/2021 → excesso Z
...
12/2022 → excesso W
```

Depois:

``` text
SOMA DOS EXCESSOS
```

# 72. FASE 32 --- Competências sem excesso

A demonstração não deverá apresentar somente os meses com excesso.

As competências sem excesso também deverão poder ser visualizadas.

Isso demonstra que o período inteiro foi analisado.

# 73. FASE 33 --- Competências com inconsistência

Situações não resolvidas deverão ser destacadas.

Exemplo:

``` text
04/2022 → calculada
05/2022 → calculada
06/2022 → classificação pendente
07/2022 → calculada
```

O sistema não deverá simplesmente ignorar junho.

# 74. FASE 34 --- Confiabilidade do cálculo

Antes do motor ser considerado definitivo, deverá ocorrer validação
especializada.

O especialista deverá conferir:

1.  classificação das fontes;
2.  regras dos 11%;
3.  regras dos 20%;
4.  progressividade;
5.  teto;
6.  múltiplos vínculos;
7.  transições de tabela;
8.  tratamento da contribuição efetiva;
9.  cálculo do excesso;
10. período;
11. arredondamentos;
12. exceções.

# 75. FASE 35 --- Validação jurídica/técnica

Antes da integração definitiva do motor, a equipe deverá responder:

``` text
Quem pertence a cada categoria?
Qual regra aplicar?
Qual alíquota?
Qual base?
Qual teto?
Como tratar múltiplos vínculos?
Como tratar contribuição já recolhida?
Como tratar fontes simultâneas?
Como tratar 13º?
Como tratar mudanças legislativas?
```

A categoria:

``` text
PROGRESSIVA
```

deverá receber atenção especial.

# 76. FASE 36 --- O que não deve ser inferido somente pela DIRF

O código DIRF não deve ser tratado automaticamente como uma
classificação previdenciária legal completa.

A lógica deverá ser:

``` text
Código DIRF
 ↓
informação de natureza
 ↓
regra de classificação
 ↓
categoria previdenciária
```

e não:

``` text
Código DIRF
 ↓
alíquota automática sem validação
```

# 77. FASE 37 --- Limites do sistema

O manual definitivo deverá informar claramente:

### O que o sistema consegue determinar automaticamente

versus:

### O que depende de informação ou decisão do usuário/especialista.

Isso evita interpretações indevidas sobre o resultado.

# 78. FASE 38 --- Experiência final desejada

Idealmente o usuário fará:

``` text
1. Enviar PDF
2. Conferir fontes excepcionais
3. Confirmar classificações excepcionais
4. Informar período
5. Conferir resultado
6. Exportar
```

Em vez de realizar manualmente toda a cadeia de cálculos em Excel.

# 79. FASE 39 --- Arquitetura final

``` text
                    ┌──────────────────┐
                    │    PDF / DIRF    │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │     EXTRATOR     │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │    BASE RAW      │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ IDENTIFICAÇÃO    │
                    │ DAS FONTES       │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ AGRUPAMENTO      │
                    │ DE VÍNCULOS      │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ CLASSIFICAÇÃO    │
                    │ AUTOMÁTICA       │
                    └────────┬─────────┘
                             ↓
                 ┌───────────┴───────────┐
                 ↓                       ↓
          AUTOMÁTICO                EXCEÇÃO
                 ↓                       ↓
                 └───────────┬───────────┘
                             ↓
                    ┌──────────────────┐
                    │ TABELA HISTÓRICA │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ MÚLTIPLOS        │
                    │ VÍNCULOS         │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ MOTOR DE         │
                    │ CONTRIBUIÇÃO     │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ CONTRIBUIÇÃO     │
                    │ EFETIVA          │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ CONTRIBUIÇÃO     │
                    │ MÁXIMA           │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ EXCESSO          │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ DEMONSTRAÇÃO     │
                    │ POR COMPETÊNCIA  │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ RESULTADO FINAL  │
                    └────────┬─────────┘
                             ↓
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
            JSON           CSV/Excel       RELATÓRIO
```

# 80. Roadmap resumido

  -------------------------------------------------------------------------
  Fase                    Etapa                   Situação
  ----------------------- ----------------------- -------------------------
  1                       Extração DIRF           ✅ Concluída

  2                       Preservação RAW         ✅ Concluída

  3                       Filtros                 ✅ Concluída

  4                       Identificação de fontes ✅ Concluída

  5                       Agrupamento             ✅ Concluída

  6                       Seleção inteligente     ✅ Concluída

  7                       Classificação           ✅ Implementada
                          11/20/Progressiva       

  8                       Classificação           ✅ Implementada na V1.2.8
                          automática              

  9                       Tabelas históricas      🟡 Funcional

  10                      Verificação mensal      ✅ Funcional

  11                      Detalhamento por        ✅ Implementado
                          competência             

  12                      Tolerância              ✅ Implementada

  13                      Validação progressiva   🟡 Em validação

  14                      Múltiplos vínculos      🟡 Implementação inicial
                                                  na Apuração;
                                                  validação/generalização
                                                  pendente

  15                      Motor 11%/20%           🟡 Parcial / em validação
                          definitivo              

  16                      Motor progressivo       🔜 Após validação
                          definitivo              

  17                      Excesso por competência 🟡 Implementação inicial
                                                  na Apuração; validação
                                                  pendente

  18                      Excesso por período     🟡 Escopo por período
                                                  implementado; validação
                                                  final pendente

  19                      Demonstração horizontal 🟡 Em evolução

  20                      Exportação              🟡 Funcional

  21                      Memória de cálculo      🔜

  22                      Auditoria completa      🔜

  23                      Testes automatizados    🔜
                          completos               

  24                      Validação por           🔜
                          especialista            

  25                      Motor definitivo        🔜

  26                      Sistema final           🔜
  -------------------------------------------------------------------------

# 80-A. ATUALIZAÇÃO DA V1.2.10 --- ESTADO ATUAL DO PROJETO

Esta seção complementa as fases acima para registrar as decisões
efetivamente tomadas após a versão-base deste roadmap.

## 80-A.1. V1.2.8 --- Classificação automática

A classificação deixou de ser apenas uma seleção manual.

O sistema passou a trabalhar conceitualmente com:

``` text
classificacao_sugerida
classificacao_final
origem_classificacao
nivel_confianca
evidencias
regra_classificacao
versao_regra
```

A classificação final continua editável pelo usuário.

O princípio é:

``` text
sistema sugere
      ↓
usuário confirma ou altera
      ↓
classificação final
```

A alteração humana não deve apagar a sugestão original. A
rastreabilidade é necessária para saber se a decisão foi automática ou
confirmada pelo usuário.

### Grupos

``` text
11%
20%
PROGRESSIVA
NÃO DEFINIDO
```

O grupo `NÃO DEFINIDO` permanece como mecanismo de segurança para
impedir que uma situação não resolvida seja tratada silenciosamente como
outra categoria.

## 80-A.2. V1.2.9 --- Apuração

A consolidação passou a ser responsabilidade da guia:

> **🧮 Apuração**

A Verificação não deve ser transformada em uma planilha de consolidação
final.

A Apuração recebe as fontes classificadas e organiza os dados por
competência.

Modelo:

``` text
COMPETÊNCIA
    ↓
FONTES SELECIONADAS
    ↓
CLASSIFICAÇÃO DE CADA FONTE
    ↓
CONSOLIDAÇÃO
    ↓
TETO
    ↓
CONTRIBUIÇÃO MÁXIMA
    ↓
CONTRIBUIÇÃO EFETIVA
    ↓
EXCESSO
```

A implementação atual é preparada para mais de dois vínculos. Os dois
vínculos presentes na planilha de referência são casos práticos de
validação.

## 80-A.3. V1.2.10 --- Escopo da Apuração

A Apuração passou a possuir dois controles essenciais:

### Período

O usuário define o intervalo que será efetivamente apurado.

Exemplos:

``` text
Todo o período
Um ano
Intervalo personalizado
```

### Declarantes

O usuário define quais declarantes participarão da apuração.

O sistema deve deixar explícito:

``` text
DECLARANTES UTILIZADOS NA APURAÇÃO
```

com:

-   nome;
-   CNPJ;
-   grupo/classificação.

O número de declarantes utilizados também deve ficar visível.

Isso é uma exigência de rastreabilidade do resultado.

## 80-A.4. Exemplo prático não deve limitar o motor

A referência atual possui dois vínculos:

``` text
Sociedade Pernambucana
+
Coopanest
```

Isso é um exemplo concreto.

O motor deve trabalhar com:

``` text
N declarantes / vínculos
```

e não com uma estrutura fixa de duas fontes.

## 80-A.5. Janeiro/2025

O caso de janeiro/2025 deve ser utilizado como teste de referência para
uma combinação:

``` text
Progressiva
+
20%
```

A planilha de referência apresenta, em síntese:

``` text
Contribuição efetiva:        R$ 1.090,66
Contribuição máxima:         R$ 1.081,45
Excesso:                     R$     9,21
```

O valor deve ser conferido contra a planilha e contra o cálculo interno
do sistema.

## 80-A.6. Julho/2025

Julho/2025 é um caso de teste especialmente importante.

A fonte progressiva apresenta remuneração superior ao teto.

Assim:

``` text
Teto 2025
R$ 8.157,41

Progressiva
R$ 13.555,14
        ↓
ocupa integralmente o teto

Saldo para 20%
R$ 0,00

Máximo 20%
R$ 0,00
```

A planilha de referência indica:

``` text
Contribuição efetiva:        R$ 1.670,41
Contribuição máxima:         R$   951,64
Excesso:                     R$   718,77
```

Este caso demonstra por que o cálculo não pode ser:

``` text
cada CNPJ × sua alíquota
```

sem considerar o teto consolidado da competência.

## 80-A.7. Relação Classificação → Verificação

A classificação confirmada pelo usuário deve alimentar a coluna:

> **Previdência Calculada**

na Verificação.

Exemplo:

``` text
Classificação confirmada:
20%

Remuneração:
R$ 5.000,00

Previdência Calculada:
R$ 5.000,00 × 20%
```

O cálculo deve respeitar o teto e as demais regras da competência.

A coluna:

> **Previdência DIRF**

permanece representando o valor original informado na DIRF.

Portanto:

``` text
Previdência DIRF
≠
Previdência Calculada
```

necessariamente.

A comparação entre ambas é parte da conferência.

## 80-A.8. Verificação × Apuração

A separação de responsabilidades fica definida assim:

### Verificação

Pergunta:

> O valor informado na DIRF é compatível com o cálculo da fonte segundo
> a classificação e a regra aplicável?

### Apuração

Pergunta:

> Considerando todos os declarantes selecionados na competência, qual é
> a contribuição máxima aplicável e quanto foi efetivamente recolhido
> acima desse limite?

Essa separação deve ser preservada.

## 80-A.9. 13º

O 13º deve aparecer na interface imediatamente depois de dezembro:

``` text
12/2025
13º/2025
01/2026
```

Internamente deve permanecer identificado como:

``` text
ano_referencia = 2025
tipo = "13º"
```

e não como uma competência mensal `13/2025`.

O 13º não deve ser somado à remuneração mensal de dezembro para
aplicação das faixas.

O tratamento consolidado definitivo do 13º continua sujeito a validação
específica.

## 80-A.10. Legenda de status

A apresentação da Verificação deverá tornar os status imediatamente
compreensíveis.

Preferência visual:

``` text
🟢 Compatível
🟡 Para análise
```

O amarelo representa necessidade de conferência, não necessariamente
erro.

A representação visual deve ser consistente entre legenda, tabela e
detalhamento.

## 80-A.11. Apuração como escopo real

O período e os declarantes escolhidos na Apuração não são apenas filtros
visuais.

Eles definem o conjunto de dados que participa efetivamente do cálculo.

Portanto:

``` text
PERÍODO ESCOLHIDO
+
DECLARANTES ESCOLHIDOS
=
ESCOPO DA APURAÇÃO
```

Esse escopo deve ser preservado na memória e nas exportações.

## 80-A.12. Regra de versionamento

A versão do código deve coincidir com a pasta interna do ZIP e com a
documentação entregue.

Exemplo:

``` text
V1.2.10
extrator_dirf_motor_v1_2_10/
```

Não deve voltar a ocorrer uma pasta interna identificada como versão
anterior.

# 81. Prioridade antes de escrever qualquer novo código

Neste momento, o recomendado é **não iniciar uma nova versão do
código**.

A equipe deve validar especialmente:

## BLOCO A --- Extração

-   O que exatamente deve ser extraído?
-   Existem campos faltantes?
-   O extrator atual atende aos modelos de DIRF utilizados?
-   Há necessidade de OCR?
-   Qual o limite operacional de páginas?

## BLOCO B --- Fontes

-   Como identificar definitivamente uma fonte previdenciária?
-   Quais códigos podem ser excluídos automaticamente?
-   Quais exigem confirmação?

## BLOCO C --- Classificação

-   Quais fontes são 11%?
-   Quais são 20%?
-   Quais são progressivas?
-   O que pode ser classificado automaticamente?
-   O que exige confirmação?

## BLOCO D --- Progressividade

-   Qual regra exata?
-   Como calcular cada faixa?
-   Como tratar múltiplos vínculos?
-   Como tratar contribuições já recolhidas?
-   Como tratar mudanças de tabela?

## BLOCO E --- Excesso

-   Qual grandeza deve ser comparada?
-   Como consolidar contribuições?
-   Como aplicar o teto entre categorias?
-   Como tratar cada competência?

## BLOCO F --- Resultado

-   O que o advogado precisa visualizar?
-   Qual memória de cálculo é necessária?
-   Qual relatório será utilizado?
-   Quais informações precisam ser auditáveis?

# 82. Pergunta central para o especialista

A pergunta que deve orientar a validação é:

> **"Dada a informação existente na DIRF, qual é exatamente a regra
> jurídica e matemática que determina, competência por competência, o
> valor máximo de contribuição previdenciária que poderia ter sido
> recolhido pelo segurado, considerando todas as fontes e categorias
> aplicáveis?"**

A partir dessa resposta, o software poderá transformar a regra em
cálculo.

# 83. Estado atual do projeto

O sistema já possui uma estrutura muito além de um simples extrator:

``` text
EXTRAÇÃO
+
RAW
+
FILTROS
+
FONTES
+
AGRUPAMENTO
+
CLASSIFICAÇÃO
+
TABELAS HISTÓRICAS
+
VERIFICAÇÃO
+
TOLERÂNCIA
+
DETALHAMENTO
+
APURAÇÃO INICIAL
+
DEMONSTRAÇÃO
+
EXPORTAÇÃO
```

O principal trabalho restante para chegar ao sistema definitivo está
concentrado em:

``` text
CLASSIFICAÇÃO AUTOMÁTICA
        ↓
VALIDAÇÃO DA PROGRESSIVA
        ↓
MÚLTIPLOS VÍNCULOS
        ↓
CONTRIBUIÇÃO MÁXIMA
        ↓
EXCESSO
        ↓
RESULTADO FINAL POR PERÍODO
```

# 84. Objetivo final em uma frase

> **O sistema deverá permitir que o usuário envie a DIRF, informe o
> período que deseja analisar e, após apenas as confirmações realmente
> necessárias, obtenha uma demonstração auditável de quanto foi
> efetivamente recolhido, quanto poderia ter sido recolhido segundo a
> regra previdenciária aplicável a cada competência e qual foi o valor
> total pago acima do limite previdenciário no período analisado.**

------------------------------------------------------------------------

## DECISÃO DE PROJETO

**Este documento deve ser tratado como o roadmap funcional de referência
antes da próxima etapa de programação.**

Antes de gerar uma nova versão do código:

1.  a equipe deve ler o documento;
2.  o especialista deve validar as regras previdenciárias;
3.  devem ser identificadas eventuais regras faltantes;
4.  devem ser corrigidas ambiguidades;
5.  devem ser definidas as situações que podem ser automatizadas;
6.  devem ser definidos os casos que exigirão confirmação humana;
7.  somente então deverá ser fechado o próximo desenho técnico do motor.
