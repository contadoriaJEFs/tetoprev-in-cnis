# V1.2.44 — Integridade e compatibilidade do TETOPREV

## Correções

- Implementada serialização segura do `.tetoprev` com JSON padrão (`allow_nan=False`).
- Valores `NaN`, `Infinity` e `-Infinity` são convertidos para `null` antes da gravação.
- Tipos pandas/NumPy e datas são normalizados para tipos JSON compatíveis.
- O conteúdo do `.tetoprev` é reaberto com `json.loads()` antes de ser disponibilizado para download, evitando entregar arquivo JSON incompleto/inválido gerado pelo sistema.
- Exportação do JSON RAW também utiliza a serialização segura.
- O carregador mantém compatibilidade com arquivos antigos que contenham `NaN`/`Infinity`, convertendo esses valores para `null` em memória.
- Erros de JSON truncado passam a apresentar mensagem específica indicando arquivo incompleto no final, em vez de uma mensagem genérica.

## Preservado

- Schema `extrator_dirf.tetoprev.v1`.
- Compatibilidade estrutural com `.tetoprev` anteriores que estejam íntegros.
- Configuração de competências inativadas da V1.2.43.
- Motor previdenciário e regras de cálculo sem alteração.
