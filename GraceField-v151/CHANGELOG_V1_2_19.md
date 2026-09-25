# Changelog — V1.2.19

## Correção da filtragem cronológica da Apuração

A V1.2.18 introduziu a seleção explícita de 13º por ano, mas a filtragem do escopo da Apuração ainda utilizava uma tupla `(ano, mês)` como chave cronológica. Em algumas DIRFs, o pandas podia falhar nessa comparação e gerar `ValueError` durante o filtro do período.

### Correção

A chave cronológica agora é escalar e numérica:

- `AAAA01` a `AAAA12` para competências mensais;
- `AAAA13` para o 13º.

Exemplo:

```text
202501
202502
...
202512
202513  ← 13º
```

Isso mantém o 13º imediatamente após dezembro e elimina a comparação de Series com tuplas.

### O que permanece inalterado

- extração RAW;
- agrupamento de vínculos;
- classificação;
- verificação;
- motor previdenciário;
- hierarquia Progressiva → 11% → 20%;
- regra de remuneração zero com previdência positiva;
- seleção explícita de declarantes;
- seleção do 13º por ano civil.

A alteração desta versão é exclusivamente a correção da chave de ordenação/filtro da Apuração.
