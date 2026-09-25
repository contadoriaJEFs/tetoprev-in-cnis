# V1.2.22

## Correção — restauração do número do processo

- Corrigida a restauração da identificação dos autos ao carregar `.TETOPREV`.
- O processo gravado no bloco `caso` tem prioridade.
- Se o campo estiver vazio, o sistema procura o número CNJ nos registros e também no nome do arquivo PDF de origem.
- Exemplo suportado: `0031059-48.2026.4.05.8300_DIRF.pdf` → `0031059-48.2026.4.05.8300`.
- Ao carregar TETOPREV, os campos de identificação são restaurados explicitamente, evitando que valores antigos da sessão impeçam o preenchimento.
- Não foram implementadas regras de CNIS, GERID ou eSocial.
- Motor previdenciário e regras de apuração permanecem inalterados.
