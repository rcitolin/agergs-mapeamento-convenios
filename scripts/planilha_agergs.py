"""Planilha consolidada do mapeamento (saida/Mapeamento_AGERGS_Celebracao.xlsx) e gráficos PNG da fase 3 e da fase 4.
Uso: python3 scripts/planilha_agergs.py"""
import json
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
S = RAIZ / "saida"
CEN = ("conservador", "esperado", "otimista")


def j(p):
    return json.loads((S / p).read_text())


def main():
    proc, mel, res = j("fase2/procedimento_CONV.json"), j("fase3/melhorias_CONV.json")["melhorias"], j("fase3/resultado_tobe_CONV.json")
    ctl, mz, lb = j("fase3/controles_CONV.json"), j("fase4/matriz_automacao_CONV.json"), j("fase3/linha_base_CONV.json")
    nomes = {e["id"]: e["nome"] for e in j("bpmn/modelo_CONV.json")["elementos"] if e["tipo"] == "tarefa"}
    tar = []
    for t, a in proc["tarefas"].items():
        l = dict(id=t, atividade=nomes.get(t, t), casos=a["casos"], pct_casos=a["pct_casos"], ocorrencias=a["ocorrencias"],
                 casos_com_laco=a["casos_com_laco"])
        for k in ("espera_antes", "execucao", "horas_piso", "horas_teto"):
            for s in ("mediana", "q1", "q3", "max"):
                l[f"{k}_{s}"] = (a.get(k) or {}).get(s)
        tar.append(l)
    tobe = [dict(fase="base", cenario="—", lead_mediana=lb["por_caso"]["lead_du"]["mediana"], lead_media=lb["por_caso"]["lead_du"]["media"],
                 horas_teto_media=lb["por_caso"]["horas_teto"]["media"], horas_ano_teto=lb["anual"]["horas"]["teto"],
                 **{f"conf_{k}": v for k, v in res["linha_base"]["conformidade_temporal"].items()})]
    for f in ("1", "2", "3"):
        for c in CEN:
            x = res["fases"][f][c]
            tobe.append(dict(fase=f, cenario=c, lead_mediana=x["lead"]["mediana"], lead_media=x["lead"]["media"],
                             horas_teto_media=x["horas_teto"]["media"], horas_ano_teto=x["anual"]["horas"]["teto"],
                             **{f"conf_{k}": v for k, v in x["conformidade_temporal"].items()}))
    melh = [dict(id=m["id"], fase=m["fase"], titulo=m["titulo"], descricao=m["descricao"], atividades=", ".join(m["atividades"]),
                 efeito=m["efeito"]["tipo"], **{c: m["efeito"]["cenarios"][c] for c in CEN}, fatos=", ".join(m["fatos"]),
                 requisitos=", ".join(m["requisitos"]), benchmark=", ".join(m["benchmark"]), hipotese=m["hipotese"],
                 justificativa=m["justificativa_parametro"], riscos=m["riscos"], dependencias=m["dependencias"],
                 controle_humano=m["controle_humano"]) for m in mel]
    ind = [dict(id=i["id"], nome=i["nome"], definicao=i["definicao"], linha_base=i["linha_base"]["valor"], unidade=i["linha_base"]["unidade"],
                **{f"meta_fase_{m['fase']}": m["valor"] for m in i["metas"]}, alerta=i["alerta"]["regra"], responsavel=i["responsavel"])
           for i in ctl["indicadores"]]
    prem = [dict(premissa="volume anual de celebrações", valor=lb["volume_anual"]["valor"], origem=lb["volume_anual"]["origem"], hipotese=True)]
    prem += [dict(premissa=f"custo-hora servidor ({k})", valor=v, origem="estimativa a calibrar", hipotese=True) for k, v in lb["custo_hora"].items()]
    prem += [dict(premissa=f"custo-hora desenvolvimento ({c})", valor=v, origem="estimativa a calibrar", hipotese=True)
             for c, v in zip(CEN, mz["premissas"]["custo_hora_dev"])]
    prem += [dict(premissa=f"fração automatizável — potencial {k}", valor=" / ".join(map(str, v)), origem="caso de referência", hipotese=True)
             for k, v in mz["premissas"]["fracao_automatizavel"].items()]
    prem.append(dict(premissa="horas por peça", valor="piso–teto por regra", origem="estimativa a calibrar com os servidores", hipotese=True))
    abas = {"Processos": pd.read_csv(S / "processos_indicadores.csv"), "Atividades por caso": pd.read_csv(S / "estadias.csv"),
            "Fichas por peça": pd.read_csv(S / "fichas_trabalho.csv"), "Procedimento": pd.DataFrame(tar),
            "Conformidade": pd.read_csv(S / "fase3" / "conformidade_CONV.csv"), "Melhorias": pd.DataFrame(melh),
            "Resultado TO-BE": pd.DataFrame(tobe), "Indicadores": pd.DataFrame(ind),
            "Matriz automação": pd.DataFrame(mz["atividades"]), "Premissas": pd.DataFrame(prem)}
    with pd.ExcelWriter(S / "Mapeamento_AGERGS_Celebracao.xlsx") as xw:
        for nome, df in abas.items():
            df.to_excel(xw, sheet_name=nome, index=False)
    print("planilha:", S / "Mapeamento_AGERGS_Celebracao.xlsx", {k: len(v) for k, v in abas.items()})

    # gráfico TO-BE
    rot = ["base"] + [f"F{f}\n{c[:4]}" for f in ("1", "2", "3") for c in CEN]
    val = [lb["por_caso"]["lead_du"]["mediana"]] + [res["fases"][f][c]["lead"]["mediana"] for f in ("1", "2", "3") for c in CEN]
    cor = ["#8a8f94"] + ["#9db7cf", "#1f5f8b", "#3f9c6b"] * 3
    fig, ax = plt.subplots(figsize=(9, 4))
    b = ax.bar(rot, val, color=cor)
    ax.bar_label(b, labels=[f"{v:.1f}".replace(".", ",") for v in val], fontsize=8)
    ax.set_ylabel("lead time mediano por caso (dias úteis)")
    ax.set_title("Lead time mediano: linha de base e TO-BE por fase e cenário")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(S / "fase3" / "tobe_lead.png", dpi=150)
    plt.close(fig)

    # gráfico matriz de automação: horas-teto/ano × fração liberada esperada, por atividade
    at = mz["atividades"]
    cores = {"alto": "#1f5f8b", "médio": "#3f9c6b", "baixo": "#8a8f94"}
    fig, ax = plt.subplots(figsize=(8, 5))
    for a in at:
        h = a["horas_teto_ano"]
        fr = a["horas_liberadas_esperado"] / h if h else 0
        ax.scatter(h, fr, s=60, color=cores[a["potencial_ia"]])
        ax.annotate(nomes.get(a["atividade"], a["atividade"]), (h, fr), fontsize=7, xytext=(4, 3), textcoords="offset points")
    for k, c in cores.items():
        ax.scatter([], [], color=c, label=f"potencial {k}")
    ax.legend(fontsize=8, frameon=False)
    ax.set_xlabel("horas de trabalho por ano (teto)")
    ax.set_ylabel("fração liberada (cenário esperado)")
    ax.set_title(f"Matriz de automação por atividade — nota composta {mz['nota_composta']:.1f}".replace(".", ","))
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    (S / "fase4").mkdir(exist_ok=True)
    fig.savefig(S / "fase4" / "matriz_automacao.png", dpi=150)
    plt.close(fig)
    print("gráficos: fase3/tobe_lead.png, fase4/matriz_automacao.png")


if __name__ == "__main__":
    main()
