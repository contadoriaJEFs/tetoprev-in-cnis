# V1.2.32 — leitura robusta de DIRF em imagem e identificação no carregamento

- Preserva o motor previdenciário e o extrator nativo existente.
- Adiciona fallback OCR por página quando uma página parece ser imagem/scan e a leitura nativa não reconhece a DIRF.
- Registra `metodo_leitura` (`texto_nativo` ou `ocr`) e `conferencia_necessaria` no RAW.
- Exibe alerta explícito com arquivo e número das páginas processadas por OCR.
- Exibe alerta separado quando o OCR não consegue extrair uma página.
- Adiciona diagnóstico por arquivo: páginas totais, texto nativo, DIRF nativa, DIRF imagem/OCR e falhas.
- Adiciona modal após o carregamento de PDF com processo, parte/autor, arquivo(s), declarações e anos identificados.
- A identificação processual é obtida do próprio PDF quando houver página PJe; não é inventada.
- Mantém `extract_pdf()` compatível com a assinatura anterior; o novo diagnóstico usa `extract_pdf_with_diagnostics()`.
