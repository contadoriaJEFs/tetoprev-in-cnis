# V1.2.21

## Arquivo de trabalho TETOPREV + identificação judicial

- Mantido o motor previdenciário da V1.2.20.
- Exportação do JSON completo + motor passa a usar extensão `.TETOPREV`.
- O conteúdo do arquivo continua sendo JSON.
- Nome automático do arquivo: quatro primeiros nomes do autor, separados por `_`, seguidos de `HHMMSSmm.TETOPREV`.
- Novo carregador de `.TETOPREV`/JSON para retomar um trabalho sem reenviar a DIRF.
- O carregamento restaura classificação por CNPJ, vínculos incluídos, seleção de 13º e identificação dos autos gravada no arquivo.
- Entrada judicial com nº do processo, nome do autor, nome do réu e ID do documento analisado.
- Nº do processo e nome do autor são preenchidos automaticamente quando encontrados no RAW da DIRF.
- O réu permanece editável/manual, pois não é um campo confiável da DIRF extraída.
- Relatório documental recolhível, organizado por página, com identificação da declaração, CNPJ, declarante, ano, código, tipo, situação, data de entrega, processo e demais dados disponíveis.
- Auditoria recolhível das duplicidades documentais, com páginas e comparação de competências, remunerações e Previdência.
- Nenhuma regra nova de CNIS, GERID, eSocial ou matriz previdenciária foi implementada nesta versão.
