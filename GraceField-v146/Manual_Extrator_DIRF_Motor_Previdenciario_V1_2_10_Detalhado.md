# MANUAL FUNCIONAL E TÉCNICO

## Extrator DIRF + Motor Previdenciário

**Versão:** 1.2.10\
**Documento:** manual detalhado de operação, arquitetura e regras
funcionais\
**Finalidade:** orientar o uso do sistema, a conferência dos resultados
e a evolução técnica do projeto.

------------------------------------------------------------------------

# 1. Visão geral

O sistema transforma informações estruturadas encontradas em arquivos
DIRF em uma sequência de tratamento previdenciário.

O objetivo final é permitir que o usuário selecione um período e
fontes/declarantes e obtenha uma apuração auditável da contribuição
efetivamente informada, da contribuição máxima aplicável e do eventual
valor acima do limite previdenciário.

Fluxo:

``` text
DIRF
 ↓
EXTRAÇÃO
 ↓
RAW
 ↓
FONTES
 ↓
AGRUPAMENTO
 ↓
CLASSIFICAÇÃO
 ↓
VERIFICAÇÃO
 ↓
APURAÇÃO
 ↓
DEMONSTRAÇÃO
 ↓
EXPORTAÇÃO / AUDITORIA
```

------------------------------------------------------------------------

# 2. Princípio de preservação do dado

O sistema deve separar três camadas.

## 2.1. RAW / dado original

É o que foi encontrado na DIRF.

Exemplos:

-   nome;
-   CNPJ;
-   código DIRF;
-   descrição;
-   competência;
-   rendimento tributável;
-   Previdência Oficial;
-   IRRF;
-   13º;
-   página;
-   arquivo de origem;
-   número do processo;
-   demais campos extraídos.

O RAW não deve ser modificado para acomodar uma regra de cálculo.

## 2.2. Dado tratado

É o resultado da organização.

Exemplos:

-   fonte selecionada;
-   vínculo;
-   grupo;
-   classificação;
-   origem da classificação;
-   confiança;
-   evidências.

## 2.3. Dado calculado

É o resultado do motor.

Exemplos:

-   base;
-   teto;
-   faixas;
-   alíquotas;
-   contribuição máxima;
-   contribuição efetiva consolidada;
-   excesso.

------------------------------------------------------------------------

# 3. Extração

A primeira etapa recebe o PDF DIRF.

O extrator percorre o documento e organiza os dados.

Arquivo de referência utilizado nos testes:

``` text
Suzana Marine - DIRFs.pdf
```

Teste realizado:

-   135 páginas;
-   1.414 registros;
-   101 blocos de declaração.

Esses números não constituem limite técnico.

O sistema deve continuar preparado para tratar documentos maiores,
observando os limites de memória e processamento que forem definidos
posteriormente.

------------------------------------------------------------------------

# 4. Campos extraídos

Entre os campos relevantes:

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

Também são preservados:

-   nome do declarante;
-   CNPJ;
-   código DIRF;
-   descrição;
-   competência;
-   Tot;
-   13º;
-   página;
-   arquivo de origem;
-   fundo/clube;
-   processo.

------------------------------------------------------------------------

# 5. Competência

Para valores mensais, a apresentação utiliza:

``` text
01/2025
02/2025
...
12/2025
```

Para o décimo terceiro:

``` text
13º/2025
```

O 13º não é um décimo terceiro mês da série mensal. É uma
competência/tipo próprio.

------------------------------------------------------------------------

# 6. Tela Extração e filtros

A tela permite explorar os dados extraídos.

Filtros relevantes:

-   ano;
-   declarante;
-   CNPJ;
-   código DIRF;
-   tipo;
-   grupo;
-   competência.

Formatação:

``` text
Competência → MM/AAAA
Data completa → DD/MM/AAAA
Valor → R$ 1.234,56
Percentual → 7,50%
CNPJ → 00.000.000/0000-00
```

------------------------------------------------------------------------

# 7. Seleção de fontes

A DIRF pode conter fontes previdenciárias e fontes que não pertencem ao
cálculo previdenciário.

