"""Pipeline determinístico do mapeamento AGERGS — celebração de convênio/contrato de delegação da regulação.

Adaptação das etapas determinísticas de metodologia-repo/scripts (trilhas, fichas, fatos, procedimento) a uma base
sem andamentos: os PDFs exportados do SEI-RS só trazem as peças. A trilha é reconstruída pela data de assinatura de
cada peça (ou, nas peças externas sem assinatura SEI, pela data escrita no texto, extraída na ficha).

Etapas (em ordem; cada uma grava em saida/):
  1. fichas   — junta as fichas dos agentes, ancora as evidências no texto (código), calcula esforço piso–teto
  2. linha    — linha do tempo por caso: ocorrências de cada tarefa do modelo, execução, espera antes e com quem
  3. fatos    — tabela de fatos citáveis (caso.* e coorte.*) e procedimento da coorte
  4. fase0    — indicadores por processo, posse por unidade, planilha da fase 0
Uso: python3 scripts/pipeline_agergs.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import statistics as st
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / "dados"
SAIDA = RAIZ / "saida"
BPMN = SAIDA / "bpmn"
F2 = SAIDA / "fase2"
for d in (SAIDA, BPMN, F2):
    d.mkdir(parents=True, exist_ok=True)

CASOS_EXCLUIDOS = {"Processo_Celebracao_Instrumentos", "Minuta_Padrao_Contrato_Delegacao"}  # processos de gestão
PARTES = {"Passo_Fundo_p1": "Passo_Fundo", "Passo_Fundo_p2": "Passo_Fundo"}

# ---------------------------------------------------------------- calendário (mesma regra de comum.py, perfil RS)
FERIADOS_MOVEIS = (-48, -47, -2, 60)
FERIADOS_FIXOS = [(1, 1), (4, 21), (5, 1), (9, 7), (9, 20), (10, 12), (11, 2), (11, 15), (11, 20), (12, 25)]


def _pascoa(ano):
    a, b, c = ano % 19, ano // 100, ano % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    return date(ano, (h + l_ - 7 * m + 114) // 31, ((h + l_ - 7 * m + 114) % 31) + 1)


_FER = []
for _y in range(2010, 2029):
    _p = _pascoa(_y)
    _FER += [_p + timedelta(days=k) for k in FERIADOS_MOVEIS] + [date(_y, m, d) for m, d in FERIADOS_FIXOS]
_FER = np.array(_FER, dtype="datetime64[D]")


def du(a: str, b: str) -> float:
    if not a or not b or b < a:
        return 0.0
    return float(np.busday_count(np.datetime64(a), np.datetime64(b), holidays=_FER))


# ---------------------------------------------------------------- vínculo atividade (ficha) → tarefa do modelo
# Encaminhamento puro não vira tarefa (regra 2 da ESPECIFICACAO_MODELO): conta como passagem.
ATIV_TAREFA = {
    "solicitacao_municipio": "t1", "autuacao_abertura": "t2",
    "juntada_documentos_municipio": "t3", "lei_autorizativa": "t3", "documento_externo_anexo": "t3",
    "analise_tecnica": "t4", "analise_economico_financeira": "t4",
    "elaboracao_minuta": "t5", "revisao_ajuste_minuta": "t5",
    "analise_juridica": "t6", "manifestacao_pge": "t7",
    "deliberacao_conselho_superior": "t8",
    "decisao_presidencia_diretoria": "t9", "inexigibilidade_licitacao": "t9",
    "envio_minuta_ao_municipio": "t10", "tratativa_com_municipio": "t10",
    "assinatura_instrumento": "t11", "publicacao_extrato": "t12",
    "comunicacao_prestador": "t13", "comunicacao_interna_pos_assinatura": "t13", "cadastro_controle": "t13",
    "cobranca_taxa_financeiro": "t13",
    "aditivo_alteracao": "t14", "arquivamento_encerramento": "t15",
    "encaminhamento_interno": None, "outro": None,
}
TERCEIROS = {"MUN", "EXT"}  # espera antes de ocorrência aberta por município ou prestador: tempo de terceiro, protegido
ANEXO_HISTORICO = {"documento_externo_anexo", "lei_autorizativa", "juntada_documentos_municipio"}

# ---------------------------------------------------------------- unidade pelo cargo do signatário
CARGO_UNIDADE = [
    (r"Procuradoria Setorial|Procurador", "PSE"),
    (r"OAB|Assuntos Jurídicos", "DAJ"),
    (r"Presidente|Assessora? do Conselho Superior|Gabinete da Presid|Secretári[oa]\(?a?\)? da Presid|Assessor Especial", "GP"),
    (r"Conselho Superior|^Conselheir", "CS"),
    (r"Diretor\(?a?\)?-Geral|Diretora-Geral|Diretoria-Geral", "DG"),
    (r"Saneamento", "DSI"), (r"Qualidade", "DQS"), (r"Tarifas", "DT"), (r"Tecnologia", "DTI"),
    (r"Institucionais", "DAI"), (r"Administrativo e Financeiro", "DAF"), (r"Transportes", "DTM"),
    (r"Atendimento ao Usuário", "DAU"),
]
FICHA_UNIDADE = [
    (r"munic|prefeit|câmara de vereadores|externo", "MUN"), (r"corsan|prestador|aegea", "EXT"),
    (r"procuradoria setorial|pge|\bpse\b", "PSE"), (r"jurídic|\bdaj\b", "DAJ"),
    (r"conselho superior|\bcs\b|conselheir", "CS"), (r"presid|\bgp\b", "GP"),
    (r"diretoria-geral|diretor-geral|\bdg\b", "DG"), (r"\bdsi\b|saneamento", "DSI"), (r"\bdqs\b|qualidade", "DQS"),
    (r"\bdt\b|tarifa", "DT"), (r"\bdti\b|tecnologia", "DTI"), (r"\bdai\b|institucion", "DAI"),
    (r"\bdaf\b|financeir|administrativ", "DAF"), (r"\bdtm\b|transporte", "DTM"), (r"\bdau\b|usuário|ouvidoria", "DAU"),
]
RAIA_UNIDADE = {"MUN": "MUN", "EXT": "MUN", "GP": "GP", "DG": "DG", "DSI": "TEC", "DQS": "TEC", "DT": "TEC",
                "DTI": "DG", "DAI": "DG", "DAF": "DG", "DTM": "TEC", "DAU": "DG", "DAJ": "DAJ", "PSE": "PSE", "CS": "CS"}


def unidade_cargo(cargo: str) -> str | None:
    for pad, u in CARGO_UNIDADE:
        if re.search(pad, cargo or "", re.I):
            return u
    return None


def unidade_ficha(txt: str) -> str | None:
    for pad, u in FICHA_UNIDADE:
        if re.search(pad, txt or "", re.I):
            return u
    return None


# ---------------------------------------------------------------- ancoragem (mesma regra de fichas_trabalho.py)
def _norm_ev(s):
    s = re.sub(r"[‘’“”\"'«»]", "", str(s or "")).lower()
    return re.sub(r"[\s\W_]+", " ", s).strip()


def ancorar(ficha, texto):
    t = _norm_ev(texto)
    cont = Counter()

    def ok(ev):
        partes = [p for p in re.split(r"\.\.\.|…", str(ev or "")) if len(_norm_ev(p)) >= 8]
        return bool(partes) and all(_norm_ev(p) in t for p in partes)

    def marca(x):
        if isinstance(x, dict):
            if "evidencia" in x:
                x["ancorado"] = ok(x.get("evidencia"))
                cont["ancorado" if x["ancorado"] else "nao_ancorado"] += 1
            for v in x.values():
                marca(v)
        elif isinstance(x, list):
            for v in x:
                marca(v)

    marca(ficha)
    return cont


# ---------------------------------------------------------------- esforço piso–teto (hipótese; regra de comum.py)
CARACTERES_LAUDA = 1250
H_LAUDA = {1: 0.05, 2: 0.25, 3: 0.5, 4: 0.9, 5: 1.5}
H_BASE = {"encaminhamento": 0.1, "comunicacao": 0.3, "instrucao_processual": 0.3, "analise_juridica": 1.0,
          "analise_tecnica_engenharia": 1.0, "analise_economico_financeira": 1.0, "auditoria_conferencia": 0.5,
          "relatoria_decisao": 1.0, "publicacao_registro": 0.2}
H_LEITURA = 0.25


def esforco(f, nchar):
    """piso = horas-base da natureza + conferência da peça (0,05 h/lauda); teto = horas_modelo de comum.py."""
    nat = f.get("natureza_trabalho")
    if f.get("autoria") != "AGERGS" or nat == "documento_externo":
        return 0.0, 0.0
    base = H_BASE.get(nat, 0.3)
    comp = f.get("composicao_texto") or {}
    fr = min(max(float(comp.get("pct_autoral") or 0) / 100, 0), 1)
    try:
        c = min(max(int(round(float(f.get("complexidade") or 1))), 1), 5)
    except (TypeError, ValueError):
        c = 1
    laudas = nchar / CARACTERES_LAUDA
    piso = base + laudas * 0.05
    n_ins = len([i for i in f.get("insumos") or [] if i.get("ancorado")])
    teto = base + laudas * fr * H_LAUDA[c] + n_ins * H_LEITURA
    return round(piso, 3), round(max(teto, piso), 3)


def estat(vals):
    v = sorted(float(x) for x in vals if x is not None)
    if not v:
        return None
    q = np.percentile(v, [25, 50, 75]) if len(v) > 1 else [v[0]] * 3
    return dict(n=len(v), media=round(st.mean(v), 1), mediana=round(float(q[1]), 1), q1=round(float(q[0]), 1),
                q3=round(float(q[2]), 1), max=round(v[-1], 1), min=round(v[0], 1))


# ================================================================ 1. fichas
def etapa_fichas():
    docs = {(r["processo"], int(r["seq"])): r for r in csv.DictReader(open(DADOS / "documentos.csv"))}
    assin = defaultdict(list)
    for a in csv.DictReader(open(DADOS / "assinaturas.csv")):
        assin[(a["processo"], int(a["seq"]))].append(a)
    corr = json.loads((DADOS / "correcoes_rotulos.json").read_text()) if (DADOS / "correcoes_rotulos.json").exists() else {}
    fichas, falt, anc = [], [], Counter()
    for arq in sorted((DADOS / "fichas").glob("*.jsonl")):
        for ln in arq.read_text().splitlines():
            if not ln.strip():
                continue
            f = json.loads(ln)
            proc = PARTES.get(f.get("processo"), f.get("processo"))
            f["processo"] = proc
            chave = (proc, int(f["seq"]))
            d = docs.get(chave)
            if not d:
                falt.append(chave)
                continue
            txt = next((DADOS / "docs" / proc).glob(f"{int(f['seq']):03d}_*.txt")).read_text(errors="replace")
            anc.update(ancorar(f, txt))
            c = corr.get(f"{proc}#{int(f['seq'])}")
            if c:
                f["atividade_original"], f["atividade"] = f.get("atividade"), c["atividade"]
            a = assin.get(chave, [])
            unid_c = next((unidade_cargo(x["cargo"]) for x in a if unidade_cargo(x["cargo"])), None)
            unid_f = unidade_ficha(f.get("unidade", ""))
            if f.get("autoria") == "externo":
                unid = unid_f if unid_f in ("MUN", "EXT") else "MUN"
            else:
                unid = unid_c or unid_f or "AGERGS-ND"
            data_ass = d["data_primeira_assinatura"]
            data_txt = f.get("data") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(f.get("data") or "")) else None
            piso, teto = esforco(f, int(d["caracteres"]))
            f.update(doc_id=d["doc_id"], nome=d["nome"], paginas=int(d["paginas"]), caracteres=int(d["caracteres"]),
                     baixo_texto=d["baixo_texto"] == "True", unidade_sigla=unid,
                     data_ref=data_ass or data_txt, origem_data="assinatura" if data_ass else ("texto" if data_txt else None),
                     tarefa_modelo=ATIV_TAREFA.get(f.get("atividade")), horas_piso=piso, horas_teto=teto,
                     signatarios=[{"cargo": x["cargo"], "data": x["data"]} for x in a])
            fichas.append(f)
    fichas.sort(key=lambda f: (f["processo"], f["seq"]))
    cobertos = {(f["processo"], f["seq"]) for f in fichas}
    sem_ficha = sorted(k for k in docs if k not in cobertos)
    with open(SAIDA / "fichas_trabalho.jsonl", "w") as fo:
        for f in fichas:
            fo.write(json.dumps(f, ensure_ascii=False) + "\n")
    campos = ["processo", "seq", "doc_id", "nome", "autoria", "unidade_sigla", "data_ref", "origem_data", "atividade",
              "tarefa_modelo", "tarefa", "natureza_trabalho", "complexidade", "horas_piso", "horas_teto",
              "horas_estimadas", "paginas", "caracteres", "baixo_texto", "entregavel"]
    with open(SAIDA / "fichas_trabalho.csv", "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        w.writerows(fichas)
    rel = dict(fichas=len(fichas), documentos=len(docs), sem_ficha=[f"{p}#{s}" for p, s in sem_ficha],
               fichas_sem_documento=[f"{p}#{s}" for p, s in falt], evidencias=dict(anc),
               pct_ancoradas=round(100 * anc["ancorado"] / max(1, sum(anc.values())), 1))
    (SAIDA / "auditoria_ancoragem.json").write_text(json.dumps(rel, ensure_ascii=False, indent=1))
    print(f"fichas: {len(fichas)}/{len(docs)} documentos; evidências ancoradas {rel['pct_ancoradas']}%;"
          f" sem ficha: {len(sem_ficha)}")
    return fichas


# ================================================================ 2. linha do tempo por caso
def etapa_linha(fichas, modelo):
    nomes = {e["id"]: e["nome"] for e in modelo["elementos"] if e["tipo"] == "tarefa"}
    por_caso = defaultdict(list)
    for f in fichas:
        if f["processo"] not in CASOS_EXCLUIDOS:
            por_caso[f["processo"]].append(f)
    casos = {}
    for proc, fs in sorted(por_caso.items()):
        fs.sort(key=lambda f: f["seq"])
        # início = 1ª peça datada, na ordem dos autos, que não é anexo histórico (lei, plano, contrato do prestador)
        proprias = [f["data_ref"] for f in fs if f["data_ref"] and f.get("atividade") not in ANEXO_HISTORICO]
        inicio_proc = proprias[0] if proprias else None
        ultima = None
        for f in fs:  # peça sem data, ou com data só no texto anterior ao início, herda a data corrente (juntada)
            d = f["data_ref"]
            if d and inicio_proc and d < inicio_proc and (f.get("atividade") in ANEXO_HISTORICO or f["origem_data"] == "texto"):
                d = None
            f["_data"] = d or ultima or inicio_proc
            if f["_data"]:
                ultima = max(ultima or f["_data"], f["_data"])
        datados = [f["_data"] for f in fs if f["_data"]]
        ocorr, passagens, unid_ant = [], 0, None
        for f in fs:
            u = f["unidade_sigla"]
            if unid_ant and u != unid_ant:
                passagens += 1
            unid_ant = u
            t = f["tarefa_modelo"]
            if not t:
                continue
            if f.get("atividade") == "comunicacao_prestador" and not any(o["atividade"] == "t11" for o in ocorr):
                t = f["tarefa_modelo"] = "t16"  # antes da assinatura: o prestador é ouvido na instrução
            if ocorr and ocorr[-1]["atividade"] == t:
                o = ocorr[-1]
            else:
                o = dict(atividade=t, nome=nomes.get(t, t), inicio=None, fim=None, pecas=[], unidades=[], horas_piso=0.0,
                         horas_teto=0.0, perdas=[])
                ocorr.append(o)
            o["pecas"].append(f"{f['nome']} ({f['doc_id']})")
            if u not in o["unidades"]:
                o["unidades"].append(u)
            o["horas_piso"] += f["horas_piso"]
            o["horas_teto"] += f["horas_teto"]
            o["perdas"] += [s["tipo"] for s in f.get("sinais_perda") or [] if s.get("ancorado")]
            if f["_data"]:
                o["inicio"] = min(o["inicio"] or f["_data"], f["_data"])
                o["fim"] = max(o["fim"] or f["_data"], f["_data"])
        fim_ant, vistos = (datados[0] if datados else None), Counter()
        ant = None
        for o in ocorr:
            vistos[o["atividade"]] += 1
            o["n"] = vistos[o["atividade"]]
            o["execucao_du"] = du(o["inicio"], o["fim"]) if o["inicio"] else None
            o["espera_antes_du"] = du(fim_ant, o["inicio"]) if (o["inicio"] and fim_ant) else None
            # terceiro só quando o município ou o prestador responde a algo da AGERGS; peça externa depois de outra
            # peça externa (reiteração do pedido) é silêncio da agência
            resp = o["unidades"][0] in TERCEIROS and (ant is None or ant["unidades"][0] not in TERCEIROS)
            o["espera_terceiros_du"] = (o["espera_antes_du"] or 0.0) if resp else 0.0
            ant = o
            o["espera_antes_por_unidade"] = {o["unidades"][0]: o["espera_antes_du"]} if o["espera_antes_du"] else {}
            o["horas_piso"], o["horas_teto"] = round(o["horas_piso"], 2), round(o["horas_teto"], 2)
            if o["fim"]:
                fim_ant = max(fim_ant or o["fim"], o["fim"])
        caminho = [o["atividade"] for o in ocorr]
        retornos = sum(1 for i, t in enumerate(caminho) if t in caminho[:i])
        idx = {t: i for i, t in enumerate(caminho)}
        assin = next((o for o in ocorr if o["atividade"] == "t11"), None)
        casos[proc] = dict(
            processo=proc, inicio=min(datados) if datados else None, fim=max(datados) if datados else None,
            lead_du=du(min(datados), max(datados)) if datados else None,
            lead_ate_assinatura_du=du(min(datados), assin["fim"]) if (assin and assin["fim"] and datados) else None,
            n_documentos=len(fs), n_agergs=sum(f["autoria"] == "AGERGS" for f in fs),
            n_externos=sum(f["autoria"] != "AGERGS" for f in fs),
            n_encaminhamentos=sum(f.get("atividade") == "encaminhamento_interno" for f in fs),
            unidades=sorted({f["unidade_sigla"] for f in fs}), passagens=passagens, retornos=retornos,
            horas_piso=round(sum(f["horas_piso"] for f in fs), 1), horas_teto=round(sum(f["horas_teto"] for f in fs), 1),
            espera_entre_atividades_du=sum(o["espera_antes_du"] or 0 for o in ocorr),
            execucao_atividades_du=sum(o["execucao_du"] or 0 for o in ocorr),
            terceiros_du=sum(o["espera_terceiros_du"] or 0 for o in ocorr),
            inicio_sem_anexos=inicio_proc,
            caminho=caminho, ocorrencias=ocorr)
    (F2 / "casos_CONV.json").write_text(json.dumps(casos, ensure_ascii=False, indent=1))
    print("casos:", len(casos))
    return casos


# ================================================================ 3. fatos e procedimento
def situacao_coorte(n):
    """procedimento: ≥ 5 casos e auditoria às cegas ≥ 85% nas substantivas; indicativo: ≥ 5 casos; senão estudo de caso."""
    arq = SAIDA / "auditoria" / "auditoria_classificador_CONV.json"
    conc = json.loads(arq.read_text())["concordancia_tarefa_substantivas"] if arq.exists() else 0
    return "estudo_de_caso" if n < 5 else ("procedimento" if conc >= 85 else "indicativo")

def etapa_fatos(casos, modelo, narr):
    tarefas = [e["id"] for e in modelo["elementos"] if e["tipo"] == "tarefa"]
    fatos = []

    def add(fid, valor, unidade, descricao, definicao=""):
        if valor is None:
            return
        fatos.append(dict(id=fid, valor=valor, unidade=unidade, descricao=descricao, definicao=definicao))

    def add_est(prefixo, vals, unidade, descricao):
        e = estat(vals)
        if e:
            for k, v in e.items():
                add(f"{prefixo}.{k}", v, "obs" if k == "n" else unidade, f"{descricao} — {k}")

    n = len(casos)
    add("coorte.casos", n, "casos", "Processos de celebração na coorte")
    for proc, c in casos.items():
        p = f"caso.{proc}"
        for k, u in (("lead_du", "du"), ("lead_ate_assinatura_du", "du"), ("n_documentos", "docs"), ("n_agergs", "docs"),
                     ("n_externos", "docs"), ("n_encaminhamentos", "docs"), ("passagens", "passagens"),
                     ("retornos", "retornos"), ("horas_piso", "h"), ("horas_teto", "h"),
                     ("espera_entre_atividades_du", "du"), ("execucao_atividades_du", "du"), ("terceiros_du", "du")):
            add(f"{p}.{k.replace('_du', '')}", c[k], u, f"{proc}: {k}")
        add(f"{p}.inicio", c["inicio"], "data", f"{proc}: primeira peça datada")
        add(f"{p}.fim", c["fim"], "data", f"{proc}: última peça datada")
        for o in c["ocorrencias"]:
            q = f"{p}.{o['atividade']}.{o['n']}"
            add(f"{q}.espera_antes", o["espera_antes_du"], "du", f"{proc}: {o['nome']} — espera antes (ocorrência {o['n']})")
            add(f"{q}.execucao", o["execucao_du"], "du", f"{proc}: {o['nome']} — execução (ocorrência {o['n']})")
            add(f"{q}.inicio", o["inicio"], "data", f"{proc}: {o['nome']} — início")
    # por caso (coorte)
    for k, u in (("lead_du", "du"), ("lead_ate_assinatura_du", "du"), ("espera_entre_atividades_du", "du"),
                 ("execucao_atividades_du", "du"), ("terceiros_du", "du"), ("horas_piso", "h"), ("horas_teto", "h"),
                 ("n_documentos", "docs"), ("n_encaminhamentos", "docs"), ("passagens", "passagens"),
                 ("retornos", "retornos")):
        add_est(f"coorte.caso.{k.replace('_du', '')}", [c[k] for c in casos.values() if c[k] is not None], u,
                f"Por caso: {k}")
    # por tarefa
    proc_tar = {}
    for t in tarefas:
        oc = [(proc, o) for proc, c in casos.items() for o in c["ocorrencias"] if o["atividade"] == t]
        cs = {proc for proc, _ in oc}
        laco = {proc for proc, o in oc if o["n"] > 1}
        add(f"coorte.{t}.casos", len(cs), "casos", f"{t}: casos em que ocorre")
        add(f"coorte.{t}.pct_casos", round(100 * len(cs) / n, 1) if n else None, "%", f"{t}: % dos casos")
        add(f"coorte.{t}.casos_com_laco", len(laco), "casos", f"{t}: casos com mais de uma ocorrência")
        add(f"coorte.{t}.ocorrencias", len(oc), "ocorrências", f"{t}: ocorrências")
        add_est(f"coorte.{t}.espera_antes", [o["espera_antes_du"] for _, o in oc if o["espera_antes_du"] is not None], "du",
                f"{t}: espera antes")
        add_est(f"coorte.{t}.execucao", [o["execucao_du"] for _, o in oc if o["execucao_du"] is not None], "du",
                f"{t}: execução")
        add_est(f"coorte.{t}.horas_piso", [o["horas_piso"] for _, o in oc], "h", f"{t}: horas piso por ocorrência")
        add_est(f"coorte.{t}.horas_teto", [o["horas_teto"] for _, o in oc], "h", f"{t}: horas teto por ocorrência")
        perdas = Counter()
        for proc, o in oc:
            for s in set(o["perdas"]):
                perdas[(s, proc)] = 1
        for s in sorted({s for s, _ in perdas}):
            add(f"coorte.{t}.perda.{s}", sum(1 for (x, _) in perdas if x == s), "casos", f"{t}: casos com sinal {s}")
        proc_tar[t] = dict(casos=len(cs), pct_casos=round(100 * len(cs) / n, 1) if n else 0, ocorrencias=len(oc),
                           casos_com_laco=len(laco),
                           espera_antes=estat([o["espera_antes_du"] for _, o in oc if o["espera_antes_du"] is not None]),
                           execucao=estat([o["execucao_du"] for _, o in oc if o["execucao_du"] is not None]),
                           horas_piso=estat([o["horas_piso"] for _, o in oc]),
                           horas_teto=estat([o["horas_teto"] for _, o in oc]))
    # onde está a espera: soma da espera antes de cada tarefa em toda a coorte e % do total
    tot_esp = sum(o["espera_antes_du"] or 0 for c in casos.values() for o in c["ocorrencias"])
    for t in tarefas:
        soma = sum(o["espera_antes_du"] or 0 for c in casos.values() for o in c["ocorrencias"] if o["atividade"] == t)
        add(f"coorte.{t}.espera_soma", soma, "du", f"{t}: soma da espera antes em todos os casos")
        add(f"coorte.{t}.pct_espera_total", round(100 * soma / tot_esp, 1) if tot_esp else None, "%",
            f"{t}: % da espera total da coorte")
    add("coorte.espera_total", tot_esp, "du", "Soma da espera antes de todas as ocorrências da coorte")
    terc = sum(o["espera_terceiros_du"] or 0 for c in casos.values() for o in c["ocorrencias"])
    add("coorte.pct_espera_terceiros", round(100 * terc / tot_esp, 1) if tot_esp else None, "%",
        "% da espera total que é tempo de resposta do município ou do prestador")
    soma_lead = sum(c["lead_du"] or 0 for c in casos.values())
    soma_exec = sum(c["execucao_atividades_du"] for c in casos.values())
    add("coorte.pct_execucao_no_lead", round(100 * soma_exec / soma_lead, 1) if soma_lead else None, "%",
        "% do lead time somado da coorte coberto por execução de atividade (dias com peça produzida)")
    hrs = sum(c["horas_teto"] for c in casos.values())
    add("coorte.pce_teto", round(100 * (hrs / 8) / soma_lead, 1) if soma_lead else None, "%",
        "Eficiência do ciclo (PCE) no teto: horas-teto/8 h por du ÷ lead somado")
    # transições e caminhos
    trans = Counter()
    saidas = Counter()
    for c in casos.values():
        for a, b in zip(c["caminho"], c["caminho"][1:]):
            trans[(a, b)] += 1
            saidas[a] += 1
    for (a, b), k in sorted(trans.items()):
        add(f"coorte.transicao.{a}.{b}", k, "passagens", f"Transição {a}→{b}")
        add(f"coorte.transicao.{a}.{b}.pct", round(100 * k / saidas[a], 1), "%", f"% das saídas de {a} que vão a {b}")
    caminhos = Counter(" > ".join(c["caminho"]) for c in casos.values())
    add("coorte.n_caminhos", len(caminhos), "caminhos", "Caminhos distintos")
    # posse (espera antes atribuída à unidade que age depois)
    posse = defaultdict(list)
    for c in casos.values():
        acc = Counter()
        for o in c["ocorrencias"]:
            for u, v in o["espera_antes_por_unidade"].items():
                acc[u] += v or 0
        for u, v in acc.items():
            posse[u].append(v)
    for u, vals in sorted(posse.items()):
        add_est(f"coorte.posse.{u}", vals, "du", f"Espera antes atribuída à unidade {u}, por caso em que aparece")
    # situação final e instrumento (das narrativas)
    sit = Counter(v.get("situacao_final") for v in narr.values())
    for s, k in sorted(sit.items(), key=lambda x: str(x[0])):
        add(f"coorte.situacao.{s}", k, "casos", f"Casos com situação final {s}")
    inst = defaultdict(list)
    for proc, c in casos.items():
        inst[narr.get(proc, {}).get("instrumento", "indeterminado")].append(proc)
    for i, procs in sorted(inst.items()):
        add(f"coorte.instrumento.{i}.casos", len(procs), "casos", f"Casos do instrumento {i}")
        add_est(f"coorte.instrumento.{i}.lead", [casos[p]["lead_du"] for p in procs if casos[p]["lead_du"] is not None],
                "du", f"Lead time ({i})")
        add_est(f"coorte.instrumento.{i}.lead_ate_assinatura",
                [casos[p]["lead_ate_assinatura_du"] for p in procs if casos[p]["lead_ate_assinatura_du"] is not None],
                "du", f"Lead até assinatura ({i})")
    fatos.sort(key=lambda x: x["id"])
    sha = hashlib.sha256(json.dumps(fatos, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]
    out = dict(codigo="CONV", definicoes=dict(
        lead="dias úteis da primeira à última peça datada do processo (datas de assinatura; peça externa: data do texto)",
        lead_ate_assinatura="dias úteis da primeira peça datada à última peça da assinatura do instrumento (t11)",
        execucao="dias úteis da primeira à última peça da ocorrência",
        espera_antes="dias úteis entre o fim da ocorrência anterior e o início desta; atribuída à unidade que age",
        terceiros="espera antes de tarefa do município (t1, t3): tempo de resposta de terceiro, protegido",
        horas="horas estimadas das peças próprias da AGERGS (piso = base + conferência; teto = laudas autorais × "
              "coeficiente da complexidade + leitura dos insumos). HIPÓTESE até a calibração com servidores",
        limite="sem andamentos do SEI: tempo em fila dentro de cada unidade não é observável; a espera é inferida "
               "pelas datas das peças"), fatos=fatos, sha=sha)
    (BPMN / "fatos_CONV.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    # formato lido por metodologia-repo/scripts/gerar_bpmn.py (metricas_da_coorte, probabilidades_ramos)
    ativ = {}
    for t, a in proc_tar.items():
        perd = [dict(item=f["id"].rsplit(".", 1)[1], casos=f["valor"]) for f in fatos if f["id"].startswith(f"coorte.{t}.perda.")]
        ativ[t] = dict(casos=a["casos"], pct_casos=a["pct_casos"], espera_antes_du=a["espera_antes"],
                       horas_piso=a["horas_piso"], sinais_perda=perd)
    trans_d = defaultdict(list)
    for (a, b), k in sorted(trans.items()):
        trans_d[a].append(dict(para=b, n=k))
    proc_json = dict(codigo="CONV", casos=n, situacao=situacao_coorte(n), tarefas=proc_tar, atividades=ativ, transicoes_por_origem=trans_d,
                     transicoes=[dict(de=a, para=b, n=k, pct=round(100 * k / saidas[a], 1)) for (a, b), k in sorted(trans.items())],
                     caminhos=[dict(caminho=k, casos=v) for k, v in caminhos.most_common()], fatos_sha=sha)
    (F2 / "procedimento_CONV.json").write_text(json.dumps(proc_json, ensure_ascii=False, indent=1))
    print(f"fatos: {len(fatos)} (sha {sha}); caminhos distintos: {len(caminhos)} em {n} casos")
    return out


# ================================================================ 4. fase 0: indicadores e planilha
def etapa_fase0(casos, narr, fichas):
    linhas = []
    for proc, c in casos.items():
        nv = narr.get(proc, {})
        linhas.append(dict(processo=proc, numero_sei=nv.get("numero_sei", ""), municipio=nv.get("municipio", ""),
                           instrumento=nv.get("instrumento", ""), servico=nv.get("servico", ""),
                           situacao_final=nv.get("situacao_final", ""), inicio=c["inicio"], fim=c["fim"],
                           lead_du=c["lead_du"], lead_ate_assinatura_du=c["lead_ate_assinatura_du"],
                           n_documentos=c["n_documentos"], n_agergs=c["n_agergs"], n_externos=c["n_externos"],
                           n_encaminhamentos=c["n_encaminhamentos"], passagens=c["passagens"], retornos=c["retornos"],
                           unidades=" ".join(c["unidades"]), horas_piso=c["horas_piso"], horas_teto=c["horas_teto"],
                           terceiros_du=c["terceiros_du"], caminho=" > ".join(c["caminho"])))
    with open(SAIDA / "processos_indicadores.csv", "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    est = []
    for proc, c in casos.items():
        for o in c["ocorrencias"]:
            est.append(dict(processo=proc, atividade=o["atividade"], ocorrencia=o["n"], nome=o["nome"], inicio=o["inicio"],
                            fim=o["fim"], execucao_du=o["execucao_du"], espera_antes_du=o["espera_antes_du"],
                            espera_terceiros_du=o["espera_terceiros_du"], unidades=" ".join(o["unidades"]),
                            horas_piso=o["horas_piso"], horas_teto=o["horas_teto"], n_pecas=len(o["pecas"])))
    with open(SAIDA / "estadias.csv", "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(est[0]))
        w.writeheader()
        w.writerows(est)
    try:
        import pandas as pd
        with pd.ExcelWriter(SAIDA / "Mapeamento_AGERGS_Celebracao.xlsx") as xw:
            pd.DataFrame(linhas).to_excel(xw, sheet_name="Processos", index=False)
            pd.DataFrame(est).to_excel(xw, sheet_name="Atividades por caso", index=False)
            pd.read_csv(SAIDA / "fichas_trabalho.csv").to_excel(xw, sheet_name="Fichas por peça", index=False)
            pd.read_csv(DADOS / "documentos.csv").to_excel(xw, sheet_name="Documentos", index=False)
    except Exception as e:  # planilha é conveniência; CSVs são a saída canônica
        print("aviso: planilha não gerada:", e)
    print("fase 0: processos_indicadores.csv, estadias.csv, Mapeamento_AGERGS_Celebracao.xlsx")


def main():
    modelo = json.loads((BPMN / "modelo_CONV.json").read_text())
    narr = {}
    for arq in sorted((DADOS / "narrativas").glob("*.json")):
        v = json.loads(arq.read_text())
        proc = PARTES.get(arq.stem, arq.stem)
        if proc in narr:  # partes de um mesmo processo: a última parte define a situação final
            narr[proc] = {**narr[proc], **{k: x for k, x in v.items() if x}}
        else:
            narr[proc] = v
    fichas = etapa_fichas()
    casos = etapa_linha(fichas, modelo)
    etapa_fatos(casos, modelo, narr)
    etapa_fase0(casos, narr, fichas)


if __name__ == "__main__":
    main()
