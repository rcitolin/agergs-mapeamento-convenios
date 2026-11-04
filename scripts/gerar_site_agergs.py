"""Gera docs/site/index.html: site navegável do mapeamento (offline, um arquivo só).
Todos os números vêm das saídas (JSON/CSV); o script não digita nenhum valor. Uso: python3 scripts/gerar_site_agergs.py"""
from __future__ import annotations

import csv
import html
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
S = RAIZ / "saida"
OUT = RAIZ / "docs" / "site"


def j(p):
    return json.loads((S / p).read_text())


def e(x):
    return html.escape("" if x is None else str(x))


def num(v, casas=1):
    if v is None or v == "":
        return "—"
    try:
        f = float(v)
    except (TypeError, ValueError):
        return e(v)
    s = f"{f:,.{casas}f}" if f != int(f) or casas == 0 else f"{int(f):,}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def tabela(cab, linhas, cls=""):
    th = "".join(f"<th>{e(c)}</th>" for c in cab)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in l) + "</tr>" for l in linhas)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def card(rotulo, valor, sub=""):
    return f'<div class="card"><div class="v">{valor}</div><div class="r">{e(rotulo)}</div><div class="s">{e(sub)}</div></div>'


def main():
    F = {f["id"]: f["valor"] for f in j("bpmn/fatos_CONV.json")["fatos"]}
    proc = j("fase2/procedimento_CONV.json")
    modelo = j("bpmn/modelo_CONV.json")
    av = j("bpmn/avaliacao_CONV.json")
    conf = j("fase3/conformidade_CONV.json")["requisitos"]
    normas = j("fase3/normas_CONV.json")
    mel = j("fase3/melhorias_CONV.json")["melhorias"]
    res = j("fase3/resultado_tobe_CONV.json")
    ctl = j("fase3/controles_CONV.json")
    mz = j("fase4/matriz_automacao_CONV.json")
    lb = j("fase3/linha_base_CONV.json")
    inds = list(csv.DictReader(open(S / "processos_indicadores.csv")))
    conf_csv = list(csv.DictReader(open(S / "fase3" / "conformidade_CONV.csv")))
    nomes = {x["id"]: x["nome"] for x in modelo["elementos"] if x["tipo"] == "tarefa"}
    raia = {x["id"]: x["raia"] for x in modelo["elementos"]}
    lbl = lambda s: e(str(s).replace("_", " "))  # noqa: E731

    # ---------------- visão geral
    sec = {}
    lead = lb["por_caso"]["lead_du"]
    f3 = res["fases"]["3"]["esperado"]["lead"]["mediana"]
    sec["geral"] = f"""
<h2>Visão geral</h2>
<p class="lead">{e(av['sintese'])}</p>
<div class="cards">
{card('processos de celebração analisados', num(F['coorte.casos'], 0), 'situação: ' + lbl(proc['situacao']))}
{card('lead time mediano por caso (du)', num(lead['mediana']), 'q1 ' + num(lead['q1']) + ' · q3 ' + num(lead['q3']) + ' · máx. ' + num(lead['max']))}
{card('do lead time coberto por execução', num(F['coorte.pct_execucao_no_lead']) + '%', 'o restante é espera entre peças')}
{card('eficiência do ciclo (horas no teto)', num(F['coorte.pce_teto']) + '%', 'horas de trabalho ÷ tempo total')}
{card('caminhos distintos', num(F['coorte.n_caminhos'], 0), 'em ' + num(F['coorte.casos'], 0) + ' casos')}
{card('lead mediano projetado (TO-BE, fase 3, esperado)', num(f3), 'dias úteis · base ' + num(lead['mediana']))}
</div>
<h3>Leitura das métricas</h3><p>{e(av['leitura_metricas'])}</p>
<h3>Gargalo</h3><p><b>{e(av['gargalo']['onde'])}</b> {e(av['gargalo']['evidencia'])}</p>
<h3>Situação final dos processos</h3>
{tabela(['Situação', 'Casos'], [[lbl(k.split('.', 2)[2]), num(v, 0)] for k, v in sorted(F.items()) if k.startswith('coorte.situacao.')])}
<p class="nota">{e(lb['aviso'])} Horas e custos são estimativas a calibrar com os servidores.</p>"""

    # ---------------- processos
    sec["processos"] = "<h2>Processos analisados</h2>" + tabela(
        ["Processo", "SEI", "Instrumento", "Situação final", "Início", "Fim", "Lead (du)", "Até assinatura (du)",
         "Peças", "Passagens", "Retornos", "Horas piso–teto", "Unidades"],
        [[e(r["municipio"] or r["processo"]), e(r["numero_sei"]), lbl(r["instrumento"]), lbl(r["situacao_final"]),
          e(r["inicio"]), e(r["fim"]), num(r["lead_du"]), num(r["lead_ate_assinatura_du"]), num(r["n_documentos"], 0),
          num(r["passagens"], 0), num(r["retornos"], 0), f"{num(r['horas_piso'])}–{num(r['horas_teto'])}", e(r["unidades"])]
         for r in inds]) + "<h3>Caminho de cada caso (sequência de atividades)</h3>" + tabela(
        ["Processo", "Caminho"], [[e(r["municipio"] or r["processo"]),
                                   " › ".join(e(nomes.get(t, t)) for t in r["caminho"].split(" > ") if t)] for r in inds])

    # ---------------- fluxo
    linhas = []
    for t, a in proc["tarefas"].items():
        ea, hp, ht = a.get("espera_antes") or {}, a.get("horas_piso") or {}, a.get("horas_teto") or {}
        linhas.append([e(t), e(nomes.get(t, t)), e(raia.get(t, "")), f"{num(a['pct_casos'])}% ({num(a['casos'], 0)})",
                       num(a["ocorrencias"], 0), num(a["casos_com_laco"], 0), num(ea.get("mediana")), num(ea.get("q3")),
                       num(ea.get("max")), f"{num(hp.get('mediana'))}–{num(ht.get('mediana'))}",
                       num(F.get(f"coorte.{t}.pct_espera_total")) + "%"])
    sec["fluxo"] = f"""<h2>Fluxo AS-IS e TO-BE</h2>
<p>Diagramas BPMN 2.0 (AS-IS consolidado dos casos e TO-BE proposto). <a href="../bpmn/index.html" target="_blank">Abrir o visualizador em tela cheia</a>.</p>
<iframe class="bpmn" src="../bpmn/index.html" title="Diagramas BPMN"></iframe>
<h3>Atividades do AS-IS na coorte</h3>
{tabela(['Id', 'Atividade', 'Raia', '% dos casos', 'Ocorrências', 'Casos com laço', 'Espera antes — mediana (du)', 'q3', 'máx.', 'Horas por ocorrência (piso–teto, mediana)', '% da espera total'], linhas)}
<h3>Caminhos mais frequentes</h3>
{tabela(['Casos', 'Caminho'], [[num(c['casos'], 0), ' › '.join(e(nomes.get(t, t)) for t in c['caminho'].split(' > '))] for c in proc['caminhos'][:5]])}"""

    # ---------------- avaliação
    desp = tabela(["Desperdício", "Severidade", "Atividades", "Evidência"],
                  [[e(d["tipo"]), e(d["severidade"]), e(", ".join(d["atividades"])), e(d["evidencia"])] for d in av["desperdicios"]])
    atv = tabela(["Id", "Atividade", "Valor", "Potencial de automação", "Melhoria sem tecnologia", "Aplicação de tecnologia", "Controle humano"],
                 [[e(t), e(nomes.get(t, t)), e(a["valor"]), e(a["potencial_ia"]), e(a["melhoria_lean"]), e(a["aplicacao_ia"]),
                   e(a["controle_humano"])] for t, a in av["atividades"].items()])
    opo = "".join(f'<div class="op"><h4>{e(o["titulo"])} <span class="tag">{e(o["categoria"])}</span>'
                  f' <span class="tag">impacto {e(o["impacto"])}</span> <span class="tag">esforço {e(o["esforco"])}</span></h4>'
                  f'<p>{e(o["descricao"])}</p><p class="s"><b>Ganho:</b> {e(o["ganho_esperado"])} <b>Pré-requisitos:</b> '
                  f'{e(o["prerequisitos"])} <b>Riscos:</b> {e(o["riscos"])}</p></div>' for o in av["oportunidades"])
    sec["avaliacao"] = (f"<h2>Avaliação AS-IS</h2><p>{e(av['sintese'])}</p><h3>Variabilidade</h3><p>{e(av['variabilidade'])}</p>"
                        f"<h3>Desperdícios (Lean)</h3>{desp}<h3>Análise de valor por atividade</h3>{atv}<h3>Oportunidades</h3>{opo}"
                        "<h3>Perguntas para validação com as unidades</h3><ul>"
                        + "".join(f"<li>{e(p)}</li>" for p in av["perguntas_validacao"]) + "</ul>")

    # ---------------- conformidade
    nor = {n["id"]: n["norma"] for n in normas["normas"]}
    linhas = []
    for r in normas["requisitos"]:
        c = conf.get(r["id"], {})
        pct = c.get("pct_conforme")
        cls = "" if pct is None else ("ok" if pct >= 80 else ("med" if pct >= 50 else "ruim"))
        linhas.append([e(r["id"]), e(nor[r["norma"]]), f"<q>{e(r['trecho'])}</q>", e(r["requisito"]),
                       num(c.get("casos_aplicaveis"), 0), f'<span class="pct {cls}">{num(pct)}{"%" if pct is not None else ""}</span>'])
    det = tabela(["Requisito", "Processo", "Aplica", "Conforme", "Detalhe"],
                 [[e(x["requisito"]), e(x["processo"]), "sim" if x["aplica"] == "True" else "não",
                   {"True": "sim", "False": "não", "": "—"}.get(x["conforme"], num(x["conforme"]) + "%"), e(x["detalhe"])]
                  for x in conf_csv if x["aplica"] == "True"])
    sec["conformidade"] = (f"<h2>Conformidade legal</h2><p>{e(normas['observacao'])}</p>"
                           + tabela(["Id", "Norma", "Trecho literal", "Requisito", "Casos aplicáveis", "% conforme"], linhas)
                           + f"<details><summary>Resultado por processo</summary>{det}</details>")

    # ---------------- TO-BE
    cen = ("conservador", "esperado", "otimista")
    barras = [("Linha de base", lead["mediana"], "base")] + [
        (f"Fase {f} · {c}", res["fases"][f][c]["lead"]["mediana"], c) for f in ("1", "2", "3") for c in cen]
    mx = max(v for _, v, _ in barras) or 1
    W, bh = 640, 26
    svg = [f'<svg viewBox="0 0 {W} {len(barras) * (bh + 8) + 10}" class="graf" role="img" aria-label="Lead mediano por fase e cenário">']
    for i, (r, v, c) in enumerate(barras):
        y = 5 + i * (bh + 8)
        w = (W - 260) * v / mx
        svg.append(f'<text x="150" y="{y + bh * 0.68}" text-anchor="end" class="gt">{e(r)}</text>'
                   f'<rect x="160" y="{y}" width="{w:.1f}" height="{bh}" rx="3" class="b-{c}"/>'
                   f'<text x="{166 + w:.1f}" y="{y + bh * 0.68}" class="gt">{num(v)} du</text>')
    svg.append("</svg>")
    fases_tab = tabela(["Fase", "Cenário", "Lead mediano (du)", "Lead médio (du)", "Horas por caso (média, teto)",
                        "Horas/ano (teto)"] + [f"Conformidade {k}" for k in res["linha_base"]["conformidade_temporal"]],
                       [["Base", "—", num(lead["mediana"]), num(lead["media"]), num(res["linha_base"]["horas_teto"]["media"]),
                         num(res["linha_base"]["anual"]["horas"]["teto"])]
                        + [num(v) + "%" for v in res["linha_base"]["conformidade_temporal"].values()]]
                       + [[f, c, num(x["lead"]["mediana"]), num(x["lead"]["media"]), num(x["horas_teto"]["media"]),
                           num(x["anual"]["horas"]["teto"])] + [num(v) + "%" for v in x["conformidade_temporal"].values()]
                          for f in ("1", "2", "3") for c in cen for x in [res["fases"][f][c]]])
    mtab = tabela(["Id", "Fase", "Melhoria", "Atividades", "Efeito", "Cons.", "Esp.", "Otim.", "Referência", "Hipótese", "Controle humano"],
                  [[e(m["id"]), num(m["fase"], 0), f"<b>{e(m['titulo'])}</b><br><span class='s'>{e(m['descricao'])}</span>",
                    e(", ".join(m["atividades"])), lbl(m["efeito"]["tipo"])]
                   + [num(m["efeito"]["cenarios"][c]) for c in cen]
                   + [e(", ".join(m["benchmark"]) or "—"), "sim" if m["hipotese"] else "não",
                      e(m["controle_humano"] if m["fase"] == 3 else "")] for m in mel])
    sens = tabela(["Melhoria retirada", "Fase", "Lead mediano piora (du)", "Lead médio piora (du)", "Horas médias pioram"],
                  [[e(s["melhoria"]), num(s["fase"], 0), num(s["lead_mediano_du"]), num(s["lead_medio_du"]), num(s["horas_medias"], 2)]
                   for s in res["sensibilidade"]["sem_cada_melhoria"]])
    sec["tobe"] = (f"<h2>TO-BE: melhorias e simulação</h2><p>Três fases cumulativas: 1 ajuste do fluxo; 2 automação de regras e "
                   f"dados; 3 automação assistida com revisão humana. Simulação sobre os {num(res['casos'], 0)} casos, em três cenários. "
                   f"Volume anual e custo-hora são premissas: {e(res['premissas']['volume_anual']['origem'])}.</p>"
                   f"<h3>Lead time mediano por fase e cenário</h3>{''.join(svg)}{fases_tab}<h3>Melhorias</h3>{mtab}"
                   f"<h3>Sensibilidade (fase 3, cenário esperado)</h3>{sens}")

    # ---------------- controles
    itab = tabela(["Id", "Indicador", "Definição", "Linha de base", "Metas (fase: valor)", "Alerta", "Responsável"],
                  [[e(i["id"]), e(i["nome"]), e(i["definicao"]), f"{num(i['linha_base']['valor'])} {e(i['linha_base']['unidade'])}",
                    "<br>".join(f"{num(m['fase'], 0)}: {num(m['valor'])}" for m in i["metas"]) or "—",
                    e(i["alerta"]["regra"]), e(i["responsavel"])] for i in ctl["indicadores"]])
    qtab = tabela(["Id", "Melhorias", "Verificação", "Amostragem", "Critério de aceite", "Meta", "Responsável"],
                  [[e(q["id"]), e(", ".join(q["melhorias"])), e(q["verificacao"]), e(q["amostragem"]), e(q["criterio_aceite"]),
                    e(q["meta"]), e(q["responsavel"])] for q in ctl["controles_qualidade_ia"]])
    sec["controles"] = f"<h2>Controles, indicadores e metas</h2>{itab}<h3>Controles de qualidade das ferramentas automatizadas</h3>{qtab}"

    # ---------------- priorização
    crit = tabela(["Critério", "Peso", "Métrica", "Nota (1–5)"],
                  [[lbl(k), num(mz["pesos"][k], 0), num(mz["metricas"][k], 3), num(mz["notas"][k], 0)] for k in mz["notas"]])
    port = tabela(["Portão", "Regra", "Atende"], [[lbl(k), e(p["regra"]), "sim" if p["ok"] else "não"] for k, p in mz["portoes_piloto"].items()])
    ctab = tabela(["Cenário", "Horas liberadas/ano", "Retorno/ano (R$)", "Construção isolada (R$)", "Construção incremental (R$)",
                   "Manutenção/ano (R$)", "Payback isolado (anos)", "Saldo em 5 anos (R$)"],
                  [[e(c), num(x["horas_liberadas_ano"]), num(x["retorno_ano"], 0), num(x["custo_construcao_isolado"], 0),
                    num(x["custo_construcao_incremental"], 0), num(x["manutencao_ano"], 0),
                    num(x["payback_anos_isolado"]) if x["payback_anos_isolado"] else "não se paga",
                    num(x["saldo_5_anos_isolado"], 0)] for c, x in mz["cenarios"].items()])
    atab = tabela(["Atividade", "Potencial", "Capacidades", "Horas-teto/ano"] + [f"Liberadas ({c})" for c in cen],
                  [[e(nomes.get(a["atividade"], a["atividade"])), e(a["potencial_ia"]), e(a["tipos_ia"]), num(a["horas_teto_ano"])]
                   + [num(a[f"horas_liberadas_{c}"]) for c in cen] for a in mz["atividades"]])
    sec["priorizacao"] = (f"<h2>Priorização da automação</h2><div class='cards'>{card('nota composta (0–100)', num(mz['nota_composta']), e(mz['prioridade']))}</div>"
                          f"<p>{e(mz['referencia_agenersa'])}.</p>{crit}<h3>Portões do piloto</h3>{port}<h3>Custo × retorno</h3>{ctab}"
                          f"<h3>Atividades e capacidades</h3>{atab}<p class='nota'>Premissas de volume, custo-hora, fração automatizável e esforço "
                          f"de construção são hipóteses a calibrar.</p>")

    abas = [("geral", "Visão geral"), ("processos", "Processos"), ("fluxo", "Fluxo"), ("avaliacao", "Avaliação AS-IS"),
            ("conformidade", "Conformidade"), ("tobe", "TO-BE"), ("controles", "Controles"), ("priorizacao", "Priorização")]
    nav = "".join(f'<button data-t="{k}">{e(v)}</button>' for k, v in abas)
    corpo = "".join(f'<section id="{k}">{sec[k]}</section>' for k, _ in abas)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(PAGINA.replace("__NAV__", nav).replace("__CORPO__", corpo), encoding="utf-8")
    print("site:", OUT / "index.html")


