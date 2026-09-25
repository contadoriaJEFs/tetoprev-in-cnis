import re, unicodedata, fitz

try:
    import pytesseract
    from PIL import Image
    import io
except Exception:  # OCR é opcional; a leitura nativa continua funcionando.
    pytesseract = None
    Image = None
    io = None

MONTHS={"Jan":1,"Fev":2,"Mar":3,"Abr":4,"Mai":5,"Jun":6,"Jul":7,"Ago":8,"Set":9,"Out":10,"Nov":11,"Dez":12}
MAIN_COLUMNS=["rendimento_tributavel","irrf","previdencia_oficial","dependentes","pensao_alimenticia","desconto_simplificado","previdencia_complementar","compensacao_judicial_ano_calendario","compensacao_judicial_anos_anteriores"]
CODE_CLASSIFICATION={"0561":"trabalho_assalariado","0588":"trabalho_sem_vinculo","3533":"aposentadoria_reserva_reforma_pensao_previdencia_publica","5928":"decisao_justica_federal","5706":"juros_sobre_capital_proprio","5557":"mercado_renda_variavel","6800":"fundos_investimento","6813":"fundos_acoes","8053":"aplicacoes_financeiras_renda_fixa"}

def clean_spaces(v): return re.sub(r"\s+"," ",v or "").strip()
def money_to_float(v):
    v=v.strip()
    return float(v.replace('.','').replace(',','.')) if v else 0.0
def parse_prefixed(lines,prefix):
    for line in lines:
        if line.startswith(prefix): return clean_spaces(line[len(prefix):])
    return ""
def parse_cnpj(lines):
    for line in lines:
        m=re.match(r"^CNPJ:\s*(.+)$",line)
        if m:return m.group(1).strip()
    return ""
def parse_numbered_field(lines,label):
    for i,line in enumerate(lines):
        if line.startswith(label):
            value=line[len(label):].strip()
            return value or (lines[i+1].strip() if i+1<len(lines) else "")
    return ""
def numeric_tokens(lines,start,count=9):
    nums=[]; j=start
    while j<len(lines) and len(nums)<count:
        if re.fullmatch(r"-?\d{1,3}(?:\.\d{3})*,\d{2}|-?\d+,\d{2}",lines[j]): nums.append(money_to_float(lines[j])); j+=1
        else: break
    return nums,j

def parse_main_table(lines,code_index):
    start=next((i for i in range(code_index,len(lines)) if lines[i] in MONTHS),None)
    if start is None:return []
    end=next((i for i in range(start,len(lines)) if lines[i]=="Meses"),len(lines))
    rows=[]; i=start
    legacy=["rendimento_tributavel","irrf","previdencia_oficial","dependentes","pensao_alimenticia","previdencia_complementar","compensacao_judicial_ano_calendario","compensacao_judicial_anos_anteriores"]
    while i<end:
        token=lines[i]
        if token in MONTHS or token in ("Tot","13º"):
            vals,nxt=numeric_tokens(lines,i+1,9)
            if len(vals) in (8,9):
                d=dict(zip(MAIN_COLUMNS,vals)) if len(vals)==9 else dict(zip(legacy,vals))
                if len(vals)==8:d["desconto_simplificado"]=0.0
                if token in MONTHS: row={"competencia":MONTHS[token],"competencia_nome":token,"tipo_competencia":"mensal"}
                elif token=="13º": row={"competencia":13,"competencia_nome":token,"tipo_competencia":"13º"}
                else: row={"competencia":None,"competencia_nome":token,"tipo_competencia":"total"}
                row.update(d); rows.append(row); i=nxt; continue
        i+=1
    return rows

