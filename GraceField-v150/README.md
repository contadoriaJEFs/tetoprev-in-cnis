# Extrator DIRF + Motor Previdenciário — V1.2.21

## GraceField-v121

V1.2.21 mantém o motor da V1.2.20 e acrescenta persistência do trabalho em arquivo `.TETOPREV`. O arquivo é JSON internamente, apenas utiliza a extensão própria para permitir que o usuário carregue novamente a ficha processada.

### Novidades
- Entrada com identificação dos autos: nº do processo, autor, réu e ID do documento analisado.
- Processo e autor são preenchidos automaticamente quando já constam da DIRF.
- Relatório documental recolhível organizado por página.
- Auditoria recolhível das duplicidades documentais, com páginas e comparação das competências/valores.
- Exportação do JSON completo + motor como `.TETOPREV`.
- Nome do arquivo: quatro primeiros nomes do autor, separados por `_`, seguidos de `HHMMSSmm.TETOPREV`.
- Carregamento posterior do `.TETOPREV`, restaurando dados, classificações, vínculos e seleções salvas.
- Seleção de 13º por ano permanece explícita e é persistida no arquivo.

### Regra de preservação
O conteúdo do `.TETOPREV` continua sendo JSON. O RAW permanece completo e a deduplicação não apaga registros.

### Execução
```bash
pip install -r requirements.txt
streamlit run app.py
```

## V1.2.30
- UX judicial sóbria no Streamlit.
- Modal de confirmação ao carregar `.TETOPREV`.
- Relatório técnico em PDF com tabelas e demonstração horizontal em paisagem.
- Formatação monetária brasileira.
- Sem implementação de CNIS/GERID/eSocial.
