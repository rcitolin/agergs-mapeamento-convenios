"""Figuras e números do relatório final (Word). Lê só as saídas do pipeline; grava relatorio/fig/*.png e
relatorio/dados_relatorio.json, que o gerador do .docx (relatorio/gerar_docx.js) consome. Nenhum número é digitado."""
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
S = RAIZ / "saida"
OUT = RAIZ / "relatorio"
FIG = OUT / "fig"
FIG.mkdir(parents=True, exist_ok=True)
AZUL, VERDE, AMBAR, CINZA, VERM, CLARO = "#1F4E79", "#2E7D6B", "#C98A1B", "#8A939C", "#B23A2E", "#DCE6F0"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.edgecolor": "#9AA3AB", "axes.labelcolor": "#333",
                     "xtick.color": "#444", "ytick.color": "#333"})

j = lambda p: json.loads((S / p).read_text())  # noqa: E731
F = {f["id"]: f["valor"] for f in j("bpmn/fatos_CONV.json")["fatos"]}
conf = j("fase3/conformidade_CONV.json")["requisitos"]
normas = {r["id"]: r for r in j("fase3/normas_CONV.json")["requisitos"]}
res = j("fase3/resultado_tobe_CONV.json")
modelo = j("bpmn/modelo_CONV.json")
nome_t = {e["id"]: e["nome"] for e in modelo["elementos"] if e["tipo"] == "tarefa"}
proc = list(csv.DictReader(open(S / "processos_indicadores.csv")))
NOME_MUN = {"Mapituba": "Mampituba", "Vila_nova_do_Sul": "Vila Nova do Sul"}
INST = {"convenio_delegacao": "Convênio", "contrato_prestacao_servicos_regulacao": "Contrato", "aditivo": "Aditivo"}
SIT = {"assinado_e_publicado": "Assinado e publicado", "assinado_sem_publicacao_no_processo": "Assinado, sem publicação nos autos",
       "aguardando_municipio": "Aguardando o município", "aguardando_agergs": "Aguardando a AGERGS"}


def mun(p):
    return NOME_MUN.get(p["processo"], (p["municipio"] or p["processo"].replace("_", " ")).replace("/RS", ""))


def sei(n):
    m = __import__("re").fullmatch(r"(\d{6})_(\d{2}\.\d{2})_(\d{2})_(\d)", n)
    return f"{m[1]}-{m[2]}/{m[3]}-{m[4]}" if m else n


# ---------------------------------------------------------------- 1. lead por caso
ps = sorted(proc, key=lambda p: float(p["lead_du"] or 0))
cor = {"Convênio": AZUL, "Contrato": AMBAR, "Aditivo": VERDE}
fig, ax = plt.subplots(figsize=(7.2, 5.0))
ax.barh([mun(p) for p in ps], [float(p["lead_du"]) for p in ps], color=[cor[INST[p["instrumento"]]] for p in ps], height=0.65)
med = F["coorte.caso.lead.mediana"]
ax.axvline(med, color=VERM, ls="--", lw=1.2)
ax.text(med + 4, -0.9, f"mediana: {med:g} du".replace(".", ","), color=VERM, fontsize=9)
for i, p in enumerate(ps):
    ax.text(float(p["lead_du"]) + 3, i, f"{float(p['lead_du']):g}".replace(".", ","), va="center", fontsize=8, color="#333")
ax.set_xlabel("Dias úteis da primeira à última peça do processo")
for k, c in cor.items():
    ax.barh([], [], color=c, label=k)
ax.legend(frameon=False, loc="lower right")
ax.set_ylim(-1.3, len(ps) - 0.4)
fig.tight_layout()
fig.savefig(FIG / "lead_casos.png", dpi=200)
plt.close(fig)