def _parse_declaration_lines(lines, page_number, metodo_leitura='texto_nativo', conferencia_necessaria=False):
    lines=[clean_spaces(x) for x in lines if clean_spaces(x)]
    if "Dados do beneficiário:" not in lines:return []
    ano_match=re.search(r"Ano-calendário:\s*(\d{4})", " ".join(lines))
    ano_int=int(ano_match.group(1)) if ano_match else None
    code_idx=next((i for i,x in enumerate(lines) if x.startswith("Código de receita:")),None)
    if code_idx is None:return []
    code_raw=lines[code_idx][len("Código de receita:"):].strip(); m=re.match(r"(\d+)\s*-\s*(.*)",code_raw)
    codigo=m.group(1) if m else ""; descricao=m.group(2).strip() if m else code_raw
    name_lines=[x for x in lines if x.startswith("Nome constante no cadastro:")]
    dirf_lines=[x for x in lines if x.startswith("Nome constante na Dirf:")]
    benef_cad=clean_spaces(name_lines[0][len("Nome constante no cadastro:"):]) if name_lines else ""
    decl_cad=clean_spaces(name_lines[1][len("Nome constante no cadastro:"):]) if len(name_lines)>1 else ""
    benef_dirf=clean_spaces(dirf_lines[0][len("Nome constante na Dirf:"):]) if dirf_lines else ""
    decl_dirf=clean_spaces(dirf_lines[1][len("Nome constante na Dirf:"):]) if len(dirf_lines)>1 else ""
    rows=parse_main_table(lines,code_idx)
    if not rows:
        rows=parse_main_table_ocr(lines,code_idx)
    if not rows:return []
    meta={"pagina_pdf":page_number,"cpf_beneficiario":parse_prefixed(lines,"CPF:"),"nome_beneficiario_cadastro":benef_cad,"nome_beneficiario_dirf":benef_dirf,"cnpj_declarante":parse_cnpj(lines),"nome_declarante_cadastro":decl_cad,"nome_declarante_dirf":decl_dirf,"ano_calendario":ano_int,"data_entrega":parse_prefixed(lines,"Data de entrega:"),"tipo_declaracao":parse_prefixed(lines,"Tipo:"),"situacao_declaracao":parse_prefixed(lines,"Situação:"),"situacao_especial":parse_prefixed(lines,"Situação especial:"),"total_codigos_receita":parse_prefixed(lines,"Total de códigos de receita:"),"codigo_receita":codigo,"descricao_codigo_receita":descricao,"classificacao_codigo":CODE_CLASSIFICATION.get(codigo,"nao_classificado"),"fundo_clube":parse_numbered_field(lines,"Fundo/Clube:"),"numero_processo":parse_numbered_field(lines,"Número do processo:"),"metodo_leitura":metodo_leitura,"conferencia_necessaria":bool(conferencia_necessaria)}
    out=[]
    for r in rows:
        item={**meta,**r}
        if r['tipo_competencia']=='mensal' and ano_int:item['competencia']=f"{ano_int}-{r['competencia']:02d}"
        elif r['tipo_competencia']=='13º' and ano_int:item['competencia']=f"{ano_int}-13"
        out.append(item)
    return out

def parse_main_table_ocr(lines,code_index):
    """Reconhece linhas tabulares devolvidas pelo OCR (mês + 9 valores)."""
    rows=[]
    num_re=r"-?(?:\d{1,3}(?:\.\d{3})*|\d+),\d{2}"
    month_re=re.compile(rf"^(Jan|Fev|Mar|Abr|Mai|Jun|Jul|Ago|Set|Out|Nov|Dez|Tot|13º)\s+({num_re}(?:\s+{num_re}){{8}})\s*$",re.I)
    for line in lines[code_index+1:]:
        if line.startswith('Exigibilidade Suspensa'):
            break
        m=month_re.match(line)
        if not m: continue
        token=m.group(1); vals=[money_to_float(x) for x in m.group(2).split()]
        if len(vals)!=9: continue
        d=dict(zip(MAIN_COLUMNS,vals))
        if token in MONTHS:
            row={"competencia":MONTHS[token],"competencia_nome":token,"tipo_competencia":"mensal"}
        elif token.lower()=='tot':
            row={"competencia":None,"competencia_nome":token,"tipo_competencia":"total"}
        else:
            row={"competencia":13,"competencia_nome":"13º","tipo_competencia":"13º"}
        row.update(d); rows.append(row)
    return rows

def extract_declaration(page,page_number):
    text=page.get_text('text')
    return _parse_declaration_lines(text.splitlines(),page_number,'texto_nativo',False)

def _ocr_page_text(page, scale=3.0):
    if pytesseract is None or Image is None or io is None:
        return ''
    pix=page.get_pixmap(matrix=fitz.Matrix(scale,scale), alpha=False)
    img=Image.open(io.BytesIO(pix.tobytes('png')))
    # PSM 3 preserva melhor as linhas da tabela DIRF do que o PSM 6 neste tipo de PDF.
    # O ambiente de execução pode não ter o binário/idioma do Tesseract; nesse caso
    # a falha é devolvida ao diagnóstico da página, sem interromper os demais PDFs.
    try:
        return pytesseract.image_to_string(img, lang='por+eng', config='--psm 3')
    except Exception:
        return ''

