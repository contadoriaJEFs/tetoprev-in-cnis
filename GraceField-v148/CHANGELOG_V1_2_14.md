# CHANGELOG V1.2.14

## Correção — identidade contínua do mesmo vínculo/CNPJ

Foi reforçada a identidade do vínculo na Demonstração horizontal e nas etapas que dependem da identidade do declarante.

### Regra

O mesmo declarante deve permanecer no mesmo vínculo/coluna durante todo o histórico quando possuir o mesmo CNPJ, mesmo que a DIRF esteja dividida em blocos e o declarante:

- apareça em páginas muito distantes;
- deixe de apresentar remuneração por várias competências;
- volte a aparecer posteriormente;
- apareça em blocos diferentes dentro do mesmo arquivo;
- tenha diferenças de máscara/formatação no CNPJ.

### Identidade

Foi criada uma chave interna `cnpj_chave`, formada pelos 14 dígitos do CNPJ, sem pontuação. A demonstração horizontal utiliza essa identidade para consolidar as ocorrências.

Quando uma ocorrência não possuir CNPJ válido, permanece o fallback pelo nome normalizado apenas quando não houver ambiguidade.

### Efeito esperado

Exemplo:

```text
04/2021 a 02/2023
SECRETARIA DE SAÚDE — CNPJ X

03/2023 a 12/2023
SECRETARIA DE SAÚDE — CNPJ X
```

Deve resultar em **uma única coluna** para o vínculo, com todas as remunerações e contribuições somadas por competência.

A existência de competências com remuneração R$ 0,00 não encerra o vínculo.

### Caso de teste de regressão

Um vínculo 11% que possui recolhimentos sem remuneração entre blocos intermediários e volta a apresentar remuneração posteriormente deve continuar sendo tratado como o mesmo vínculo até a última competência efetivamente existente.

Não deve ser criada uma nova coluna para o mesmo CNPJ.
