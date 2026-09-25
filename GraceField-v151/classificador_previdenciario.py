import math
import re
import pandas as pd

REGRA_VERSAO = '2.0'
REGRA_ID = 'CLASSIFICACAO_CNIS_DIRF_V2'


def _rates(df):
    x = df.copy()
    x['rendimento_tributavel'] = pd.to_numeric(x.get('rendimento_tributavel'), errors='coerce').fillna(0)
    x['previdencia_oficial'] = pd.to_numeric(x.get('previdencia_oficial'), errors='coerce').fillna(0)
    # Fontes com Previdência Oficial e remuneração zero não permitem inferir
    # alíquota pela razão contribuição/remuneração. Elas continuam sendo
    # preservadas para a apuração; como sua remuneração é zero, não precisam de
    # classificação para determinar o máximo da competência.
    x = x[x['tipo_competencia'].eq('mensal') & (x['previdencia_oficial'] >= 0)].copy()
    x['rendimento_tributavel'] = pd.to_numeric(x['rendimento_tributavel'], errors='coerce').fillna(0)
    x['previdencia_oficial'] = pd.to_numeric(x['previdencia_oficial'], errors='coerce').fillna(0)
    x = x[(x['rendimento_tributavel'] > 0) | (x['previdencia_oficial'] > 0)].copy()
    if x.empty:
        return []
    x['rate'] = x['previdencia_oficial'] / x['rendimento_tributavel']
    return x.loc[x['rate'].notna(), 'rate'].tolist()


def _near(r, target, tol):
    return abs(r - target) <= tol


def sugerir_classificacao(df_fonte, cnis_evidencias=None):
    """Sugere grupo previdenciário com regras conservadoras e auditáveis.

    A taxa observada é evidência auxiliar, nunca fundamento isolado para uma
    classificação jurídica. Sugestões fracas ficam como confirmação necessária.
    """
    sub = df_fonte.copy()
    cnis_evidencias = cnis_evidencias or []
    evidencias = []
    regra = REGRA_ID
    sugestao = 'nao_definido'
    confianca = 'baixa'

    # Prioridade 1: identificação documental do CNIS. A natureza do vínculo
    # prevalece sobre a inferência pela alíquota efetiva da DIRF. A DIRF
    # continua como evidência auxiliar/conferência.
    naturezas = sorted(set(str(e.get('tipo_filiado') or '').strip() for e in cnis_evidencias if e.get('tipo_filiado')))
    cooperacoes = sorted(set(str(e.get('cooperacao') or 'nao_identificado') for e in cnis_evidencias))
    if naturezas:
        naturezas_norm = set(naturezas)
        if len(naturezas_norm) == 1:
            natureza = next(iter(naturezas_norm))
            if natureza == 'Contribuinte Individual':
                if 'misto' in cooperacoes:
                    sugestao, confianca = 'nao_definido', 'media'
                    evidencias.append('CNIS identifica Contribuinte Individual, mas há evidência conflitante de Cooperado e Não Cooperado para o mesmo CNPJ; classificação automática suspensa.')
                elif 'cooperado' in cooperacoes:
                    sugestao, confianca = '20', 'alta'
                    evidencias.append('CNIS identifica Contribuinte Individual com prestação Cooperado; classificação objetiva: 20%.')
                else:
                    sugestao, confianca = '11', 'alta'
                    if 'nao_cooperado' in cooperacoes:
                        evidencias.append('CNIS identifica Contribuinte Individual Não Cooperado; classificação objetiva: 11%.')
                    else:
                        evidencias.append('CNIS identifica Contribuinte Individual; na ausência de marcação de cooperado, classificação objetiva: 11%.')
            elif natureza == 'Empregado ou Agente Público':
                sugestao, confianca = 'progressiva', 'alta'
                evidencias.append('CNIS identifica Empregado ou Agente Público; classificação objetiva: metodologia progressiva.')
            else:
                evidencias.append(f'CNIS identifica natureza de vínculo não mapeada automaticamente: {natureza}.')
        else:
            evidencias.append('CNIS apresentou mais de uma natureza de vínculo para o mesmo CNPJ; classificação automática não foi consolidada.')

    rates = _rates(sub)

    if not naturezas and rates:
        med = float(pd.Series(rates).median())
        min_r, max_r = min(rates), max(rates)
        n = len(rates)

        # Padrão estável de contribuição fixa de 20%.
        if n >= 2 and all(_near(r, 0.20, 0.0125) for r in rates):
            sugestao, confianca = '20', 'alta'
            evidencias.append(f'Padrão de alíquota observada estável próximo de 20% ({med*100:.2f}% mediana).')
        # Padrão estável de contribuição fixa de 11%.
        elif n >= 2 and all(_near(r, 0.11, 0.0125) for r in rates):
            sugestao, confianca = '11', 'alta'
            evidencias.append(f'Padrão de alíquota observada estável próximo de 11% ({med*100:.2f}% mediana).')
        else:
            # Evidência de progressividade: múltiplas taxas compatíveis com
            # faixas históricas e variação relevante entre competências.
            bandas = (0.075, 0.09, 0.12, 0.14)
            compat = [r for r in rates if any(_near(r, b, 0.006) for b in bandas)]
            variacao = max_r - min_r
            if len(set(round(r, 3) for r in compat)) >= 2 and variacao >= 0.015:
                sugestao, confianca = 'progressiva', 'alta'
                evidencias.append('Foram observadas taxas efetivas distintas compatíveis com faixas da metodologia progressiva.')
            elif med <= 0.145 and max_r - min_r >= 0.02:
                sugestao, confianca = 'progressiva', 'media'
                evidencias.append('Padrão observado é compatível com metodologia progressiva, mas não é conclusivo.')
            else:
                evidencias.append('Padrão de contribuição observado não permite distinguir com segurança 11%, 20% ou progressiva.')
    elif not naturezas:
        evidencias.append('Não há base mensal suficiente para inferência automática pela contribuição observada.')

    # Códigos DIRF são natureza de rendimento e não determinam, sozinhos,
    # o grupo previdenciário. Apenas registramos essa evidência contextual.
    codigos = set(sub.get('codigo_receita', pd.Series(dtype=str)).dropna().astype(str).str.strip())
    if codigos:
        evidencias.append('Código(s) DIRF registrado(s) como evidência contextual; não usado isoladamente para definir o grupo.')

    if sugestao == 'nao_definido' and not naturezas:
        confianca = 'baixa'

    return {
        'classificacao_sugerida': sugestao,
        'classificacao_final': sugestao if confianca == 'alta' else 'nao_definido',
        'origem_classificacao': 'automatico' if confianca == 'alta' else 'pendente',
        'nivel_confianca': confianca,
        'evidencias': evidencias,
        'regra_classificacao': regra,
        'versao_regra': REGRA_VERSAO,
        'fonte_classificacao': 'CNIS' if naturezas and sugestao != 'nao_definido' else ('DIRF / regra automática' if not naturezas else 'CNIS / análise necessária'),
        'natureza_cnis': ' / '.join(naturezas),
        'cooperacao_cnis': ' / '.join(cooperacoes),
    }