def extract_document_identity(file_bytes):
    """Extrai identificação processual presente no PDF, quando houver página PJe.

    Não inventa dados: somente preenche processo/autor/réu quando o texto do
    próprio documento contém esses campos.
    """
    doc=fitz.open(stream=file_bytes,filetype='pdf')
    processo=autor=reu=''
    for page in doc:
        text=page.get_text('text') or ''
        if not processo:
            m=re.search(r"Número:\s*([0-9]{7}-[0-9]{2}\.[0-9]{4}\.[0-9]\.[0-9]{2}\.[0-9]{4})", text)
            if m: processo=m.group(1)
        if not autor:
            m=re.search(r"([^\n]+?)\s*\(AUTOR\)", text, re.I)
            if m: autor=clean_spaces(m.group(1))
        if not reu:
            m=re.search(r"([^\n]+?)\s*\(REU\)", text, re.I)
            if m: reu=clean_spaces(m.group(1))
        if processo and autor and reu: break
    return {'processo':processo,'autor':autor,'reu':reu}

def extract_pdf_with_diagnostics(file_bytes):
    doc=fitz.open(stream=file_bytes,filetype='pdf')
    records=[]; declarations=[]
    ocr_ok=False
    ocr_erro=''
    if pytesseract is not None:
        try:
            pytesseract.get_tesseract_version()
            ocr_ok=True
        except Exception as exc:
            ocr_erro=str(exc)
    else:
        ocr_erro='pytesseract/Pillow não disponíveis'
    diag={
        'paginas_total':len(doc), 'paginas_texto_nativo':0, 'paginas_dirf_nativas':0,
        'paginas_imagem_dirf':[], 'paginas_ocr':[], 'paginas_ocr_falha':[],
        'paginas_nao_dirf':0, 'ocr_disponivel':ocr_ok, 'ocr_erro':ocr_erro,
    }
    for pno,page in enumerate(doc,1):
        native=page.get_text('text') or ''
        if native.strip(): diag['paginas_texto_nativo'] += 1
        pr=extract_declaration(page,pno)
        if pr:
            diag['paginas_dirf_nativas'] += 1
            declarations.append(pr[0]); records.extend(pr)
            continue
        # Fallback somente quando a página parece ser imagem/scan ou quando a leitura nativa é muito curta.
        suspect=(len(native.strip()) < 700 and len(page.get_images(full=True)) > 0) or (len(native.strip()) < 350)
        if not suspect:
            diag['paginas_nao_dirf'] += 1
            continue
        ocr_text=_ocr_page_text(page)
        if not ocr_text:
            diag['paginas_ocr_falha'].append(pno)
            continue
        ocr_pr=_parse_declaration_lines(ocr_text.splitlines(),pno,'ocr',True)
        if ocr_pr:
            diag['paginas_ocr'].append(pno)
            diag['paginas_imagem_dirf'].append(pno)
            declarations.append(ocr_pr[0]); records.extend(ocr_pr)
        else:
            diag['paginas_ocr_falha'].append(pno)
    return records,declarations,len(doc),diag

def extract_pdf(file_bytes):
    records,declarations,pages,_diag=extract_pdf_with_diagnostics(file_bytes)
    return records,declarations,pages


def validate_records(records):
    df = __import__('pandas').DataFrame(records)
    checks = []
    if df.empty:
        return checks
    monthly = df[df['tipo_competencia'] == 'mensal'].copy()
    block_keys = ['arquivo_origem', 'pagina_pdf', 'ano_calendario', 'cnpj_declarante', 'codigo_receita', 'fundo_clube', 'numero_processo']
    for keys, grp in monthly.groupby(block_keys, dropna=False):
        vals = keys if isinstance(keys, tuple) else (keys,)
        mask = __import__('pandas').Series(True, index=df.index)
        for col, value in zip(block_keys, vals):
            if __import__('pandas').isna(value):
                mask &= df[col].isna()
            else:
                mask &= df[col].eq(value)
        total = df[mask & df['tipo_competencia'].eq('total')]
        if total.empty:
            continue
        expected = round(float(grp['rendimento_tributavel'].sum()), 2)
        informed = round(float(total.iloc[0]['rendimento_tributavel']), 2)
        diff = round(expected - informed, 2)
        checks.append({'arquivo': vals[0], 'pagina': vals[1], 'ano': vals[2], 'cnpj': vals[3], 'codigo': vals[4], 'fundo_clube': vals[5], 'numero_processo': vals[6], 'soma_meses': expected, 'total_DIRF': informed, 'diferenca': diff, 'status': 'OK' if abs(diff) < 0.01 else 'DIVERGÊNCIA'})
    return checks