Fontes claramente incompatíveis com o objetivo podem ser desmarcadas por
padrão.

Exemplos de códigos encontrados na base:

``` text
5706
5557
6800
6813
8053
```

A exclusão da seleção não significa apagar o registro.

O dado continua no RAW.

------------------------------------------------------------------------

# 8. Agrupamento de vínculos

A tela de agrupamento organiza as fontes.

A identificação deve priorizar:

``` text
Nome do declarante
CNPJ
```

O sistema deve permitir selecionar as fontes relevantes e preservar as
demais.

O objetivo é chegar a uma lista clara das fontes que poderão participar
das etapas seguintes.

------------------------------------------------------------------------

# 9. Classificação previdenciária

Os grupos utilizados são:

``` text
11%
20%
PROGRESSIVA
NÃO DEFINIDO
```

## 9.1. 11%

Grupo de contribuição fixa de 11%, submetido às regras e limitações
aplicáveis à competência.

## 9.2. 20%

Grupo de contribuição fixa de 20%.

A base efetivamente considerada deve respeitar o teto e o espaço
disponível no cálculo consolidado da competência.

## 9.3. Progressiva

Grupo que utiliza a tabela histórica progressiva correspondente à
competência.

Não se deve simplesmente aplicar a maior alíquota sobre toda a
remuneração.

## 9.4. Não definido

Indica que ainda não há classificação suficiente para prosseguir com
segurança.

------------------------------------------------------------------------

# 10. Classificação automática

A V1.2.8 introduziu a classificação automática.

O sistema pode analisar evidências como:

-   código DIRF;
-   natureza;
-   existência de Previdência Oficial;
-   padrão de contribuição;
-   histórico;
-   regras cadastradas;
-   classificações previamente confirmadas.

A classificação automática não deve ser confundida com uma conclusão
jurídica absoluta.

A estrutura deve distinguir:

``` text
classificacao_sugerida
classificacao_final
origem_classificacao
nivel_confianca
evidencias
regra_classificacao
versao_regra
```

------------------------------------------------------------------------

# 11. Edição pelo usuário

A sugestão automática deve permanecer editável.

Fluxo:

``` text
SISTEMA
 ↓
Sugestão
 ↓
Usuário confirma
ou
Usuário altera
 ↓
Classificação final
```

Se o usuário alterar, a origem deve registrar:

``` text
usuario
```

Se não houver intervenção:

``` text
automatico
```

A sugestão original deve permanecer disponível para auditoria.

------------------------------------------------------------------------

# 12. Alíquota efetiva observada

A interface pode mostrar uma alíquota efetiva observada.

Conceitualmente:

``` text
Previdência Oficial
÷
Rendimento Tributável
× 100
```

Essa informação é diagnóstica.

Não deve ser usada isoladamente para afirmar:

``` text
11%
20%
Progressiva
```

------------------------------------------------------------------------

# 13. Tabelas históricas

A tabela aplicável deve ser identificada pela competência.

Estrutura:

``` text
competência
 ↓
vigência
 ↓
faixas
 ↓
alíquotas
 ↓
teto
```

A base atual contempla:

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

Devem ser preservadas as mudanças ocorridas dentro do ano.

Exemplos:

``` text
2020:
01/2020–02/2020
03/2020 em diante

2023:
01/2023–04/2023
05/2023–12/2023
```

------------------------------------------------------------------------

# 14. Verificação

A Verificação é a camada de conferência.

Ela pode trabalhar com:

-   todos os anos;
-   um ano;
-   intervalo;
-   fonte/declarantes selecionados.

A tabela apresenta:

  Campo              Função
  ------------------ ----------------------------
  Competência        competência analisada
  Metodologia        regra utilizada
  Tabela             tabela histórica
  Remuneração        base informada/considerada
  Previdência DIRF   valor original
  Calculada          resultado do cálculo
  Diferença          comparação
  Status             situação da conferência

------------------------------------------------------------------------

# 15. Previdência DIRF x Previdência Calculada

São grandezas diferentes.

### Previdência DIRF

É o valor encontrado no documento.

### Previdência Calculada

É o valor produzido pelo sistema a partir da classificação e da regra
aplicável.

