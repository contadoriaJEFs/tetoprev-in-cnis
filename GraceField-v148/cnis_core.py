import re
from io import BytesIO
import fitz

CNPJ_RE = re.compile(r'\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b')
SEQ_RE = re.compile(r'^\s*(\d+)\s*$')
DATE_RANGE_RE = re.compile(r'^(\d{2}/\d{2}/\d{4})(?:\s+(\d{2}/\d{2}/\d{4}|\d{2}/\d{4}))?$')
DATE_RE = re.compile(r'^\d{2}/\d{2}/\d{4}$')


def normalize_cnpj(v):
    return re.sub(r'\D', '', str(v or '')) if v else ''


def _page_number(text, fallback):
    m = re.search(r'Página\s+(\d+)\s+de\s+(\d+)', text or '')
    return int(m.group(1)) if m else fallback


def _clean_cnpj(c):
    return normalize_cnpj(c)


def _is_header_start(lines, i):
    # Repeated CNIS vínculo table header.
    return i + 1 < len(lines) and lines[i].strip() == 'Código Emp.'


def _parse_vinculos_page(text, page_no):
    lines = [x.strip() for x in (text or '').splitlines() if x.strip()]
    out = []
    i = 0
    while i < len(lines):
        if not _is_header_start(lines, i):
            i += 1
            continue
        # Find Seq. and then its numeric value within the next 15 lines.
        seq_idx = next((j for j in range(i, min(i + 15, len(lines))) if lines[j] == 'Seq.'), None)
        if seq_idx is None:
            i += 1
            continue
        k = seq_idx + 1
        while k < len(lines) and not SEQ_RE.match(lines[k]):
            k += 1
        if k >= len(lines):
            i += 1
            continue
        seq = int(lines[k])
        # Block ends at next repeated table header or Relações Previdenciárias.
        end = k + 1
        while end < len(lines) and not _is_header_start(lines, end) and lines[end] != 'Relações Previdenciárias':
            end += 1
        block = lines[k:end]
        tipo_idx = next((j for j, v in enumerate(block) if v in ('Contribuinte Individual', 'Empregado ou Agente', 'Público')), None)
        if tipo_idx is None:
            i = end
            continue
        if tipo_idx + 1 < len(block) and block[tipo_idx] == 'Empregado ou Agente' and block[tipo_idx + 1] == 'Público':
            tipo = 'Empregado ou Agente Público'
        else:
            tipo = block[tipo_idx]
        # CNPJ immediately following sequence is the employer/origin CNPJ for employee links.
        cnpj_origem = ''
        for v in block[1:8]:
            if CNPJ_RE.fullmatch(v):
                cnpj_origem = _clean_cnpj(v)
                break
        # Para CI, coletamos os CNPJs das linhas de remuneração e, quando
        # disponível, a natureza da prestação: Cooperado / Não Cooperado.
        cnpjs = set()
        cooperacao_por_cnpj = {}
        if cnpj_origem:
            cnpjs.add(cnpj_origem)

        competencia_re = re.compile(r'^\d{2}/\d{4}$')
        row_starts = [pos for pos, valor in enumerate(block) if competencia_re.match(valor)]
        for rpos, pos in enumerate(row_starts):
            end_row = row_starts[rpos + 1] if rpos + 1 < len(row_starts) else len(block)
            row = block[pos:end_row]
            row_cnpjs = set()
            for campo in row[1:]:
                for c in CNPJ_RE.findall(campo):
                    row_cnpjs.add(_clean_cnpj(c))
            cnpjs.update(row_cnpjs)
            forma = ''
            for campo in row[1:]:
                if campo in ('Cooperado', 'Não Cooperado'):
                    forma = campo
                    break
            if forma == 'Cooperado':
                status = 'cooperado'
            elif forma == 'Não Cooperado':
                status = 'nao_cooperado'
            else:
                status = ''
            if status:
                for c in row_cnpjs:
                    cooperacao_por_cnpj.setdefault(c, set()).add(status)

        # Fallback para CNPJs que apareçam no bloco fora das linhas
        # estruturadas de remuneração.
        for v in block:
            for c in CNPJ_RE.findall(v):
                cnpjs.add(_clean_cnpj(c))

        # Se houver evidência conflitante no mesmo CNPJ, preservamos o estado
        # como 'misto' para exigir análise, em vez de escolher silenciosamente.
        cooperacao = {}
        for c in cnpjs:
            estados = cooperacao_por_cnpj.get(c, set())
            if 'cooperado' in estados and 'nao_cooperado' in estados:
                cooperacao[c] = 'misto'
            elif 'cooperado' in estados:
                cooperacao[c] = 'cooperado'
            elif 'nao_cooperado' in estados:
                cooperacao[c] = 'nao_cooperado'
            else:
                cooperacao[c] = 'nao_identificado'
        # Date range: first line(s) after tipo usually contain it.
        inicio = fim = ''
        for v in block[tipo_idx + 1:tipo_idx + 6]:
            m = DATE_RANGE_RE.match(v)
            if m:
                inicio, fim = m.group(1), (m.group(2) or '')
                break
        indicadores = []
        for j, v in enumerate(block):
            if v == 'Indicadores:' and j + 1 < len(block):
                # Indicators continue until a known table/header or next field.
                for z in block[j + 1:min(j + 6, len(block))]:
                    if z not in ('Competência', 'Remunerações') and not CNPJ_RE.fullmatch(z):
                        if re.fullmatch(r'[A-Z0-9_-]{3,}', z):
                            indicadores.append(z)
        out.append({
            'seq': seq,
            'tipo_filiado': tipo,
            'cnpj_origem': cnpj_origem,
            'cnpjs': sorted(cnpjs),
            'data_inicio': inicio,
            'data_fim': fim,
            'indicadores': sorted(set(indicadores)),
            'cooperacao_por_cnpj': cooperacao,
            'pagina': page_no,
        })
        i = end
    return out


