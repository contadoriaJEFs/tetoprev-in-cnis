# V1.2.33

## Correção do OCR em ambiente Streamlit

- Mantida integralmente a base da V1.2.32.
- Corrigida a integração do OCR para que a ausência do Tesseract não interrompa a leitura dos demais PDFs/páginas.
- Diagnóstico explícito da disponibilidade do Tesseract.
- Falhas de OCR ficam registradas por página para conferência.
- `packages.txt` mantido dentro da aplicação e também na raiz do pacote, pois o Streamlit Community Cloud pode exigir o arquivo de pacotes do sistema na raiz do repositório quando o `app.py` está em subdiretório.
- Dependências do sistema: `tesseract-ocr` e `tesseract-ocr-por`.
- Nenhuma alteração no motor previdenciário, classificação, apuração ou regras de cálculo.