Exemplo:

``` text
Previdência DIRF:       R$ 1.000,00
Previdência Calculada:  R$   950,00
Diferença:              R$    50,00
```

A confirmação de uma classificação na tela de Classificação deve
alimentar a Previdência Calculada da Verificação.

Isso não altera o valor original da DIRF.

------------------------------------------------------------------------

# 16. Status da Verificação

Status principais:

``` text
🟢 COMPATÍVEL
🟡 PARA ANÁLISE
SEM COMPARAÇÃO
SEM TABELA
```

"Para análise" significa que existe diferença ou condição que exige
conferência. Não significa automaticamente erro.

A legenda deve ser visualmente evidente.

------------------------------------------------------------------------

# 17. Tolerância

A tolerância padrão utilizada atualmente é:

``` text
R$ 0,01
```

Pode haver tolerância personalizada.

A comparação deve ocorrer sobre o valor interno antes do arredondamento
visual.

Exemplo:

``` text
diferença interna = R$ 0,011
```

não deve ser transformada em R\$ 0,01 antes de verificar uma tolerância
de R\$ 0,010.

------------------------------------------------------------------------

# 18. Detalhamento por competência

O detalhamento deve ser preservado.

Cada competência deve permitir reconstruir:

-   status;
-   competência;
-   remuneração;
-   contribuição calculada;
-   metodologia;
-   tabela;
-   teto;
-   fonte;
-   tolerância;
-   origem da tolerância;
-   diferença interna;
-   Previdência DIRF;
-   faixas progressivas.

Pergunta que o detalhamento deve responder:

> De onde veio esse valor?

------------------------------------------------------------------------

# 19. 13º

O 13º deve aparecer imediatamente depois de dezembro.

Exemplo:

``` text
10/2025
11/2025
12/2025
13º/2025
01/2026
```

Não deve ser representado internamente como:

``` text
13/2025
```

A estrutura deve manter:

``` text
ano_referencia = 2025
tipo = "13º"
```

O 13º não deve ser somado à remuneração mensal de dezembro para
aplicação das faixas.

O cálculo consolidado específico do 13º ainda exige validação própria
antes de ser tratado como definitivo.

------------------------------------------------------------------------

# 20. Apuração

A Apuração é a etapa de consolidação.

Ela deve responder:

> Considerando o período e os declarantes selecionados, quanto foi
> efetivamente informado e qual é a contribuição máxima aplicável por
> competência?

------------------------------------------------------------------------

# 21. Definição do período

O usuário deve poder definir:

``` text
Todo o período
Um ano
Intervalo personalizado
```

Exemplo:

``` text
01/2024 a 07/2025
```

O período não é apenas um filtro visual.

Ele define o escopo real do cálculo.

------------------------------------------------------------------------

# 22. Definição dos declarantes

A Apuração deve permitir selecionar explicitamente os declarantes.

Exemplo:

``` text
☑ Sociedade Pernambucana
☑ Coopanest
☐ Outra fonte
```

Deve ficar visível:

``` text
2 declarantes utilizados na apuração
```

e:

``` text
Nome
CNPJ
Grupo
```

A seleção não apaga nenhuma fonte do RAW.

------------------------------------------------------------------------

# 23. Consolidação por competência

A Apuração deve reunir todas as fontes selecionadas que possuem dados
naquela competência.

Modelo:

``` text
07/2025

Fonte A
Progressiva
Remuneração
Contribuição

Fonte B
20%
Remuneração
Contribuição

Fonte C
...
```

Depois:

``` text
CONSOLIDAÇÃO
 ↓
TETO
 ↓
MÁXIMO
 ↓
EFETIVO
 ↓
EXCESSO
```

O modelo deve funcionar para N vínculos.

------------------------------------------------------------------------

# 24. Exemplo: janeiro/2025

Dois vínculos:

``` text
Sociedade Pernambucana → Progressiva
Coopanest → 20%
```

Referência da planilha:

``` text
Contribuição efetiva:  R$ 1.090,66
Máximo:                R$ 1.081,45
Excesso:               R$     9,21
```

Esse caso deve ser mantido como teste de regressão.

