from motor_previdenciario import verificar_tabela, tabela_por_competencia
from dirf_core import extract_pdf, validate_records
from pathlib import Path
import pandas as pd

EXPECTED = {
    '2017-01':'2017','2019-12':'2019','2020-01':'2020_01_02','2020-03':'2020_03_12',
    '2021-12':'2021','2022-01':'2022','2023-04':'2023_01_04','2023-05':'2023_05_12',
    '2024-01':'2024','2025-01':'2025','2026-01':'2026'
}
for comp, ident in EXPECTED.items():
    assert tabela_por_competencia(comp)['id'] == ident
assert round(verificar_tabela('2019-01', 4000)['contribuicao_calculada'], 2) == 440.00
assert round(verificar_tabela('2020-03', 4000)['contribuicao_calculada'], 2) == 418.95
p = Path('/mnt/data/Suzana Marine - DIRFs.pdf')
if p.exists():
    records, declarations, pages = extract_pdf(p.read_bytes())
    for r in records: r['arquivo_origem'] = p.name
    checks = validate_records(records)
    assert len(records) == 1414
    assert len(declarations) == 101
    assert pages == 135
    assert len(checks) == 101
    assert not [x for x in checks if x['status'] != 'OK']
print('OK — smoke tests concluídos.')


# V1.2.4: tolerância usa diferença interna antes do arredondamento visual.
from motor_previdenciario import verificar_tabela
r = verificar_tabela('2023-02', 1674.66, 131.18, tolerancia=0.01)
assert r['status'] == 'COMPATIVEL'
r2 = verificar_tabela('2023-02', 1674.66, 131.201, tolerancia=0.01)
assert r2['status'] == 'DIFERENCA_PARA_ANALISE'
r3 = verificar_tabela('2023-02', 1674.66, 131.201, tolerancia=0.02)
assert r3['status'] == 'COMPATIVEL'

# V1.2.7 — 13º é competência própria e usa a tabela de dezembro do ano.
from motor_previdenciario import verificar_13o
r13 = verificar_13o(2024, 5500.63, 566.89)
assert r13['tipo_competencia'] == '13º'
assert r13['competencia'] == '2024-13'
assert r13['tabela_id'] == '2024'
assert r13['status'] == 'ANALISE_13O_CONJUNTA'

# V1.2.9 — apuração conjunta de múltiplos vínculos, seguindo a planilha-base.
from motor_previdenciario import apurar_competencia

def _caso(comp, rem_prog, prev_prog, rem20, prev20):
    return pd.DataFrame([
        {'competencia': comp, 'tipo_competencia': 'mensal', 'cnpj_declarante': 'A', 'nome_declarante_dirf': 'Sociedade Pernambucana', 'grupo_previdenciario': 'progressiva', 'rendimento_tributavel': rem_prog, 'previdencia_oficial': prev_prog},
        {'competencia': comp, 'tipo_competencia': 'mensal', 'cnpj_declarante': 'B', 'nome_declarante_dirf': 'Coopanest', 'grupo_previdenciario': '20', 'rendimento_tributavel': rem20, 'previdencia_oficial': prev20},
    ])

jan25 = apurar_competencia(_caso('2025-01', 5993.86, 657.95, 114310.77, 432.71), 8157.41)
assert jan25['status'] == 'OK'
assert round(jan25['contribuicao_maxima_progressiva'], 2) == 648.74
assert round(jan25['saldo_teto_apos_progressiva'], 2) == 2163.55
assert round(jan25['contribuicao_maxima_20'], 2) == 432.71
assert round(jan25['contribuicao_maxima_total'], 2) == 1081.45
assert round(jan25['soma_contribuicoes_recolhidas'], 2) == 1090.66
assert round(jan25['contribuicao_acima_teto'], 2) == 9.21

