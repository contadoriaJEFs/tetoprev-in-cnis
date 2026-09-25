# CHANGELOG — V1.2.4

## Interface brasileira
- Competências exibidas na interface no padrão `MM/AAAA` (ex.: `01/2020`).
- Datas completas exibidas no padrão `DD/MM/AAAA` quando apresentadas.
- Vigências históricas exibidas em padrão brasileiro.
- Valores e percentuais permanecem em padrão brasileiro na apresentação.

## Verificação da progressiva
- Mantida a navegação por ano-calendário + fonte/vínculo.
- Adicionada tolerância padrão do sistema de R$ 0,01.
- Adicionada opção de tolerância personalizada informada pelo usuário.
- O resultado registra a origem da tolerância: `SISTEMA — PADRÃO` ou `USUÁRIO`.
- A comparação utiliza a diferença interna antes do arredondamento visual.
- A diferença apresentada continua com duas casas; a auditoria pode exibir a diferença interna com quatro casas.
- A tolerância altera somente o status de compatibilidade; não altera o cálculo previdenciário.

## Auditoria
- Os resultados da verificação passam a carregar `tolerancia_utilizada`, `tolerancia_origem` e `diferenca_bruta`.

## Testes
- Smoke tests executados após as alterações.