PAGINA = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Celebração de Convênios — Mapeamento</title><style>
:root{--bg:#f7f7f5;--fg:#1d2327;--mut:#5c6670;--card:#fff;--bd:#dde1e4;--ac:#1f5f8b;--ok:#2e7d32;--med:#b26a00;--ruim:#b3261e;
--b1:#9db7cf;--b2:#1f5f8b;--b3:#3f9c6b;--b0:#8a8f94}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#14181b;--fg:#e6e8ea;--mut:#9aa4ad;--card:#1d2226;--bd:#30373d;--ac:#7cb6e0;--b1:#5d7f9c;--b2:#7cb6e0;--b3:#6cc596;--b0:#6c737a}}
:root[data-theme=dark]{--bg:#14181b;--fg:#e6e8ea;--mut:#9aa4ad;--card:#1d2226;--bd:#30373d;--ac:#7cb6e0;--b1:#5d7f9c;--b2:#7cb6e0;--b3:#6cc596;--b0:#6c737a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
header{padding:18px 16px 0;max-width:1280px;margin:auto}h1{font-size:1.35rem;margin:0 0 4px}header p{margin:0;color:var(--mut)}
nav{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--bd);display:flex;gap:4px;overflow-x:auto;padding:8px 16px;z-index:2}
nav button{background:none;border:1px solid transparent;color:var(--fg);padding:6px 12px;border-radius:6px;cursor:pointer;white-space:nowrap;font:inherit}
nav button.on{background:var(--card);border-color:var(--bd);color:var(--ac);font-weight:600}
#tema{margin-left:auto}main{max-width:1280px;margin:auto;padding:8px 16px 40px}section{display:none}section.on{display:block}
h2{font-size:1.2rem;margin:18px 0 8px}h3{font-size:1rem;margin:22px 0 6px}h4{margin:0 0 4px;font-size:.95rem}.lead{font-size:1.02rem}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:10px;margin:12px 0}
.card{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:12px}.card .v{font-size:1.6rem;font-weight:650;color:var(--ac)}
.card .r{font-size:.85rem}.card .s,.s{color:var(--mut);font-size:.8rem}.nota{color:var(--mut);font-size:.85rem}
.tw{overflow-x:auto;border:1px solid var(--bd);border-radius:8px;background:var(--card);margin:8px 0}
table{border-collapse:collapse;width:100%;font-size:.84rem}th,td{padding:6px 8px;border-bottom:1px solid var(--bd);text-align:left;vertical-align:top}
th{position:sticky;top:0;background:var(--card);font-weight:600}q{font-style:italic;color:var(--mut)}
.pct{font-weight:650}.ok{color:var(--ok)}.med{color:var(--med)}.ruim{color:var(--ruim)}
.tag{font-size:.72rem;font-weight:500;border:1px solid var(--bd);border-radius:10px;padding:1px 7px;color:var(--mut)}
.op{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:10px 12px;margin:8px 0}.op p{margin:4px 0}
iframe.bpmn{width:100%;height:70vh;border:1px solid var(--bd);border-radius:8px;background:#fff}
.graf{width:100%;max-width:760px;display:block;margin:8px 0}.gt{font-size:12px;fill:var(--fg)}
.b-base{fill:var(--b0)}.b-conservador{fill:var(--b1)}.b-esperado{fill:var(--b2)}.b-otimista{fill:var(--b3)}
details{margin:10px 0}summary{cursor:pointer;color:var(--ac)}a{color:var(--ac)}
</style></head><body>
<header><h1>Celebração de convênios e contratos de delegação da regulação</h1>
<p>AGERGS · mapeamento AS-IS, avaliação, conformidade legal, TO-BE, controles e priorização</p></header>
<nav>__NAV__<button id="tema" title="Alternar tema">◐</button></nav><main>__CORPO__</main>
<script>
const bs=[...document.querySelectorAll('nav button[data-t]')];
function ab(t){bs.forEach(b=>b.classList.toggle('on',b.dataset.t===t));document.querySelectorAll('section').forEach(s=>s.classList.toggle('on',s.id===t));try{localStorage.setItem('aba',t)}catch(e){}}
bs.forEach(b=>b.onclick=()=>ab(b.dataset.t));let ini='geral';try{ini=localStorage.getItem('aba')||ini}catch(e){}ab(document.getElementById(ini)?ini:'geral');
document.getElementById('tema').onclick=()=>{const r=document.documentElement,d=r.dataset.theme==='dark'||(!r.dataset.theme&&matchMedia('(prefers-color-scheme:dark)').matches);r.dataset.theme=d?'light':'dark'};
</script></body></html>"""

if __name__ == "__main__":
    main()