jul25 = apurar_competencia(_caso('2025-07', 13555.14, 1516.88, 71384.43, 153.53), 8157.41)
assert jul25['status'] == 'OK'
assert round(jul25['contribuicao_maxima_progressiva'], 2) == 951.64
assert round(jul25['saldo_teto_apos_progressiva'], 2) == 0.00
assert round(jul25['contribuicao_maxima_20'], 2) == 0.00
assert round(jul25['contribuicao_maxima_total'], 2) == 951.64
assert round(jul25['soma_contribuicoes_recolhidas'], 2) == 1670.41
assert round(jul25['contribuicao_acima_teto'], 2) == 718.77

print('OK — testes V1.2.9 de apuração conjunta concluídos.')


# V1.2.9 — a Verificação respeita a classificação da fonte apenas na coluna calculada.
from motor_previdenciario import verificar_por_grupo
r20 = verificar_por_grupo('2025-07', 71384.43, '20', 153.53)
assert round(r20['contribuicao_calculada'], 2) == 1631.48
r11 = verificar_por_grupo('2025-07', 5000, '11', 550)
assert round(r11['contribuicao_calculada'], 2) == 550.00
print('OK — testes V1.2.9 de classificação na verificação concluídos.')


# V1.2.11 — Previdência DIRF deve ser considerada mesmo quando a remuneração da fonte é zero.
caso_sem_rem = pd.DataFrame([
    {'competencia': '2021-04', 'tipo_competencia': 'mensal', 'cnpj_declarante': 'A', 'nome_declarante_dirf': 'COOMEB', 'grupo_previdenciario': '11', 'rendimento_tributavel': 23290.64, 'previdencia_oficial': 620.62},
    {'competencia': '2021-04', 'tipo_competencia': 'mensal', 'cnpj_declarante': 'B', 'nome_declarante_dirf': 'Secretaria Estadual de Saúde', 'grupo_previdenciario': '11', 'rendimento_tributavel': 0.00, 'previdencia_oficial': 366.35},
])
r_sem_rem = apurar_competencia(caso_sem_rem, 6433.57)
assert r_sem_rem['status'] == 'OK'
assert round(r_sem_rem['soma_contribuicoes_recolhidas'], 2) == 986.97
assert round(r_sem_rem['contribuicao_maxima_total'], 2) == 707.69
assert round(r_sem_rem['contribuicao_acima_teto'], 2) == 279.28
assert 'B' in r_sem_rem['fontes_recolhimento_sem_remuneracao']

# A fonte sem remuneração e com recolhimento não deve bloquear a apuração mesmo sem classificação.
caso_sem_class = caso_sem_rem.copy()
caso_sem_class.loc[caso_sem_class['cnpj_declarante'].eq('B'), 'grupo_previdenciario'] = 'nao_definido'
r_sem_class = apurar_competencia(caso_sem_class, 6433.57)
assert r_sem_class['status'] == 'OK'
assert round(r_sem_class['soma_contribuicoes_recolhidas'], 2) == 986.97
assert round(r_sem_class['contribuicao_acima_teto'], 2) == 279.28
print('OK — V1.2.11: recolhimento com remuneração zero preservado na apuração.')

# V1.2.16 — vínculo persistente por CNPJ e prioridade do grupo 11% quando ele existe.
from motor_previdenciario import classificar_declarante
split = pd.DataFrame([
    {'cnpj_declarante':'10.572.048/0001-28','cnpj_chave':'10572048000128','grupo_previdenciario':'nao_definido','rendimento_tributavel':0,'previdencia_oficial':366.35},
    {'cnpj_declarante':'10.572.048/0001-28','cnpj_chave':'10572048000128','grupo_previdenciario':'nao_definido','rendimento_tributavel':1000,'previdencia_oficial':110},
])
cs = classificar_declarante(split, {'10.572.048/0001-28':'11'})
assert cs['grupo_previdenciario'].tolist() == ['11','11']

