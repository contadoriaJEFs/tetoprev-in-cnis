# GraceField V1.2.39

## Identificação única do caso nos arquivos exportados

- Criado identificador de caso alfanumérico de 8 caracteres, gerado uma vez por caso.
- O identificador é persistido no `.tetoprev` em `caso.id_caso`.
- Ao carregar um `.tetoprev` que já possui `id_caso`, o mesmo identificador é restaurado.
- Arquivos relacionados ao caso passam a utilizar o mesmo código.
- PDF: `Nome_da_Parte_XXXXXXXX.pdf`.
- Excel de conferência: `Nome_da_Parte_XXXXXXXX_conferencia.xlsx`.
- Excel Competência + Acima do teto: `Nome_da_Parte_XXXXXXXX_competencia_acima_teto.xlsx`.
- Arquivo de caso: `Nome_da_Parte_XXXXXXXX.tetoprev`.
- Extensão `.tetoprev` passou a ser minúscula no nome baixado.
- O código não contém dados pessoais e não depende do nome da parte.

## Preservação funcional

- Nenhuma regra do motor previdenciário foi alterada nesta versão.
- Os testes de regressão existentes permanecem passando, inclusive o teste V1.2.35 referente ao caso da planilha.
