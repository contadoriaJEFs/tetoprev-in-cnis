# V1.2.9 — Apuração por competência

## Apuração
- Consolidação automática de N vínculos por competência.
- Tratamento conjunto dos grupos `progressiva`, `11` e `20`.
- Ordem de ocupação do teto: Progressiva → 11% → 20%, conforme a lógica prática da planilha-base usada nesta etapa.
- Cálculo de contribuição máxima e valor acima do teto.
- Preservação da contribuição efetivamente informada na DIRF.
- 13º tratado separadamente de dezembro.
- Detalhamento das fontes, bases, grupos e faixas progressivas.

## Verificação
- A classificação final da fonte passa a alimentar a coluna **Previdência Calculada**.
- A consolidação entre vínculos não é feita na Verificação; ela permanece exclusiva da Apuração.

## Validação
- Janeiro/2025: máximo total R$ 1.081,45 e excesso R$ 9,21 no caso prático de dois vínculos.
- Julho/2025: progressiva consome o teto; máximo 20% = R$ 0,00 e excesso R$ 718,77.
- Testes smoke e testes específicos de apuração/classificação concluídos.