caso_2023 = pd.DataFrame([
    {'competencia':'2023-03','tipo_competencia':'mensal','cnpj_declarante':'A','nome_declarante_dirf':'COOMEB','grupo_previdenciario':'11','rendimento_tributavel':11208.01,'previdencia_oficial':0},
    {'competencia':'2023-03','tipo_competencia':'mensal','cnpj_declarante':'B','nome_declarante_dirf':'FGH','grupo_previdenciario':'20','rendimento_tributavel':0,'previdencia_oficial':877.22},
    {'competencia':'2023-03','tipo_competencia':'mensal','cnpj_declarante':'C','nome_declarante_dirf':'RHP','grupo_previdenciario':'progressiva','rendimento_tributavel':14716.62,'previdencia_oficial':877.22},
])
r23 = apurar_competencia(caso_2023, 7507.49)
assert r23['status'] == 'OK'
assert round(r23['contribuicao_maxima_progressiva'],2) == 877.24
assert round(r23['contribuicao_maxima_11'],2) == 0.00
assert round(r23['contribuicao_maxima_20'],2) == 0.00
assert round(r23['contribuicao_maxima_total'],2) == 877.24
assert round(r23['soma_contribuicoes_recolhidas'],2) == 1754.44
assert round(r23['contribuicao_acima_teto'],2) == 877.20
print('OK — V1.2.16: identidade persistente e hierarquia Progressiva → 11% → 20% validadas.')

# V1.2.20 — deduplicação documental: mesma declaração repetida no PDF não pode dobrar a apuração.
from deduplicacao_documental import marcar_duplicatas_documentais
pdf_teste = Path('/mnt/data/0031059-48.2026.4.05.8300_DIRF.pdf')
if pdf_teste.exists():
    rec20, dec20, _ = extract_pdf(pdf_teste.read_bytes())
    for r in rec20:
        r['arquivo_origem'] = pdf_teste.name
    d20, st20 = marcar_duplicatas_documentais(pd.DataFrame(rec20))
    assert st20['blocos_identificados'] == 16
    assert st20['blocos_unicos'] == 8
    assert st20['blocos_duplicados'] == 8
    assert st20['registros_duplicados'] == 112
    assert int(d20['duplicata_documental'].sum()) == 112
    assert int((~d20['duplicata_documental']).sum()) == 112
    fundo = d20[d20['cnpj_declarante'].astype(str).str.replace(r'\D', '', regex=True).eq('10392418000145') & d20['tipo_competencia'].eq('mensal') & d20['competencia'].isin(['2023-09','2023-10'])]
    assert round(float(fundo[fundo['competencia'].eq('2023-09')]['rendimento_tributavel'].sum()), 2) == 9600.00
    fundo_can = fundo[~fundo['duplicata_documental']]
    assert round(float(fundo_can[fundo_can['competencia'].eq('2023-09')]['rendimento_tributavel'].sum()), 2) == 4800.00
    assert round(float(fundo_can[fundo_can['competencia'].eq('2023-10')]['rendimento_tributavel'].sum()), 2) == 13068.75
    print('OK — V1.2.20: duplicatas documentais preservadas no RAW e excluídas do cálculo.')


# V1.2.34 — IN RFB 2.110/2022, art. 49, §2º, II, b:
# remuneração progressiva abaixo do teto não pode consumir automaticamente o teto.
from motor_previdenciario import calcular_contribuicao_progressiva_pelo_total
_t25 = tabela_por_competencia('2025-05')
_case = calcular_contribuicao_progressiva_pelo_total(5000.00, _t25)
assert round(_case['base_considerada'], 2) == 5000.00
assert _case['atingiu_teto'] is False
assert round(_case['contribuicao_maxima'], 2) == 509.60

# Quando a remuneração progressiva atinge o teto, aí sim o máximo do teto é usado.
_case_teto = calcular_contribuicao_progressiva_pelo_total(8157.41, _t25)
assert _case_teto['atingiu_teto'] is True
assert round(_case_teto['contribuicao_maxima'], 2) == 951.64

