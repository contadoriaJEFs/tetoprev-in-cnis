# V1.2.48 — Classificação objetiva com base no CNIS

## CNIS → classificação

- O CNIS passa a ser fonte efetiva da classificação quando identifica o tipo de filiado do vínculo.
- **Contribuinte Individual → 11%**.
- **Contribuinte Individual Cooperado → 20%**.
- **Empregado ou Agente Público → Progressiva**.
- A informação de **Cooperado / Não Cooperado** é extraída das linhas de prestação de serviço do CNIS e associada ao CNPJ.
- Em caso de evidência conflitante de Cooperado e Não Cooperado para o mesmo CNPJ, a classificação automática fica pendente de análise.
- A alíquota efetiva observada na DIRF permanece como evidência auxiliar e não substitui a identificação documental do CNIS.
- A fonte da classificação passa a ser registrada como **CNIS**, separadamente da origem de eventual confirmação manual.
- Classificações automáticas/legadas não confirmadas pelo usuário são recalculadas quando um CNIS novo fornece evidência objetiva; uma classificação explicitamente confirmada pelo usuário continua prevalecendo.
- A tela de classificação passa a exibir a natureza identificada, a classificação derivada e a fonte documental.
- O modal de evidência CNIS passa a mostrar também a condição de prestação quando disponível.

## Integridade

- Motor previdenciário e regras de apuração não foram alterados.
- Testes de regressão existentes mantidos.
