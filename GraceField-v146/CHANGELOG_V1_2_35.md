# V1.2.35 — Ocupação do teto por enquadramento

## Alterações

- Mantido integralmente o motor de cálculo da V1.2.34.
- Mantida a correção da V1.2.34 para remuneração progressiva inferior ao teto.
- Na etapa **Apuração**, a lista de declarantes selecionados passa a exibir o **tratamento previdenciário efetivamente utilizado**:
  - Progressiva
  - 11%
  - 20%
  - Não definida
- O resumo por competência passa a demonstrar, após o teto, as remunerações separadas por enquadramento:
  - Rem. progressiva
  - Máx. progressiva
  - Rem. 11%
  - Máx. 11%
  - Rem. 20%
  - Saldo p/ 20%
  - Máx. 20%
  - Máx. total
  - Acima do teto
- O campo **Saldo p/ 20%** representa o limite de remuneração remanescente após Progressiva e 11%; não é um novo teto previdenciário.
- O motor passa a registrar separadamente o saldo após Progressiva, após 11% e após 20%, corrigindo a semântica do campo `saldo_teto_apos_11` sem alterar os resultados já validados.
- O detalhamento da competência também informa os saldos remanescentes.

## Validação

Todos os smoke tests anteriores foram executados com sucesso.

Foi acrescentado teste de regressão baseado no caso concreto da planilha:

- Teto 2025: R$ 8.157,41
- Progressiva: R$ 1.518,00
- Máximo progressivo: R$ 113,85
- 20%: remuneração R$ 9.800,88
- Saldo para 20%: R$ 6.639,41
- Máximo 20%: R$ 1.327,88
- Máximo total: R$ 1.441,73
- Recolhido: R$ 1.745,33
- Acima do teto: R$ 303,60

Resultado: aprovado.
