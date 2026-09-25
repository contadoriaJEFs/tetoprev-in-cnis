"""Deduplicação conservadora de blocos DIRF repetidos no mesmo arquivo.

A extração RAW não é alterada nem apagada. O módulo apenas identifica blocos
que representam a mesma declaração repetida no PDF e marca as ocorrências.
A primeira ocorrência (menor página) é considerada canônica; as seguintes
são marcadas como duplicatas documentais.
"""

import hashlib
import json
import re
from collections import defaultdict

import pandas as pd


COLUNAS_NUMERICAS = [
    "rendimento_tributavel",
    "irrf",
    "previdencia_oficial",
    "dependentes",
    "pensao_alimenticia",
    "desconto_simplificado",
    "previdencia_complementar",
    "compensacao_judicial_ano_calendario",
    "compensacao_judicial_anos_anteriores",
]

COLUNAS_IDENTIDADE = [
    "arquivo_origem",
    "cpf_beneficiario",
    "cnpj_declarante",
    "nome_declarante_dirf",
    "nome_declarante_cadastro",
    "nome_beneficiario_dirf",
    "nome_beneficiario_cadastro",
    "ano_calendario",
    "data_entrega",
    "tipo_declaracao",
    "situacao_declaracao",
    "situacao_especial",
    "total_codigos_receita",
    "codigo_receita",
    "descricao_codigo_receita",
    "classificacao_codigo",
    "fundo_clube",
    "numero_processo",
]


def _norm_text(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip().upper()


def _norm_num(value):
    try:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return 0.0
        return round(float(value), 2)
    except Exception:
        return _norm_text(value)


def _valor(row, coluna):
    if coluna in COLUNAS_NUMERICAS:
        return _norm_num(row.get(coluna))
    return _norm_text(row.get(coluna))


def _assinatura_bloco(grupo):
    """Gera assinatura do conteúdo integral de uma declaração/bloco.

    A página PDF não entra na assinatura. Assim, a mesma declaração copiada
    para outra página do mesmo arquivo produz a mesma assinatura. Competência,
    tipo de competência e todos os valores extraídos entram no fingerprint.
    """
    g = grupo.copy()
    g = g.sort_values(
        [c for c in ["tipo_competencia", "competencia", "competencia_nome"] if c in g.columns],
        kind="stable",
    )

    meta = {}
    row_cols = ["competencia", "competencia_nome", "tipo_competencia"] + COLUNAS_NUMERICAS
    for col in COLUNAS_IDENTIDADE:
        if col in g.columns:
            meta[col] = _norm_text(g.iloc[0].get(col))

    linhas = []
    for _, row in g.iterrows():
        linhas.append({col: _valor(row, col) for col in row_cols if col in g.columns})

    payload = {"meta": meta, "linhas": linhas}
    bruto = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(bruto.encode("utf-8")).hexdigest()


def marcar_duplicatas_documentais(df):
    """Marca blocos DIRF repetidos sem remover dados do RAW.

    Retorna:
      - dataframe com metadados de deduplicação;
      - estatísticas para a interface/auditoria.

    Regra: somente blocos com conteúdo integralmente equivalente são tratados
    como duplicados. A ocorrência de menor página é preservada como canônica.
    """
    if df is None or df.empty:
        out = df.copy() if df is not None else pd.DataFrame()
        for col, default in [
            ("bloco_id", ""),
            ("assinatura_documental", ""),
            ("ocorrencia_documental", 1),
            ("duplicata_documental", False),
            ("status_documental", "CANONICO"),
            ("pagina_canonica", None),
            ("duplicata_de_pagina", None),
        ]:
            if col not in out.columns:
                out[col] = default
        return out, {
            "blocos_identificados": 0,
            "blocos_unicos": 0,
            "blocos_duplicados": 0,
            "registros_duplicados": 0,
        }

    out = df.copy()
    if "arquivo_origem" not in out.columns:
        out["arquivo_origem"] = ""
    if "pagina_pdf" not in out.columns:
        out["pagina_pdf"] = 0

    # Um bloco DIRF, na extração atual, corresponde a uma página que contém
    # "Dados do beneficiário". O identificador usa arquivo + página, nunca CNPJ.
    out["bloco_id"] = out.apply(
        lambda r: f"{r.get('arquivo_origem', '')}|pagina:{r.get('pagina_pdf', '')}",
        axis=1,
    )

    bloco_assinatura = {}
    for bloco_id, g in out.groupby("bloco_id", sort=False, dropna=False):
        bloco_assinatura[bloco_id] = _assinatura_bloco(g)
    out["assinatura_documental"] = out["bloco_id"].map(bloco_assinatura)

    # A assinatura já inclui arquivo_origem; portanto, uma mesma declaração
    # em dois PDFs distintos não é silenciosamente misturada.
    paginas_por_assinatura = defaultdict(list)
    for bloco_id, assinatura in bloco_assinatura.items():
        try:
            pagina = int(out.loc[out["bloco_id"].eq(bloco_id), "pagina_pdf"].iloc[0])
        except Exception:
            pagina = 0
        paginas_por_assinatura[assinatura].append((pagina, bloco_id))

    status_por_bloco = {}
    for assinatura, itens in paginas_por_assinatura.items():
        itens = sorted(itens, key=lambda x: (x[0], x[1]))
        pagina_canonica, bloco_canonico = itens[0]
        for ocorrencia, (pagina, bloco_id) in enumerate(itens, start=1):
            duplicada = ocorrencia > 1
            status_por_bloco[bloco_id] = {
                "ocorrencia": ocorrencia,
                "duplicada": duplicada,
                "pagina_canonica": pagina_canonica,
                "duplicata_de_pagina": pagina_canonica if duplicada else None,
            }

    out["ocorrencia_documental"] = out["bloco_id"].map(lambda x: status_por_bloco[x]["ocorrencia"])
    out["duplicata_documental"] = out["bloco_id"].map(lambda x: status_por_bloco[x]["duplicada"]).astype(bool)
    out["status_documental"] = out["duplicata_documental"].map(
        {False: "CANONICO", True: "DUPLICATA_DOCUMENTAL"}
    )
    out["pagina_canonica"] = out["bloco_id"].map(lambda x: status_por_bloco[x]["pagina_canonica"])
    out["duplicata_de_pagina"] = out["bloco_id"].map(lambda x: status_por_bloco[x]["duplicata_de_pagina"])

    total_blocos = len(bloco_assinatura)
    duplicados_blocos = sum(1 for x in status_por_bloco.values() if x["duplicada"])
    registros_dup = int(out["duplicata_documental"].sum())
    stats = {
        "blocos_identificados": total_blocos,
        "blocos_unicos": total_blocos - duplicados_blocos,
        "blocos_duplicados": duplicados_blocos,
        "registros_duplicados": registros_dup,
    }
    return out, stats