------------------------------------------------------------------------

# 25. Exemplo: julho/2025

Dados de referência:

``` text
Sociedade Pernambucana
Progressiva
R$ 13.555,14

Coopanest
20%
R$ 71.384,43
```

Teto:

``` text
R$ 8.157,41
```

A remuneração progressiva ultrapassa o teto.

Portanto:

``` text
Teto utilizado pela progressiva
= R$ 8.157,41

Saldo para 20%
= R$ 0,00
```

Conforme a planilha de referência:

``` text
Máximo progressivo = R$ 951,64
Máximo 20%         = R$   0,00
Máximo total       = R$ 951,64

Efetivamente informado = R$ 1.670,41

Excesso = R$ 718,77
```

Esse exemplo demonstra que a contribuição efetiva do vínculo de 20%
continua sendo preservada, mas o máximo permitido pela consolidação pode
ser zero.

------------------------------------------------------------------------

# 26. Regra conceitual da contribuição máxima

A pergunta do motor é:

> Qual a contribuição máxima que pode ser considerada para aquela
> competência?

A resposta depende de:

-   grupo;
-   remuneração;
-   teto;
-   tabela;
-   faixas;
-   múltiplos vínculos;
-   regras da competência.

------------------------------------------------------------------------

# 27. Progressiva

Quando a categoria é progressiva:

``` text
base
 ↓
faixa 1
 ↓
faixa 2
 ↓
faixa 3
 ↓
faixa 4
 ↓
contribuição
```

Não utilizar:

``` text
remuneração × 14%
```

como substituição da progressividade.

------------------------------------------------------------------------

# 28. 20% em conjunto com progressiva

Quando uma fonte progressiva utiliza parte do teto e outra fonte é 20%,
a Apuração deve considerar o espaço restante.

Conceito:

``` text
Teto
-
espaço utilizado pelo cálculo anterior
=
saldo disponível
```

Então:

``` text
saldo disponível
× 20%
```

limitado à remuneração da fonte.

------------------------------------------------------------------------

# 29. N vínculos

O motor não deve assumir apenas:

``` text
A + B
```

Deve aceitar:

``` text
A + B + C + D + ...
```

A quantidade de declarantes é variável.

------------------------------------------------------------------------

# 30. Contribuição efetivamente informada

A contribuição efetiva deve ser obtida a partir dos valores da DIRF das
fontes incluídas no escopo.

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

Essa soma é diferente do cálculo da contribuição máxima.

------------------------------------------------------------------------

# 31. Excesso

A operação central é:

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

O valor do excesso deve ser tratado por competência antes de ser
totalizado no período.

------------------------------------------------------------------------

# 32. Resultado por período

Ao final:

``` text
Período analisado
Declarantes utilizados

Total de contribuições informadas
R$ ...

Total de contribuições máximas
R$ ...

Total acima do teto
R$ ...
```

Abaixo, deve existir a memória por competência.

------------------------------------------------------------------------

# 33. Demonstração

A Demonstração deve aproximar a lógica da planilha de referência.

Para cada competência, futuramente:

``` text
Fonte A
Remuneração
Contribuição

Fonte B
Remuneração
Contribuição

...

Total efetivo
Teto
Máximo
Excesso
```

A planilha é referência para validação, mas o cálculo definitivo deve
ser executado pelo sistema.

------------------------------------------------------------------------

# 34. Auditoria

Para uma competência, deve ser possível responder:

``` text
Qual arquivo?
Qual página?
Qual declarante?
Qual CNPJ?
Qual código?
Qual remuneração?
Qual contribuição?
Qual classificação?
Quem classificou?
Qual tabela?
Qual teto?
Qual regra?
Qual cálculo?
Qual resultado?
```

------------------------------------------------------------------------

# 35. Exportações

Saídas planejadas:

-   JSON completo;
-   JSON RAW;
-   CSV normalizado;
-   CSV da apuração;
-   validações;
-   tabelas;
-   demonstração.

Excel é ferramenta de conferência/exportação.

Não deve ser requisito para executar o cálculo.

------------------------------------------------------------------------

# 36. Exceções