# ---------------------------------------------------------------- 2. onde está a espera
esp = sorted(((F.get(f"coorte.{t}.pct_espera_total", 0), t) for t in nome_t), reverse=True)[:8]
fig, ax = plt.subplots(figsize=(7.2, 3.4))
lab = {"t1": "Pedido do município sem resposta (reiteração)", "t13": "Comunicação ao prestador e às unidades",
       "t12": "Publicação do extrato", "t5": "Elaboração ou ajuste da minuta", "t6": "Análise jurídica",
       "t11": "Assinatura do instrumento", "t3": "Complementação de documentos", "t16": "Oitiva do prestador",
       "t15": "Arquivamento", "t10": "Envio da minuta ao município"}
ys = [lab.get(t, nome_t[t]) for _, t in esp][::-1]
xs = [v for v, _ in esp][::-1]
ax.barh(ys, xs, color=[AZUL if v >= 10 else CINZA for v in xs], height=0.6)
for i, v in enumerate(xs):
    ax.text(v + 0.3, i, f"{v:g}%".replace(".", ","), va="center", fontsize=9)
ax.set_xlabel("% da espera total que ocorre antes de cada etapa")
fig.tight_layout()
fig.savefig(FIG / "espera.png", dpi=200)
plt.close(fig)

# ---------------------------------------------------------------- 3. conformidade
reqs = [k for k in ("R-CONV-01", "R-CONV-03", "R-CONV-04", "R-CONV-05", "R-CONV-06", "R-CONV-08", "R-CONV-09", "R-CONV-10")]
curto = {"R-CONV-01": "Instrumento assinado nos autos", "R-CONV-03": "Parecer jurídico antes da assinatura",
         "R-CONV-04": "Autorização formal antes da assinatura", "R-CONV-05": "Extrato publicado nos autos",
         "R-CONV-06": "Publicação em até 10 du da assinatura", "R-CONV-08": "Inexigibilidade nos autos (contratos)",
         "R-CONV-09": "Decisão em até 30 dias da instrução", "R-CONV-10": "Atos internos em até 5 dias"}
vals = [conf[k]["pct_conforme"] for k in reqs]
fig, ax = plt.subplots(figsize=(7.2, 3.6))
cores = [VERDE if v >= 75 else (AMBAR if v >= 40 else VERM) for v in vals]
ax.barh([curto[k] for k in reqs][::-1], vals[::-1], color=cores[::-1], height=0.6)
for i, (v, k) in enumerate(zip(vals[::-1], reqs[::-1])):
    ax.text(v + 1, i, f"{v:g}%  ({conf[k]['casos_aplicaveis']} casos)".replace(".", ","), va="center", fontsize=8.5)
ax.set_xlim(0, 118)
ax.set_xlabel("% dos casos aplicáveis em conformidade")
fig.tight_layout()
fig.savefig(FIG / "conformidade.png", dpi=200)
plt.close(fig)

# ---------------------------------------------------------------- 4. TO-BE simulado
cen = ("conservador", "esperado", "otimista")
fig, ax = plt.subplots(figsize=(7.2, 3.3))
base = res["linha_base"]["lead"]["mediana"]
ax.bar([0], [base], color=CINZA, width=0.6)
ax.text(0, base + 1.5, f"{base:g}".replace(".", ","), ha="center", fontsize=9)
cc = {"conservador": "#9DB7CF", "esperado": AZUL, "otimista": VERDE}
for f in (1, 2, 3):
    for i, c in enumerate(cen):
        v = res["fases"][str(f)][c]["lead"]["mediana"]
        x = f + (i - 1) * 0.26
        ax.bar([x], [v], width=0.24, color=cc[c], label=c.capitalize() if f == 1 else None)
        ax.text(x, v + 1.5, f"{v:g}".replace(".", ","), ha="center", fontsize=7.5)
ax.set_xticks([0, 1, 2, 3], ["Hoje", "Fase 1\nfluxo", "Fase 2\nregras e dados", "Fase 3\nIA assistida"])
ax.set_ylabel("Lead time mediano (du)")
ax.legend(frameon=False, ncol=3, loc="upper right")
ax.set_ylim(0, base * 1.18)
fig.tight_layout()
fig.savefig(FIG / "tobe.png", dpi=200)
plt.close(fig)


