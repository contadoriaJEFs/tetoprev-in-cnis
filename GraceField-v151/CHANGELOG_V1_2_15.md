# Changelog V1.2.16

## Correções

### 1. Identidade persistente do vínculo
- A classificação previdenciária passa a ser resolvida pela chave canônica do CNPJ.
- Páginas, blocos separados, lacunas de remuneração e retornos posteriores do mesmo CNPJ não criam novo vínculo nem nova classificação.
- A Demonstração e a Apuração continuam consolidadas por CNPJ.

### 2. Máximo de 11% em conjunto com fonte progressiva
- Quando existe grupo 11% na competência, o cálculo passa a ocupar o teto primeiro pelo grupo 11%, depois 20% e, por fim, progressiva, alinhando-se ao modelo da planilha Daniel Moreira.
- Assim, a presença posterior de uma fonte progressiva não zera indevidamente o Máx. 11% quando o vínculo 11% continua ativo.
- Quando não existe grupo 11%, preserva-se a ordem progressiva → 20%, compatível com a planilha prática de 2025 usada no projeto.

### 3. Regressão
- Incluído teste para CNPJ 11% persistente em blocos separados e para o cenário de março/2023 com 11% + 20% + progressiva.
