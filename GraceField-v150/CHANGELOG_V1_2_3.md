# CHANGELOG — V1.2.3

## Verificação anual por fonte

- A guia de verificação deixou de operar apenas por competência isolada.
- O usuário seleciona primeiro o **ano-calendário** e uma **fonte/vínculo selecionado**.
- O sistema carrega automaticamente as competências mensais encontradas para aquela fonte no ano.
- Cada competência continua sendo calculada individualmente, com sua própria tabela e metodologia.
- O resumo anual mostra remuneração, Previdência DIRF, contribuição calculada, diferença e contagem de status.
- Cada competência pode ser expandida para auditoria das faixas, bases e contribuições.
- O modo continua independente do motor principal.
- A seleção de fontes da guia respeita o agrupamento: somente fontes incluídas em 🔗 Agrupamento aparecem para verificação.

## Regressão

- Smoke tests executados com sucesso.
- Base histórica 2017–2026 preservada.
- Motor 11%/20% preservado.
- Progressiva continua em validação antes da integração definitiva ao motor.
