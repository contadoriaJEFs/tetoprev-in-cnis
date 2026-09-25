# Changelog — V1.2.5

## Verificação histórica
- Substituída a navegação obrigatória por um único ano por três modos:
  - Todos os anos disponíveis;
  - Intervalo de anos;
  - Um ano.
- A escolha do período serve para navegação/consolidação; o cálculo continua competência a competência.
- Ao selecionar uma fonte, o sistema carrega automaticamente o histórico mensal encontrado dentro do período.
- Registros da mesma fonte e competência são consolidados antes da verificação para evitar duplicidade quando houver mais de um registro/código no mesmo mês.

## Usabilidade
- Mantido o padrão brasileiro de competência `MM/AAAA`.
- Adicionado botão explícito **📋 COPIAR PARA EXCEL** para a tabela consolidada da Verificação, com cabeçalho e valores.
- Mantido o detalhamento expansível por competência, inicialmente recolhido.
- Mantidos CSV e demais mecanismos de exportação.

## Tolerância
- Mantida tolerância padrão de R$ 0,01.
- Mantida tolerância personalizada pelo usuário, com identificação da origem do critério.
- A comparação continua usando a diferença interna antes do arredondamento visual.

## Preservação da lógica
- Não houve alteração da lógica principal de apuração 11%/20%.
- A metodologia progressiva continua na bancada de verificação e não foi incorporada silenciosamente ao motor principal.