O sistema deve sinalizar:

``` text
CLASSIFICAÇÃO PENDENTE
TETO NÃO CADASTRADO
COMPETÊNCIA SEM TABELA
DADOS INSUFICIENTES
SITUAÇÃO PARA ANÁLISE
```

Não deve simplesmente ignorar a competência.

------------------------------------------------------------------------

# 37. Testes prioritários

## Tabelas

-   primeira faixa;
-   limites;
-   teto;
-   mudanças anuais;
-   2020;
-   2023;
-   2024;
-   2025;
-   2026. 

## Grupos

-   11%;
-   20%;
-   progressiva;
-   combinações.

## Vínculos

-   um;
-   dois;
-   N.  

## Competências

-   mensal;
-   dezembro;
-   13º;
-   transição.

## Resultados

-   abaixo do teto;
-   exatamente no teto;
-   acima do teto;
-   progressiva acima do teto;
-   20% sem saldo;
-   classificação pendente.

------------------------------------------------------------------------

# 38. Regras de desenvolvimento

Não alterar o motor de extração para corrigir uma regra de cálculo.

Não apagar dados do RAW.

Não usar a alíquota efetiva observada como classificação jurídica
automática.

Não calcular cada fonte isoladamente quando a regra exigir consolidação.

Não misturar 13º com dezembro para aplicação das faixas.

Não esconder declarantes utilizados.

Não produzir resultado sem memória suficiente para auditoria.

------------------------------------------------------------------------

# 39. Fluxo final desejado

O usuário deverá fazer:

``` text
1. Enviar DIRF
2. Conferir fontes excepcionais
3. Confirmar classificações necessárias
4. Definir período
5. Selecionar declarantes
6. Conferir Verificação
7. Executar Apuração
8. Conferir Demonstração
9. Exportar
```

O sistema deverá fazer automaticamente a maior parte do trabalho
intermediário.

------------------------------------------------------------------------

# 40. Estado atual

Na V1.2.10, já existem:

``` text
EXTRAÇÃO
RAW
FILTROS
IDENTIFICAÇÃO
AGRUPAMENTO
CLASSIFICAÇÃO AUTOMÁTICA
EDIÇÃO DA CLASSIFICAÇÃO
TABELAS HISTÓRICAS
VERIFICAÇÃO
13º NA VERIFICAÇÃO
TOLERÂNCIA
DETALHAMENTO
APURAÇÃO
PERÍODO NA APURAÇÃO
SELEÇÃO DE DECLARANTES
CONSOLIDAÇÃO INICIAL
DEMONSTRAÇÃO
EXPORTAÇÃO
```

As partes que ainda precisam de validação mais profunda são
principalmente:

``` text
PROGRESSIVIDADE
MÚLTIPLOS VÍNCULOS
11% + 20% + PROGRESSIVA
13º CONSOLIDADO
EXCESSO DEFINITIVO
DEMONSTRAÇÃO FINAL
MEMÓRIA DE CÁLCULO
AUDITORIA
```

------------------------------------------------------------------------

# 41. Regra para a próxima versão

Antes de alterar novamente o motor:

1.  testar a Apuração com janeiro/2025;
2.  testar julho/2025;
3.  comparar com a planilha;
4.  testar mais de dois vínculos;
5.  verificar o 13º;
6.  registrar divergências;
7.  somente então implementar novas regras.

------------------------------------------------------------------------

# 42. Objetivo final

> O sistema deverá permitir que o usuário envie a DIRF, defina o período
> e os declarantes que participarão da análise e, após apenas as
> confirmações realmente necessárias, obtenha uma demonstração auditável
> de quanto foi efetivamente informado, quanto poderia ser considerado
> segundo as regras previdenciárias aplicáveis a cada competência e qual
> foi o valor total eventualmente pago acima do limite previdenciário.

------------------------------------------------------------------------

# 43. Documento de referência

Este manual deve evoluir junto com o roadmap.

Toda alteração relevante de:

-   regra;
-   interface;
-   classificação;
-   cálculo;
-   tabela;
-   apuração;
-   exportação;

deve ser registrada na documentação da respectiva versão.
