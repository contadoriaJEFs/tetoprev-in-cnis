# V1.2.11 — Recolhimento com remuneração zero

## Correção

- A Apuração agora preserva e soma a **Previdência Oficial da DIRF** mesmo quando a fonte informa **R$ 0,00 de remuneração**.
- Uma fonte com remuneração zero e recolhimento positivo não consome o teto e não bloqueia a competência por classificação pendente, pois sua base máxima é R$ 0,00.
- O detalhamento da Apuração identifica explicitamente essas fontes.
- O RAW permanece inalterado.

## Caso de regressão

Abril/2021, conforme planilha de referência:

- COOMEB: remuneração R$ 23.290,64; Previdência R$ 620,62.
- Secretaria Estadual de Saúde: remuneração R$ 0,00; Previdência R$ 366,35.
- Total recolhido: R$ 986,97.
- Contribuição máxima: R$ 707,69.
- Acima do teto: R$ 279,28.

## Testes

- Smoke tests anteriores preservados.
- Novo teste de recolhimento sem remuneração: OK.
- Novo teste sem classificação da fonte de remuneração zero: OK.
