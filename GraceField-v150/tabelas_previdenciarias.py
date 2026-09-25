"""Base histórica das tabelas do RGPS usadas pelo Extrator DIRF + Motor Previdenciário.

Escopo desta base: Empregado, Empregado Doméstico e Trabalhador Avulso.
Não misturar com RPPS, contribuinte individual ou facultativo.
"""
import pandas as pd

TABELAS_HISTORICAS = [
    {'id':'2017','inicio':'2017-01','fim':'2017-12','metodologia':'tradicional','fonte':'INSS — Tabela de contribuição – histórico / Portaria Ministerial MF nº 8/2017','faixas':[(0.00,1659.38,0.08),(1659.38,2765.66,0.09),(2765.66,5531.31,0.11)],'teto':5531.31},
    {'id':'2018','inicio':'2018-01','fim':'2018-12','metodologia':'tradicional','fonte':'INSS — Tabela de contribuição – histórico / Portaria nº 15/2018','faixas':[(0.00,1693.72,0.08),(1693.72,2822.90,0.09),(2822.90,5645.80,0.11)],'teto':5645.80},
    {'id':'2019','inicio':'2019-01','fim':'2019-12','metodologia':'tradicional','fonte':'INSS — Tabela de contribuição – histórico / Portaria MF nº 9/2019','faixas':[(0.00,1751.81,0.08),(1751.81,2919.72,0.09),(2919.72,5839.45,0.11)],'teto':5839.45},
    {'id':'2020_01_02','inicio':'2020-01','fim':'2020-02','metodologia':'tradicional','fonte':'INSS — Tabela de contribuição – histórico','faixas':[(0.00,1830.29,0.08),(1830.29,3050.52,0.09),(3050.52,6101.06,0.11)],'teto':6101.06},
    {'id':'2020_03_12','inicio':'2020-03','fim':'2020-12','metodologia':'progressiva','fonte':'eSocial — faixas progressivas a partir de 01/03/2020','faixas':[(0.00,1045.00,0.075),(1045.00,2089.60,0.09),(2089.60,3134.40,0.12),(3134.40,6101.06,0.14)],'teto':6101.06},
    {'id':'2021','inicio':'2021-01','fim':'2021-12','metodologia':'progressiva','fonte':'INSS — Tabela de contribuição – histórico / Portaria SEPRT nº 477/2021','faixas':[(0.00,1100.00,0.075),(1100.00,2203.48,0.09),(2203.48,3305.22,0.12),(3305.22,6433.57,0.14)],'teto':6433.57},
    {'id':'2022','inicio':'2022-01','fim':'2022-12','metodologia':'progressiva','fonte':'Portaria MTP/ME nº 12/2022','faixas':[(0.00,1212.00,0.075),(1212.00,2427.35,0.09),(2427.35,3641.03,0.12),(3641.03,7087.22,0.14)],'teto':7087.22},
    {'id':'2023_01_04','inicio':'2023-01','fim':'2023-04','metodologia':'progressiva','fonte':'Portaria Interministerial MPS/MF nº 26/2023','faixas':[(0.00,1302.00,0.075),(1302.00,2571.29,0.09),(2571.29,3856.94,0.12),(3856.94,7507.49,0.14)],'teto':7507.49},
    {'id':'2023_05_12','inicio':'2023-05','fim':'2023-12','metodologia':'progressiva','fonte':'Portaria Interministerial MPS/MF nº 27/2023','faixas':[(0.00,1320.00,0.075),(1320.00,2571.29,0.09),(2571.29,3856.94,0.12),(3856.94,7507.49,0.14)],'teto':7507.49},
    {'id':'2024','inicio':'2024-01','fim':'2024-12','metodologia':'progressiva','fonte':'Portaria Interministerial MPS/MF nº 2/2024','faixas':[(0.00,1412.00,0.075),(1412.00,2666.68,0.09),(2666.68,4000.03,0.12),(4000.03,7786.02,0.14)],'teto':7786.02},
    {'id':'2025','inicio':'2025-01','fim':'2025-12','metodologia':'progressiva','fonte':'Portaria Interministerial MPS/MF nº 6/2025','faixas':[(0.00,1518.00,0.075),(1518.00,2793.88,0.09),(2793.88,4190.83,0.12),(4190.83,8157.41,0.14)],'teto':8157.41,'contribuicao_maxima_teto':951.64},
    {'id':'2026','inicio':'2026-01','fim':'2026-12','metodologia':'progressiva','fonte':'Portaria Interministerial MPS/MF nº 13/2026','faixas':[(0.00,1621.00,0.075),(1621.00,2902.84,0.09),(2902.84,4354.27,0.12),(4354.27,8475.55,0.14)],'teto':8475.55},
]

TETOS = {}
for tabela in TABELAS_HISTORICAS:
    for p in pd.period_range(pd.Period(tabela['inicio'],freq='M'), pd.Period(tabela['fim'],freq='M'), freq='M'):
        TETOS[str(p)] = tabela['teto']

def tabela_por_competencia(competencia):
    if not competencia or not isinstance(competencia,str): return None
    try: p=pd.Period(competencia,freq='M')
    except Exception: return None
    for tabela in TABELAS_HISTORICAS:
        if pd.Period(tabela['inicio'],freq='M') <= p <= pd.Period(tabela['fim'],freq='M'):
            return tabela
    return None
