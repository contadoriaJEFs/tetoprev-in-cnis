# CHANGELOG V1.2.13

## Correção — agrupamento da Demonstração horizontal

- O agrupamento horizontal passa a utilizar o CNPJ em forma canônica, eliminando diferenças de pontuação/formatação entre páginas da mesma DIRF.
- Ocorrências do mesmo CNPJ em páginas/blocos distintos são consolidadas nas mesmas duas colunas: **Remuneração** e **Previdência**.
- Quando uma página/bloco vier sem CNPJ, o sistema tenta recuperar o CNPJ somente quando o nome do declarante apontar inequivocamente para um único CNPJ já identificado no arquivo.
- Nunca são mesclados CNPJs diferentes apenas por coincidência de nome.
- A soma por competência continua preservando todos os lançamentos encontrados no RAW.

## Testes

- `py_compile` dos módulos principais: OK.
- testes smoke existentes: OK.
