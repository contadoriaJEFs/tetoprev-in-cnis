# Changelog — V1.2.18

## Inclusão explícita do 13º por ano civil na Apuração

Alteração pontual sobre o último modelo V1.2.17.

### Regra

O 13º deixa de entrar automaticamente na Apuração apenas por existir dentro do histórico ou por o respectivo ano estar dentro do período mensal selecionado.

A Apuração passa a apresentar uma seleção por ano civil:

- `☐ Incluir 13º/2021`
- `☐ Incluir 13º/2022`
- `☐ Incluir 13º/2023`
- etc.

Somente os anos marcados pelo usuário são acrescentados à Apuração.

### Exemplos

Período `01/2025 a 12/2025`:

- `13º/2025` aparece para seleção;
- permanece desmarcado por padrão;
- se não for marcado, não participa da Apuração.

Período `01/2021 a 12/2025`:

- o sistema apresenta os 13º disponíveis de 2021 a 2025;
- cada ano pode ser incluído ou excluído independentemente.

Isso permite, por exemplo, incluir 2021, 2022 e 2023, mas deixar 2024 e 2025 fora.

### Preservações

Não foram alterados nesta versão:

- motor de extração;
- RAW;
- classificação previdenciária;
- hierarquia Progressiva → 11% → 20%;
- motor de apuração mensal;
- regra de consolidação dos vínculos;
- tratamento de remuneração zero com Previdência DIRF positiva;
- guia de Verificação;
- Demonstração horizontal.

O 13º continua sendo competência própria, separada de dezembro.
