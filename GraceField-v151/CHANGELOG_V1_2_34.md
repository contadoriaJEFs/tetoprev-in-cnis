# V1.2.34

## Apuração normativa — IN RFB 2.110/2022
- Ajuste explícito da metodologia para vínculos concomitantes empregado/progressiva + contribuinte individual/20%.
- A remuneração global dos vínculos progressivos é a primeira base considerada e somente o saldo do teto é disponibilizado ao grupo de 20%.
- A contribuição máxima progressiva não é levada ao teto quando a remuneração global progressiva é inferior ao teto.
- Adicionada auditoria visual para detectar inconsistência entre remuneração progressiva, base e teto.
- Adicionada consulta normativa dentro da guia Apuração, com link para a fonte oficial da Receita Federal.
- Mantidos os valores de Previdência DIRF como dado documental, sem correção automática.

## Testes
- Regressão para remuneração progressiva de R$ 5.000,00 em 2025: base permanece R$ 5.000,00 e contribuição máxima R$ 509,60.
- Regressão para remuneração no teto de 2025: contribuição máxima R$ 951,64.