# ---------------------------------------------------------------- 5. fluxos (raias)
def raias(arq, lanes, nos, arestas, largura=11.0, titulo=None, cols=None):
    """lanes: [(id, nome)]; nos: {id: (lane, col, texto, tipo)}; tipo: tarefa|decisao|evento; arestas: [(a, b, estilo)]."""
    ncol = cols or (max(c for _, c, _, _ in nos.values()) + 1)
    lh = 1.0
    fig, ax = plt.subplots(figsize=(largura, 0.82 * len(lanes) + 0.3))
    W = ncol * 1.55 + 1.6
    for i, (lid, ln) in enumerate(lanes):
        y = (len(lanes) - 1 - i) * lh
        ax.add_patch(plt.Rectangle((0, y), W, lh, fc="#F4F7FA" if i % 2 == 0 else "white", ec="#C9D3DC", lw=0.8, zorder=0))
        ax.text(0.08, y + lh / 2, ln, va="center", fontsize=7.6, color=AZUL, fontweight="bold", wrap=True)
    pos = {}
    li = {lid: i for i, (lid, _) in enumerate(lanes)}
    for n, (lane, col, txt, tipo) in nos.items():
        x = 1.6 + col * 1.55 + 0.72
        y = (len(lanes) - 1 - li[lane]) * lh + lh / 2
        pos[n] = (x, y)
        if tipo == "tarefa":
            ax.add_patch(FancyBboxPatch((x - 0.66, y - 0.33), 1.32, 0.66, boxstyle="round,pad=0.02,rounding_size=0.08",
                                        fc="white", ec=AZUL, lw=1.1, zorder=2))
            ax.text(x, y, txt, ha="center", va="center", fontsize=6.2, zorder=3)
        elif tipo == "decisao":
            ax.add_patch(plt.Polygon([(x, y + 0.36), (x + 0.5, y), (x, y - 0.36), (x - 0.5, y)], fc="#FFF6E5", ec=AMBAR, lw=1.1, zorder=2))
            ax.text(x, y, txt, ha="center", va="center", fontsize=5.8, zorder=3)
        else:
            ax.add_patch(plt.Circle((x, y), 0.2, fc="#EAF4F1" if tipo == "inicio" else "#F3E1DE",
                                    ec=VERDE if tipo == "inicio" else VERM, lw=1.4))
            ax.text(x, y - 0.33, txt, ha="center", va="top", fontsize=5.8)
    HW = {"tarefa": (0.66, 0.33), "decisao": (0.5, 0.36), "inicio": (0.2, 0.2), "fim": (0.2, 0.2)}
    for a, b, est in arestas:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        (w1, h1), (w2, h2) = HW[nos[a][3]], HW[nos[b][3]]
        if est == "laco":  # retorno: sai por baixo de a e entra por baixo de b
            p1, p2, cs = (x1, y1 - h1), (x2, y2 - h2), "arc3,rad=-0.45" if x2 < x1 else "arc3,rad=0.45"
            if abs(x1 - x2) < 0.1:
                p1, p2, cs = (x1 + w1 * 0.6, y1 + (h1 if y2 > y1 else -h1)), (x2 + w2 * 0.6, y2 + (-h2 if y2 > y1 else h2)), "arc3,rad=-0.3"
        elif abs(x2 - x1) < 0.1:
            sg = 1 if y2 > y1 else -1
            p1, p2, cs = (x1, y1 + sg * h1), (x2, y2 - sg * h2), "arc3,rad=0"
        elif x2 > x1:
            p1, p2, cs = (x1 + w1, y1), (x2 - w2, y2), "arc3,rad=0"
        else:
            p1, p2, cs = (x1 - w1, y1), (x2 + w2, y2), "arc3,rad=0"
        laco = est == "laco"
        ax.add_patch(FancyArrowPatch(p1, p2, connectionstyle=cs, arrowstyle="-|>", mutation_scale=8,
                                     lw=1.0, color=VERM if laco else "#55606B", ls="--" if laco else "-",
                                     shrinkA=1, shrinkB=1, zorder=1.5))
    ax.set_xlim(0, W)
    ax.set_ylim(-0.05, len(lanes) * lh + 0.05)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(FIG / arq, dpi=220)
    plt.close(fig)


