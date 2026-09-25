# V1.2.46 — Camada CNIS × DIRF

- Adicionada entrada opcional de CNIS em PDF.
- Extração dos vínculos do CNIS com sequência, tipo de filiado, período, CNPJ de origem, CNPJs de contratantes/tomadores e indicadores.
- Cruzamento documental por CNPJ normalizado entre CNIS e DIRF.
- A guia Classificação passa a exibir a natureza identificada no CNIS e a fonte documental da evidência.
- Adicionado preview da evidência do CNIS em modal, com recorte da página relevante e identificação de vínculo/página.
- Evidências CNIS são persistidas na classificação e no `.tetoprev`.
- O PDF do CNIS é armazenado no `.tetoprev` em Base64 para permitir reabertura do caso e novo preview sem reenviar o documento.
- O CNIS não altera automaticamente a alíquota/metodologia 11%/20%/progressiva nesta versão; ele fornece identificação documental do vínculo para tornar a classificação mais objetiva e auditável.
- Mantido o motor previdenciário existente sem alteração das regras de apuração.
