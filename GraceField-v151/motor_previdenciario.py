from typing import Optional
import json
import re
import pandas as pd

from tabelas_previdenciarias import TABELAS_HISTORICAS, TETOS, tabela_por_competencia


def calcular_faixas(remuneracao: float, tabela: dict):
    """Calcula a contribuição conforme a metodologia da tabela histórica."""
    rem = max(float(remuneracao or 0), 0.0)
    teto = float(tabela['teto'])
    base = min(rem, teto)
    detalhes = []

    if tabela['metodologia'] == 'tradicional':
        faixa_escolhida = None
        for idx, (inferior, superior, aliquota) in enumerate(tabela['faixas'], start=1):
            if base <= superior:
                faixa_escolhida = (idx, inferior, superior, aliquota)
                break
        if faixa_escolhida is None:
            faixa_escolhida = (len(tabela['faixas']), *tabela['faixas'][-1])
        idx, inferior, superior, aliquota = faixa_escolhida
        contrib = base * aliquota
        for n, (inf, sup, aliq) in enumerate(tabela['faixas'], start=1):
            detalhes.append({
                'faixa': n,
                'limite_inferior': inf,
                'limite_superior': sup,
                'base_na_faixa': base if n == idx else 0.0,
                'aliquota': aliq,
                'contribuicao': contrib if n == idx else 0.0,
                'aplicada': n == idx,
            })
        return {'remuneracao': rem, 'base_limitada_ao_teto': base, 'contribuicao_calculada': contrib, 'faixas': detalhes}

    total = 0.0
    for idx, (inferior, superior, aliquota) in enumerate(tabela['faixas'], start=1):
        parcela = max(min(base, superior) - inferior, 0.0)
        contrib = parcela * aliquota
        detalhes.append({
            'faixa': idx,
            'limite_inferior': inferior,
            'limite_superior': superior,
            'base_na_faixa': parcela,
            'aliquota': aliquota,
            'contribuicao': contrib,
            'aplicada': parcela > 0,
        })
        total += contrib
        if base <= superior:
            break
    # Algumas tabelas oficiais/folhas utilizam a parcela a deduzir arredondada
    # para determinar o valor máximo no teto. A referência prática de 2025
    # utilizada neste projeto resulta em R$ 951,64 no teto de R$ 8.157,41.
    if base >= teto - 1e-9 and tabela.get('contribuicao_maxima_teto') is not None:
        total = float(tabela['contribuicao_maxima_teto'])
        for d in detalhes:
            if d['aplicada']:
                # Mantemos a memória das bases por faixa; o total oficial no teto
                # é controlado pelo valor máximo cadastrado na tabela.
                pass
    return {'remuneracao': rem, 'base_limitada_ao_teto': base, 'contribuicao_calculada': total, 'faixas': detalhes}


