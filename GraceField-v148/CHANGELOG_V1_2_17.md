# CHANGELOG V1.2.17

## Correção — Verificação deve respeitar a classificação persistente do vínculo

### Problema
Ao selecionar na guia **Verificação** um declarante/CNPJ que já havia sido definido como **11%**, a consolidação interna por competência removia a coluna de classificação. Como consequência, a linha podia cair em `nao_definido` e a função de verificação padrão aplicava indevidamente a **tabela progressiva**.

### Correção
A Verificação agora recupera explicitamente a classificação persistente do CNPJ selecionado em `st.session_state.assignments` antes de consolidar as ocorrências da DIRF.

A classificação é preservada durante o agrupamento por:
- competência;
- ano;
- tipo de competência;
- blocos e páginas diferentes da DIRF.

### Regra
```text
CNPJ selecionado
      ↓
classificação definida para o CNPJ
      ↓
11% / 20% / Progressiva
      ↓
Verificação utiliza o mesmo tipo
      ↓
Apuração e Demonstração utilizam o mesmo vínculo/classificação
```

### 13º
O 13º continua separado de dezembro, mas, quando o vínculo possui classificação definida, a Verificação passa a utilizar essa classificação também no cálculo individual de referência, mantendo o status de **análise conjunta**.

### Importante
A correção não altera a tela de Apuração nem sua hierarquia de cálculo:

```text
Progressiva → 11% → 20%
```

Ela apenas garante que a fonte chegue às etapas seguintes com a classificação que já foi definida para seu CNPJ.
