# GraceField V1.2.36 — Performance

## Objetivo
Reduzir o tempo de espera provocado pelos reruns do Streamlit sem alterar a lógica previdenciária ou o motor de cálculo.

## Causa identificada
A cada interação da interface, o Streamlit reexecuta `app.py`. Antes da V1.2.36, quando havia PDF no `st.file_uploader`, o bloco de leitura chamava novamente `extract_pdf_with_diagnostics()` para cada PDF em **todo rerun**.

Em teste local com `Suzana Marine - DIRFs.pdf` (135 páginas / 1.414 registros), a extração levou aproximadamente **14–16 segundos por execução**. Isso explica a espera observada ao apenas desmarcar fontes ou alterar controles.

## Correção
A extração dos PDFs agora fica armazenada em `st.session_state['_dirf_extracao_cache']`, indexada pelo SHA-256 do conteúdo do PDF.

- Primeiro carregamento do PDF: extrai normalmente.
- Reruns posteriores com o mesmo conteúdo: reutilizam a extração.
- PDF novo ou conteúdo diferente: gera nova chave e é processado.
- `extract_document_identity()` também é reaproveitado junto com a extração.
- O RAW e os registros documentais não são modificados pela otimização.

## Integridade
Nenhuma regra do motor previdenciário foi alterada nesta versão.

A V1.2.35 permanece como referência funcional.