def extract_cnis(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype='pdf')
    vinculos = []
    paginas = []
    for idx, page in enumerate(doc):
        text = page.get_text('text') or ''
        page_no = _page_number(text, idx + 1)
        paginas.append({'pagina': page_no, 'texto': text})
        vinculos.extend(_parse_vinculos_page(text, page_no))
    # Remove duplicated block parses caused by repeated headers, preserving page.
    uniq = {}
    for v in vinculos:
        key = (v['pagina'], v['seq'], v['tipo_filiado'], v['data_inicio'], v['data_fim'], tuple(v['cnpjs']))
        uniq[key] = v
    vinculos = list(uniq.values())

    # Build CNPJ evidence. For CI, the CNPJ can occur in remuneration rows rather than origin.
    por_cnpj = {}
    for v in vinculos:
        for cnpj in v['cnpjs']:
            por_cnpj.setdefault(cnpj, []).append({
                'cnpj': cnpj,
                'seq': v['seq'],
                'tipo_filiado': v['tipo_filiado'],
                'cnpj_origem': v['cnpj_origem'],
                'data_inicio': v['data_inicio'],
                'data_fim': v['data_fim'],
                'indicadores': v['indicadores'],
                'cooperacao': (v.get('cooperacao_por_cnpj') or {}).get(cnpj, 'nao_identificado'),
                'pagina': v['pagina'],
            })
    for cnpj in por_cnpj:
        por_cnpj[cnpj] = sorted(por_cnpj[cnpj], key=lambda x: (x['pagina'], x['seq']))
    return {
        'paginas': len(doc),
        'vinculos': vinculos,
        'por_cnpj': por_cnpj,
    }


def render_cnis_page(pdf_bytes, page_no, cnpj=None, seq=None, dpi=180):
    """Renderiza uma evidência CNIS legível, priorizando o bloco do vínculo.

    A versão anterior procurava o número da sequência diretamente na página.
    Como números curtos podem aparecer em outros pontos do documento, isso
    podia produzir um recorte deslocado (inclusive no rodapé). Agora a busca
    prioriza o bloco textual que contém a natureza do vínculo e a sequência,
    mantendo uma área vertical ampla para incluir o início das remunerações.
    """
    doc = fitz.open(stream=pdf_bytes, filetype='pdf')
    if page_no < 1 or page_no > len(doc):
        return None
    page = doc[page_no - 1]
    rect = page.rect
    clip = None

    # 1) Localiza o bloco do vínculo pela natureza + sequência.
    tipo_alvos = [
        'Contribuinte Individual',
        'Empregado ou Agente Público',
        'Empregado ou Agente',
    ]
    blocks = page.get_text('blocks') or []
    candidato = None
    seq_txt = str(seq) if seq is not None else ''
    cnpj_norm = normalize_cnpj(cnpj)
    for b in blocks:
        txt = str(b[4] or '').replace('\n', ' ')
        tem_tipo = any(t in txt for t in tipo_alvos)
        tem_seq = bool(seq_txt and re.search(rf'(?<!\d){re.escape(seq_txt)}(?!\d)', txt))
        if tem_tipo and (tem_seq or not seq_txt):
            # Para CI, o bloco pode conter vários CNPJs nas linhas seguintes;
            # ainda assim a natureza do vínculo é a evidência principal.
            candidato = b
            break

    if candidato is not None:
        # O bloco de identificação costuma ficar imediatamente antes das
        # linhas de remuneração. Mantemos uma janela vertical generosa.
        y0 = max(rect.y0, candidato[1] - 75)
        y1 = min(rect.y1, candidato[1] + 560)
        clip = fitz.Rect(rect.x0 + 25, y0, rect.x1 - 25, y1)
    else:
        # Fallback: procura o CNPJ, mas nunca usa números curtos isolados.
        targets = []
        if cnpj:
            # Procura primeiro a forma formatada; depois as variantes sem pontuação.
            targets.extend(page.search_for(str(cnpj)))
            if not targets and cnpj_norm:
                targets.extend(page.search_for(cnpj_norm))
        if targets:
            r = targets[0]
            clip = fitz.Rect(
                max(rect.x0, r.x0 - 180),
                max(rect.y0, r.y0 - 120),
                min(rect.x1, r.x1 + 300),
                min(rect.y1, r.y1 + 520),
            )

    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, clip=clip or rect, alpha=False)
    return pix.tobytes('png')