def _cnpj_chave(v):
    digits = re.sub(r'\D', '', str(v or ''))
    return digits if len(digits) == 14 else ''


def classificar_fontes(df, cnpjs, assignments=None, metadata=None, cnis_por_cnpj=None):
    assignments = assignments or {}
    metadata = metadata or {}
    cnis_por_cnpj = cnis_por_cnpj or {}
    assignments_canon = {_cnpj_chave(k): v for k, v in assignments.items() if _cnpj_chave(k)}
    metadata_canon = {_cnpj_chave(k): v for k, v in metadata.items() if _cnpj_chave(k)}
    result = {}
    for cnpj in cnpjs:
        chave = _cnpj_chave(cnpj)
        sub = df[df['cnpj_declarante'].astype(str).map(_cnpj_chave).eq(chave)]
        cnis_ev = cnis_por_cnpj.get(chave, [])
        sug = sugerir_classificacao(sub, cnis_ev)
        if chave in assignments_canon:
            final = assignments_canon[chave]
            old = metadata_canon.get(chave, {})
            # Uma classificação manual confirmada pelo usuário tem precedência.
            # Uma classificação automática/legada, porém, deve ser recalculada
            # quando uma evidência CNIS nova estiver disponível.
            manual_confirmada = bool(old.get('confirmacao_manual_explicita'))
            if manual_confirmada or not cnis_ev:
                sug.update({
                    'classificacao_final': final,
                    'origem_classificacao': 'usuario' if manual_confirmada else old.get('origem_classificacao', 'usuario'),
                    'nivel_confianca': 'confirmada' if manual_confirmada else old.get('nivel_confianca', 'confirmada'),
                    'data_classificacao': old.get('data_classificacao'),
                    'usuario_confirmador': old.get('usuario_confirmador'),
                    'confirmacao_manual_explicita': bool(old.get('confirmacao_manual_explicita')),
                })
        result[cnpj] = sug
    return result