def _cnpj_chave(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return ''
    digits = re.sub(r'\D', '', str(v))
    return digits if len(digits) == 14 else ''


def classificar_declarante(df, assignments):
    out = df.copy()
    # A classificação pertence ao vínculo/CNPJ, não ao bloco, página ou
    # ocorrência individual da DIRF. Normalizamos tanto as chaves antigas
    # (com máscara) quanto uma eventual cnpj_chave já existente no dataframe.
    canon_assignments = {}
    for key, value in (assignments or {}).items():
        ck = _cnpj_chave(key)
        if ck:
            canon_assignments[ck] = value
    if 'cnpj_chave' in out.columns:
        keys = out['cnpj_chave'].astype(str)
    else:
        keys = out['cnpj_declarante'].map(_cnpj_chave)
    out['grupo_previdenciario'] = keys.map(canon_assignments).fillna('nao_definido')
    return out


def classify_declarante(df, assignments):
    return classificar_declarante(df, assignments)


def observed_rate(df):
    out = df.copy()
    base = out['rendimento_tributavel'].astype(float)
    out['aliquota_efetiva_observada'] = out['previdencia_oficial'].astype(float).div(base.where(base.ne(0)))
    return out['aliquota_efetiva_observada']


def verificar_tabela(competencia: str, remuneracao: float, previdencia_dirf: Optional[float] = None, tolerancia: float = 0.01):
    tabela = tabela_por_competencia(competencia)
    if tabela is None:
        return {'status': 'TABELA_NAO_CADASTRADA', 'competencia': competencia, 'remuneracao': float(remuneracao or 0)}
    calc = calcular_faixas(remuneracao, tabela)
    informado = None if previdencia_dirf in (None, '') else float(previdencia_dirf)
    diferenca_bruta = None if informado is None else float(informado - calc['contribuicao_calculada'])
    diferenca = None if diferenca_bruta is None else round(diferenca_bruta, 2)
    tolerancia = max(float(tolerancia or 0), 0.0)
    if informado is None:
        status = 'SEM_COMPARACAO'
    elif abs(diferenca_bruta) <= tolerancia:
        status = 'COMPATIVEL'
    else:
        status = 'DIFERENCA_PARA_ANALISE'
    return {
        'status': status,
        'competencia': competencia,
        'metodologia': tabela['metodologia'],
        'tabela_id': tabela['id'],
        'fonte': tabela['fonte'],
        'teto': tabela['teto'],
        'remuneracao': float(remuneracao or 0),
        'previdencia_dirf': informado,
        'contribuicao_calculada': round(calc['contribuicao_calculada'], 2),
        'diferenca_dirf_menos_calculado': diferenca,
        'diferenca_bruta': diferenca_bruta,
        'tolerancia_utilizada': tolerancia,
        'faixas': calc['faixas'],
    }


def verificar_por_grupo(competencia: str, remuneracao: float, grupo: str, previdencia_dirf: Optional[float] = None, tolerancia: float = 0.01, tipo_competencia: str = 'mensal'):
    """Verificação individual usando a classificação confirmada da fonte.

    Esta função altera somente a base da coluna "Previdência Calculada"; o valor
    "Previdência DIRF" continua sendo o valor extraído. A consolidação entre
    vínculos permanece exclusiva da guia Apuração.
    """
    tabela = tabela_por_competencia(competencia if tipo_competencia == 'mensal' else f'{str(competencia)[:4]}-12')
    if tabela is None:
        return {'status': 'TABELA_NAO_CADASTRADA', 'competencia': competencia, 'tipo_competencia': tipo_competencia, 'remuneracao': float(remuneracao or 0)}
    rem = max(float(remuneracao or 0), 0.0)
    grupo = str(grupo or 'nao_definido')
    if grupo == 'progressiva':
        calc = calcular_faixas(rem, tabela)
        metodologia = tabela['metodologia']
        faixas = calc['faixas']
    elif grupo in ('11', '20'):
        teto = float(tabela['teto'])
        base = min(rem, teto)
        aliq = 0.11 if grupo == '11' else 0.20
        calc = {'contribuicao_calculada': base * aliq, 'faixas': []}
        metodologia = f'fixa_{grupo}'
        faixas = []
    else:
        return verificar_tabela(competencia, rem, previdencia_dirf, tolerancia)

    informado = None if previdencia_dirf in (None, '') else float(previdencia_dirf)
    diferenca_bruta = None if informado is None else float(informado - calc['contribuicao_calculada'])
    tolerancia = max(float(tolerancia or 0), 0.0)
    if informado is None:
        status = 'SEM_COMPARACAO'
    elif abs(diferenca_bruta) <= tolerancia:
        status = 'COMPATIVEL'
    else:
        status = 'DIFERENCA_PARA_ANALISE'
    return {
        'status': status, 'competencia': competencia, 'tipo_competencia': tipo_competencia,
        'metodologia': metodologia, 'tabela_id': tabela['id'], 'fonte': tabela['fonte'],
        'teto': tabela['teto'], 'remuneracao': rem, 'previdencia_dirf': informado,
        'contribuicao_calculada': round(calc['contribuicao_calculada'], 2),
        'diferenca_dirf_menos_calculado': None if diferenca_bruta is None else round(diferenca_bruta, 2),
        'diferenca_bruta': diferenca_bruta, 'tolerancia_utilizada': tolerancia,
        'faixas': faixas, 'grupo_previdenciario': grupo,
        'observacao': 'Cálculo individual conforme a classificação da fonte. A consolidação entre vínculos é realizada exclusivamente na guia Apuração.'
    }


def verificar_13o(ano: int, remuneracao: float, previdencia_dirf: Optional[float] = None, tolerancia: float = 0.01):
    try:
        ano_i = int(ano)
    except Exception:
        return {'status': 'TABELA_NAO_CADASTRADA', 'competencia': f'{ano}-13', 'tipo_competencia': '13º', 'remuneracao': float(remuneracao or 0)}
    tabela = tabela_por_competencia(f'{ano_i:04d}-12')
    competencia = f'{ano_i:04d}-13'
    if tabela is None:
        return {'status': 'TABELA_NAO_CADASTRADA', 'competencia': competencia, 'tipo_competencia': '13º', 'remuneracao': float(remuneracao or 0)}
    calc = calcular_faixas(remuneracao, tabela)
    informado = None if previdencia_dirf in (None, '') else float(previdencia_dirf)
    diferenca_bruta = None if informado is None else float(informado - calc['contribuicao_calculada'])
    diferenca = None if diferenca_bruta is None else round(diferenca_bruta, 2)
    tolerancia = max(float(tolerancia or 0), 0.0)
    status = 'ANALISE_13O_CONJUNTA' if informado is not None else 'SEM_COMPARACAO'
    return {
        'status': status,
        'competencia': competencia,
        'tipo_competencia': '13º',
        'metodologia': tabela['metodologia'],
        'tabela_id': tabela['id'],
        'fonte': tabela['fonte'],
        'teto': tabela['teto'],
        'remuneracao': float(remuneracao or 0),
        'previdencia_dirf': informado,
        'contribuicao_calculada': round(calc['contribuicao_calculada'], 2),
        'diferenca_dirf_menos_calculado': diferenca,
        'diferenca_bruta': diferenca_bruta,
        'tolerancia_utilizada': tolerancia,
        'faixas': calc['faixas'],
        'observacao': '13º separado da remuneração mensal; para múltiplos vínculos, validar a apuração conjunta do 13º.'
    }


def _teto_da_competencia(competencia: str, tipo_competencia: str, tetos: dict):
    if tipo_competencia == '13º':
        try:
            ano = int(str(competencia)[:4])
            tabela = tabela_por_competencia(f'{ano:04d}-12')
            return None if tabela is None else float(tabela['teto'])
        except Exception:
            return None
    return tetos.get(competencia)


def calcular_contribuicao_progressiva_pelo_total(remuneracao_total, tabela):
    """Calcula o máximo do grupo progressivo sobre a remuneração global do grupo.

    Regra de apuração adotada para vínculos concomitantes de empregado e
    contribuinte individual: primeiro se considera a remuneração global dos
    vínculos de empregado (grupo progressivo), limitada ao teto; somente a
    parcela efetivamente ocupada por essa remuneração reduz o saldo disponível
    para os vínculos de 20%.
    """
    rem = max(float(remuneracao_total or 0), 0.0)
    teto = float(tabela['teto'])
    base = min(rem, teto)
    calc = calcular_faixas(base, tabela)
    return {
        'remuneracao_total': rem,
        'teto': teto,
        'base_considerada': base,
        'contribuicao_maxima': float(calc['contribuicao_calculada']),
        'faixas': calc['faixas'],
        'atingiu_teto': bool(rem >= teto - 1e-9),
    }


def _calcular_grupo(base, grupo, tabela, teto_restante):
    """Calcula o máximo de um grupo usando o saldo disponível do teto."""
    rem = max(float(base or 0), 0.0)
    base_limitada = min(rem, max(float(teto_restante), 0.0))
    if grupo == 'progressiva':
        # A contribuição progressiva não deve ser levada ao teto apenas porque
        # existe um teto. A base é a remuneração global efetivamente informada
        # nos vínculos progressivos, limitada ao teto.
        calc = calcular_contribuicao_progressiva_pelo_total(min(rem, max(float(teto_restante), 0.0)), tabela)
        return {
            'remuneracao': rem,
            'base_maxima': calc['base_considerada'],
            'contribuicao_maxima': calc['contribuicao_maxima'],
            'faixas': calc['faixas'],
            'atingiu_teto': calc['atingiu_teto'],
        }
    aliquota = 0.11 if grupo == '11' else 0.20
    return {
        'remuneracao': rem,
        'base_maxima': base_limitada,
        'contribuicao_maxima': base_limitada * aliquota,
        'faixas': [],
    }


def apurar_competencia(grupo, teto: Optional[float], tipo_competencia='mensal'):
    """Consolida todos os vínculos de uma competência e calcula o máximo permitido.

    A ordem de ocupação usada nesta versão segue o modelo prático da planilha-base:
    progressiva primeiro, depois 11% e, por fim, 20%. Isso permite que um vínculo
    progressivo que já consuma o teto deixe saldo zero para os vínculos posteriores.
    """
    if teto is None:
        return {'status': 'TETO_NAO_CADASTRADO'}

    g = grupo.copy()
    g['rendimento_tributavel'] = pd.to_numeric(g['rendimento_tributavel'], errors='coerce').fillna(0.0)
    g['previdencia_oficial'] = pd.to_numeric(g['previdencia_oficial'], errors='coerce').fillna(0.0)
    g['grupo_previdenciario'] = g['grupo_previdenciario'].fillna('nao_definido').astype(str)

    # Uma fonte pode informar Previdência Oficial mesmo sem informar remuneração.
    # Nesse caso, o recolhimento da DIRF deve entrar integralmente na contribuição
    # efetiva. Como a remuneração é zero, a classificação 11/20/progressiva não é
    # necessária para calcular o máximo dessa fonte: sua base máxima é, por
    # definição, R$ 0,00. Portanto, não bloqueamos a competência por classificação
    # pendente quando a fonte possui apenas recolhimento e remuneração zero.
    pendentes_df = g[
        g['grupo_previdenciario'].eq('nao_definido') &
        (g['rendimento_tributavel'].abs() >= 0.005)
    ]
    unknown = sorted(pendentes_df['cnpj_declarante'].dropna().astype(str).unique())
    fontes_recolhimento_sem_remuneracao = sorted(
        g.loc[
            g['rendimento_tributavel'].abs() < 0.005,
            'cnpj_declarante'
        ].dropna().astype(str).unique()
    )
    if unknown:
        return {
            'status': 'CLASSIFICACAO_PENDENTE',
            'tipo_competencia': tipo_competencia,
            'teto_previdenciario': float(teto),
            'cnpjs_pendentes': ', '.join(unknown),
            'soma_contribuicoes_recolhidas': float(g['previdencia_oficial'].sum()),
            'fontes_recolhimento_sem_remuneracao': fontes_recolhimento_sem_remuneracao,
        }

    # Consolidação por CNPJ + grupo evita que várias linhas da mesma fonte
    # apareçam como vínculos distintos no cálculo. A identidade é o CNPJ;
    # páginas/blocos separados da DIRF não criam novos vínculos.
    #
    # Base normativa da metodologia: IN RFB 2.110/2022, art. 49, §2º, II, b.
    # Para serviços concomitantes de empregado e contribuinte individual,
    # primeiro é considerada a soma das remunerações de empregado (progressiva);
    # somente a diferença até o teto fica disponível para o grupo de CI/20%.
    fontes = (g.groupby(['cnpj_declarante', 'grupo_previdenciario'], dropna=False, as_index=False)
                .agg(remuneracao=('rendimento_tributavel', 'sum'),
                     contribuicao_recolhida=('previdencia_oficial', 'sum'),
                     nome_declarante=('nome_declarante_dirf', lambda s: ' / '.join(sorted(set(str(x) for x in s.dropna()), key=str.casefold)))))

    teto_f = float(teto)
    saldo = teto_f
    max_total = 0.0
    partes = {}
    saldos = {}
    # Hierarquia de ocupação do teto, conforme a planilha de referência:
    # 1º Progressiva, 2º 11%, 3º 20%.
    # A classificação do vínculo permanece independente da quantidade de
    # remuneração/contribuição em uma competência. O que muda por competência
    # é apenas o saldo disponível do teto para cada grupo.
    ordem = ['progressiva', '11', '20']
    tabela = tabela_por_competencia((str(grupo['competencia'].iloc[0]) if 'competencia' in grupo.columns and len(grupo) else ''))
    if tipo_competencia == '13º':
        ano = str(grupo['competencia'].iloc[0])[:4] if 'competencia' in grupo.columns and len(grupo) else ''
        tabela = tabela_por_competencia(f'{ano}-12') if ano else None
    if tabela is None:
        return {'status': 'TABELA_NAO_CADASTRADA', 'tipo_competencia': tipo_competencia, 'teto_previdenciario': teto_f}

    for grupo_nome in ordem:
        sg = fontes[fontes['grupo_previdenciario'].eq(grupo_nome)]
        rem = float(sg['remuneracao'].sum()) if not sg.empty else 0.0
        rec = _calcular_grupo(rem, grupo_nome, tabela, saldo)
        partes[grupo_nome] = rec
        saldo = max(saldo - rec['base_maxima'], 0.0)
        saldos[grupo_nome] = saldo
        max_total += rec['contribuicao_maxima']

    contrib = float(fontes['contribuicao_recolhida'].sum())
    excesso = contrib - max_total
    return {
        'status': 'OK',
        'tipo_competencia': tipo_competencia,
        'teto_previdenciario': teto_f,
        'metodologia_tabela': tabela['metodologia'],
        'tabela_id': tabela['id'],
        'fonte_tabela': tabela['fonte'],
        'base_normativa': 'IN RFB nº 2.110/2022, art. 49, § 2º, II, b',
        'regra_apuracao': '1º soma das remunerações de empregado (progressiva); 2º saldo do teto para contribuinte individual/20%',
        'remuneracao_progressiva': partes['progressiva']['remuneracao'],
        'base_maxima_progressiva': partes['progressiva']['base_maxima'],
        'contribuicao_maxima_progressiva': partes['progressiva']['contribuicao_maxima'],
        'progressiva_atingiu_teto': bool(partes['progressiva'].get('atingiu_teto', False)),
        'remuneracao_11': partes['11']['remuneracao'],
        'base_maxima_11': partes['11']['base_maxima'],
        'contribuicao_maxima_11': partes['11']['contribuicao_maxima'],
        'remuneracao_20': partes['20']['remuneracao'],
        'base_maxima_20': partes['20']['base_maxima'],
        'saldo_teto_apos_progressiva': float(saldos.get('progressiva', teto_f)),
        'saldo_teto_apos_11': float(saldos.get('11', saldos.get('progressiva', teto_f))),
        'saldo_teto_apos_20': float(saldos.get('20', saldos.get('11', saldos.get('progressiva', teto_f)))),
        'contribuicao_maxima_20': partes['20']['contribuicao_maxima'],
        'contribuicao_maxima_total': max_total,
        'soma_contribuicoes_recolhidas': contrib,
        'contribuicao_acima_teto': max(excesso, 0.0),
        'diferenca_recolhido_menos_maximo': excesso,
        'fontes': fontes.to_dict(orient='records'),
        'fontes_recolhimento_sem_remuneracao': fontes_recolhimento_sem_remuneracao,
        'faixas_progressiva': partes['progressiva']['faixas'],
    }


def _ordem_competencia(item):
    comp, tipo = item
    try:
        ano = int(str(comp)[:4])
    except Exception:
        ano = 9999
    if tipo == '13º':
        return (ano, 13)
    try:
        mes = int(str(comp)[5:7])
    except Exception:
        mes = 99
    return (ano, mes)


def apurar(df, tetos):
    """Apura mensal e 13º por competência, consolidando N vínculos selecionados."""
    if df is None or df.empty:
        return pd.DataFrame()
    base = df[df['tipo_competencia'].isin(['mensal', '13º'])].copy()
    if base.empty:
        return pd.DataFrame()

    rows = []
    for (comp, tipo), g in base.groupby(['competencia', 'tipo_competencia'], dropna=False):
        teto = _teto_da_competencia(str(comp), str(tipo), tetos)
        r = apurar_competencia(g, teto, str(tipo))
        r = {'competencia': comp, **r}
        rows.append(r)

    if not rows:
        return pd.DataFrame()
    result = pd.DataFrame(rows)
    result['_ord'] = result.apply(lambda r: _ordem_competencia((r['competencia'], r.get('tipo_competencia', 'mensal'))), axis=1)
    result = result.sort_values('_ord').drop(columns='_ord').reset_index(drop=True)
    return result