pc = lambda t: f"{round(F.get(f'coorte.{t}.pct_casos', 0))}% dos casos"  # noqa: E731
raias("fluxo_asis.png",
      [("MUN", "Município /\nprestador"), ("GP", "Gabinete da\nPresidência"), ("DG", "Diretoria-Geral\ne apoio"),
       ("DAJ", "Jurídico (DAJ)\ne PSE"), ("CS", "Conselho\nSuperior")],
      {"s": ("MUN", 0, "Interesse\ndo município", "inicio"),
       "t1": ("MUN", 1, f"Pedir delegação\n({pc('t1')})", "tarefa"),
       "t2": ("GP", 2, f"Autuar e\ndistribuir\n({pc('t2')})", "tarefa"),
       "t6": ("DAJ", 3, f"Analisar\njuridicamente\n({pc('t6')})", "tarefa"),
       "t3": ("MUN", 3, f"Complementar\ndocumentos\n({pc('t3')})", "tarefa"),
       "t5": ("DAJ", 4, f"Elaborar ou\najustar minuta\n({pc('t5')})", "tarefa"),
       "t8": ("CS", 5, f"Deliberar\n({pc('t8')})", "tarefa"),
       "t10": ("GP", 5, f"Enviar minuta\nao município\n({pc('t10')})", "tarefa"),
       "t11": ("GP", 6, f"Assinar\n({pc('t11')})", "tarefa"),
       "t12": ("DG", 7, f"Publicar\nextrato\n({pc('t12')})", "tarefa"),
       "t13": ("DG", 8, f"Comunicar\nprestador e\nunidades\n({pc('t13')})", "tarefa"),
       "f": ("GP", 9, f"Arquivar\n({pc('t15')})", "fim")},
      [("s", "t1", ""), ("t1", "t2", ""), ("t2", "t6", ""), ("t6", "t3", "laco"), ("t3", "t6", "laco"), ("t6", "t5", ""),
       ("t5", "t6", "laco"), ("t5", "t8", ""), ("t5", "t10", ""), ("t10", "t5", "laco"), ("t8", "t11", ""), ("t10", "t11", ""),
       ("t11", "t12", ""), ("t12", "t13", ""), ("t13", "f", "")])
raias("fluxo_tobe.png",
      [("MUN", "Município /\nprestador"), ("DAI", "Dono do processo\n(DAI)"), ("TEC", "Diretoria\ntécnica"),
       ("JUR", "Jurídico e PSE"), ("GP", "Presidência e\nConselho"), ("DG", "Diretoria-Geral\ne apoio")],
      {"s": ("MUN", 0, "Interesse\ndo município", "inicio"),
       "t1": ("MUN", 1, "Formulário de\nadesão + kit de\ndocumentos", "tarefa"),
       "t2": ("DAI", 2, "Abrir processo\ne conferir\nchecklist", "tarefa"),
       "g1": ("DAI", 3, "Completo?", "decisao"),
       "t3": ("MUN", 3, "Diligência\núnica com\nprazo", "tarefa"),
       "t4": ("TEC", 4, "Análise técnica\n(em paralelo)", "tarefa"),
       "t5": ("DAI", 4, "Preencher a\nminuta padrão", "tarefa"),
       "t16": ("MUN", 4, "Oitiva do\nprestador com\nprazo fixo", "tarefa"),
       "t6": ("JUR", 5, "Conferir\nenquadramento\n(parecer\nreferencial)", "tarefa"),
       "g2": ("JUR", 6, "Desvio?", "decisao"),
       "t8": ("GP", 6, "Deliberar só\nos desvios", "tarefa"),
       "t9": ("GP", 7, "Autorizar e\njustificar\nnos autos", "tarefa"),
       "t11": ("GP", 8, "Assinatura\neletrônica\nno SEI", "tarefa"),
       "t12": ("DG", 9, "Publicar em\naté 10 du +\ncomunicado\núnico", "tarefa"),
       "f": ("DAI", 10, "Encerrar e\ncadastrar", "fim")},
      [("s", "t1", ""), ("t1", "t2", ""), ("t2", "g1", ""), ("g1", "t3", ""), ("t3", "t2", "laco"), ("g1", "t4", ""),
       ("g1", "t5", ""), ("g1", "t16", ""), ("t4", "t6", ""), ("t5", "t6", ""), ("t16", "t6", ""), ("t6", "g2", ""),
       ("g2", "t8", ""), ("g2", "t9", ""), ("t8", "t9", ""), ("t9", "t11", ""), ("t11", "t12", ""), ("t12", "f", "")], largura=11.5)