# V1.2.34 — caso misto progressiva + 20%: a progressiva ocupa apenas a remuneração
# global efetivamente existente; o CI/20% recebe somente o saldo do teto.
import pandas as pd
_case_misto = pd.DataFrame([
    {'cnpj_declarante':'11111111111111','grupo_previdenciario':'progressiva','rendimento_tributavel':5000.00,'previdencia_oficial':0.0,'nome_declarante_dirf':'EMP','competencia':'2025-05'},
    {'cnpj_declarante':'22222222222222','grupo_previdenciario':'20','rendimento_tributavel':10000.00,'previdencia_oficial':0.0,'nome_declarante_dirf':'CI','competencia':'2025-05'},
])
_r_misto = apurar_competencia(_case_misto, 8157.41, 'mensal')
assert _r_misto['status'] == 'OK'
assert round(_r_misto['base_maxima_progressiva'], 2) == 5000.00
assert round(_r_misto['contribuicao_maxima_progressiva'], 2) == 509.60
assert round(_r_misto['base_maxima_20'], 2) == 3157.41
assert round(_r_misto['contribuicao_maxima_20'], 2) == 631.48
assert round(_r_misto['contribuicao_maxima_total'], 2) == 1141.08


# V1.2.35 — demonstração da ocupação do teto por enquadramento, sem alterar
# os resultados do motor: a remuneração é separada por grupo e o saldo para 20%
# é o limite remanescente após Progressiva e 11%.
_case_planilha = pd.DataFrame([
    {'cnpj_declarante':'P','grupo_previdenciario':'progressiva','rendimento_tributavel':1518.00,'previdencia_oficial':113.85,'nome_declarante_dirf':'PROGRESSIVA','competencia':'2025-04'},
    {'cnpj_declarante':'C','grupo_previdenciario':'20','rendimento_tributavel':9800.88,'previdencia_oficial':1631.48,'nome_declarante_dirf':'COOPANEST','competencia':'2025-04'},
])
_r_planilha = apurar_competencia(_case_planilha, 8157.41)
assert _r_planilha['status'] == 'OK'
assert round(_r_planilha['remuneracao_progressiva'], 2) == 1518.00
assert round(_r_planilha['contribuicao_maxima_progressiva'], 2) == 113.85
assert round(_r_planilha['remuneracao_11'], 2) == 0.00
assert round(_r_planilha['remuneracao_20'], 2) == 9800.88
assert round(_r_planilha['saldo_teto_apos_progressiva'], 2) == 6639.41
assert round(_r_planilha['saldo_teto_apos_11'], 2) == 6639.41
assert round(_r_planilha['base_maxima_20'], 2) == 6639.41
assert round(_r_planilha['contribuicao_maxima_20'], 2) == 1327.88
assert round(_r_planilha['contribuicao_maxima_total'], 2) == 1441.73
assert round(_r_planilha['contribuicao_acima_teto'], 2) == 303.60

print('OK — V1.2.35: remunerações por enquadramento e saldo remanescente validados contra o caso da planilha.')

# V1.2.48 — CNIS determina a classificação objetiva.
from classificador_previdenciario import sugerir_classificacao as _sug_cnis
import pandas as _pd_cnis
_rows_cnis = _pd_cnis.DataFrame([{
    'rendimento_tributavel': 10000.0,
    'previdencia_oficial': 499.0,
    'tipo_competencia': 'mensal',
    'codigo_receita': '0588',
}])
assert _sug_cnis(_rows_cnis, [{'tipo_filiado': 'Contribuinte Individual', 'cooperacao': 'nao_cooperado'}])['classificacao_sugerida'] == '11'
assert _sug_cnis(_rows_cnis, [{'tipo_filiado': 'Contribuinte Individual', 'cooperacao': 'cooperado'}])['classificacao_sugerida'] == '20'
assert _sug_cnis(_rows_cnis, [{'tipo_filiado': 'Empregado ou Agente Público', 'cooperacao': 'nao_identificado'}])['classificacao_sugerida'] == 'progressiva'
print('OK — V1.2.48: classificação CNIS 11%/20%/progressiva validada.')
