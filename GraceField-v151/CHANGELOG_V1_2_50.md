# V1.2.50 — Classificação CNIS aplicada efetivamente ao motor

## Correção da classificação automática

- A classificação derivada do CNIS passa a ser efetivamente aplicada ao `assignments`, que alimenta o motor previdenciário.
- `Contribuinte Individual` não cooperado → **11%**.
- `Contribuinte Individual` cooperado → **20%**.
- `Empregado / Agente Público` → **Progressiva**.
- Evidência automática/legada armazenada em `.tetoprev` não confirmada explicitamente pelo usuário é recalculada quando o CNIS atual fornece classificação objetiva.
- O valor da alíquota efetiva observada na DIRF continua sendo apenas evidência auxiliar.

## Confirmação manual

- Alterar o `selectbox` não altera mais a classificação efetivamente utilizada.
- A decisão manual somente é persistida após o clique em **CONFIRMAR CLASSIFICAÇÃO**.
- Foi criada a marca `confirmacao_manual_explicita` para diferenciar decisão do usuário de classificação automática.
- Classificações automáticas não são mais transformadas em decisões manuais por mera alteração/reexecução da interface.

## Interface

- A classificação final exibida acompanha a classificação efetivamente aplicada ao motor.
- Alteração ainda não confirmada é mostrada como **Alteração pendente**.
- A chave do widget incorpora a classificação automática/origem para impedir que um estado visual antigo, como `Progressiva`, seja reaproveitado quando o CNIS determinar `11%` ou `20%`.

## Integridade

- O motor previdenciário e as tabelas históricas não foram alterados.
- Corrige especificamente a divergência em que a tela mostrava `11% — Contribuinte Individual`, mas a classificação final permanecia `Progressiva`.