# ---------------------------------------------------------------- números para o texto
fmt = lambda v: (f"{float(v):g}".replace(".", ",")) if isinstance(v, (int, float)) else v  # noqa: E731
D = {k: fmt(v) for k, v in F.items() if k.startswith("coorte.") and not k.startswith("coorte.transicao")}
D.update({f"conf.{k}": fmt(v["pct_conforme"]) for k, v in conf.items() if v["pct_conforme"] is not None})
D.update({f"conf.{k}.n": str(v["casos_aplicaveis"]) for k, v in conf.items()})
for f in ("1", "2", "3"):
    for c in cen:
        r = res["fases"][f][c]
        D[f"tobe.{f}.{c}.lead"] = fmt(r["lead"]["mediana"])
        D[f"tobe.{f}.{c}.ganho"] = fmt(r["ganho_pct"]["lead_mediano"])
        D[f"tobe.{f}.{c}.horas"] = fmt(r["horas_teto"]["mediana"])
        for k, v in r["conformidade_temporal"].items():
            D[f"tobe.{f}.{c}.{k}"] = fmt(v)
D["espera.pos_assinatura"] = fmt(round(F["coorte.t13.pct_espera_total"] + F["coorte.t12.pct_espera_total"], 1))
D["base.lead"] = fmt(res["linha_base"]["lead"]["mediana"])
D["base.horas"] = fmt(res["linha_base"]["horas_teto"]["mediana"])
aud = j("auditoria/auditoria_classificador_CONV.json")
D["aud.pecas"], D["aud.subst"] = str(aud["pecas"]), fmt(aud["concordancia_tarefa_substantivas"])
mz = j("fase4/matriz_automacao_CONV.json")
D["prio.nota"] = fmt(mz["nota_composta"])
D["prio.retorno"] = f"{mz['cenarios']['esperado']['retorno_ano']:,}".replace(",", ".")
D["prio.construcao"] = f"{mz['cenarios']['esperado']['custo_construcao_isolado']:,}".replace(",", ".")
docs = list(csv.DictReader(open(RAIZ / "dados" / "documentos.csv")))
D["base.documentos"] = str(len(docs))
D["base.pdfs"] = str(len({d["processo"] for d in docs}))
D["casos"] = [dict(municipio=mun(p), sei=sei(p["numero_sei"]), instrumento=INST[p["instrumento"]], ano=p["inicio"][:4],
                   lead=fmt(float(p["lead_du"])), docs=p["n_documentos"], situacao=SIT.get(p["situacao_final"], p["situacao_final"]))
              for p in sorted(proc, key=lambda p: p["inicio"])]
D["melhorias"] = j("fase3/melhorias_CONV.json")["melhorias"]
D["indicadores"] = [dict(nome=i["nome"], base=fmt(i["linha_base"]["valor"]), unidade=i["linha_base"]["unidade"],
                         metas={str(m["fase"]): fmt(m["valor"]) for m in i["metas"]}, resp=i["responsavel"])
                    for i in j("fase3/controles_CONV.json")["indicadores"]]
D["sens"] = res["sensibilidade"]["sem_cada_melhoria"]
(OUT / "dados_relatorio.json").write_text(json.dumps(D, ensure_ascii=False, indent=1))
print("figuras:", sorted(p.name for p in FIG.glob("*.png")))
