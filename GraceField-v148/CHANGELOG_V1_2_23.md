# V1.2.23 — UX judicial e relatório técnico

## Mantido
- Motor previdenciário e metodologia atual.
- Deduplicação documental conservadora.
- Seleção de 13º por ano civil.
- Persistência em `.TETOPREV`.
- Classificação por CNPJ existente.
- CNIS, GERID e eSocial permanecem fora da implementação.

## Novidades
- Identidade visual mais sóbria e técnica no Streamlit.
- Cabeçalho visual de sistema de análise judicial.
- Modal de confirmação ao carregar trabalho `.TETOPREV`, mostrando processo e autor disponíveis.
- Processo não é mais inferido pelo nome do arquivo; somente dados efetivamente disponíveis no RAW/TETOPREV podem preencher o campo automaticamente.
- PDF de Relatório da Análise na aba Exportação.
- Relatório estruturado em tabelas, com identificação dos autos, declarantes utilizados, páginas, período, 13º incluídos, resultado consolidado e demonstração horizontal.
- Demonstração horizontal do relatório em página paisagem.
- Valores monetários no PDF em padrão brasileiro `1.234,56`, com `R$` somente nos quadros-resumo.
- Demonstração horizontal da interface acompanha o escopo mensal da apuração quando disponível.
