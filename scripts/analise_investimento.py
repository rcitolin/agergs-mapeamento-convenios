"""Análise de investimento da automação da celebração (relatório docs/ANALISE_INVESTIMENTO.md).

Compara três cenários tarefa a tarefa — atual (AS-IS), sem sistema (ganhos rápidos) e automatizado — e calcula VPL,
payback, teto de investimento, margem de segurança, custo por hora liberada, estresse e sensibilidade.
Ocorrências e horas do AS-IS vêm de saida/fase2/casos_CONV.json; volume e custo-hora foram informados pelo gestor;
o resto é HIPÓTESE declarada abaixo. Saída: saida/fase5/analise_investimento_CONV.json"""
import collections
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CASOS = RAIZ / "saida" / "fase2" / "casos_CONV.json"
OUT = RAIZ / "saida" / "fase5"

# dados informados pelo gestor
VOLUME = 20                    # casos/ano, inclui aditivos e novos serviços regulados
CUSTO_HORA = 57.69             # R$ 10.000/mês ÷ 173,3 h
# premissas do roteiro de análise
TAXA, HORIZONTE, MANUT = 0.085, 5, 0.20
# HIPÓTESES
CUSTO_HORA_DEV = 150           # R$/h técnica, centro da faixa 100–220 de comum.py
PRODUTIVIDADE = 0.5            # redução das horas de desenvolvimento pelas ferramentas atuais
OPERACAO = 3600 + 100          # hospedagem R$ 300/mês + uso de IA (~1 M caracteres/caso × R$ 5/M)
TRABALHO_NOVO = (12, 36)       # h/ano de cadastro, suporte, falhas e exceções do sistema
HORAS_SEM_SISTEMA, MANUT_SEM_SISTEMA = 100, 16   # implantação e revisão anual dos modelos (h de servidor)
HORAS_NORMA = 24               # resolução do Conselho, além da implantação sem sistema
VALIDACAO_H = 30 * 2           # 30 casos × 2 h de servidor
COMPONENTES = [  # horas de construção (metodologia-repo/scripts/comum.py, HORAS_CAPACIDADE e HORAS_PLATAFORMA)
    ("Plataforma: integração SEI-RS, ambiente, trilha de auditoria", 160), ("Configuração de 13 atividades (16 h cada)", 208),
    ("Verificação de conformidade", 100), ("Extração de dados de documentos", 80), ("Redação assistida de minuta", 80),
    ("Classificação e triagem", 60), ("Busca de precedentes e normas", 60), ("Automação de tramitação (RPA no SEI)", 40),
    ("Sumarização e linha do tempo", 40), ("Adequação LGPD e segurança (HIPÓTESE)", 40),
    ("Monitoramento de prazos e alertas", 24), ("Painel e indicadores", 24)]
ORDEM = ["t1", "t2", "t3", "t4", "t5", "t16", "t6", "t7", "t8", "t9", "t10", "t11", "t12", "t13", "t14", "t15", "out"]
CONCENTRADO = {"t4", "t5", "t6", "t7", "t8", "t9"}
CEN = ("min", "med", "max")


def as_is():
    """(ocorrências por caso, h mín por ocorrência, h máx por ocorrência); 'out' = peças sem tarefa."""
    d = json.loads(CASOS.read_text())
    n = len(d)
    agg = collections.defaultdict(lambda: [0, 0.0, 0.0])
    tp = tt = 0.0
    for c in d.values():
        tp += c["horas_piso"]
        tt += c["horas_teto"]
        for o in c["ocorrencias"]:
            a = agg[o["atividade"]]
            a[0] += 1
            a[1] += o["horas_piso"]
            a[2] += o["horas_teto"]
    m = {k: (a[0] / n, a[1] / a[0], a[2] / a[0]) for k, a in agg.items()}
    sp = sum(q * a for q, a, _ in m.values())
    st = sum(q * b for q, _, b in m.values())
    m["out"] = (1, tp / n - sp, tt / n - st)
    return m


A0 = as_is()
# HIPÓTESE: tempos sem sistema (fases 1 e 2 do TO-BE) e automatizado (fase 3), por ocorrência
A1 = dict(A0, t2=(1, .25, .5), t3=(.5, .3, .5), t5=(1, .6, 1.2), t16=(1, .2, .4), t6=(1, .6, 1.8),
          t7=(.2,) + A0["t7"][1:], t8=(.4,) + A0["t8"][1:], t9=(1, .3, .6), t10=(0, 0, 0), t11=(1, .3, .5),
          t12=(1, .15, .3), t13=(1, .2, .4), t15=(1, .2, .4))
A2 = dict(A1, t2=(1, .15, .3), t3=(.5, .2, .4), t5=(1, .4, .8), t16=(1, .15, .3), t6=(1, .5, 1.5),
          t8=(.4, A0["t8"][1] * .8, A0["t8"][2] * .8), t9=(1, .2, .4), t11=(1, .25, .4), t12=(1, .1, .2),
          t13=(1, .1, .2), t15=(1, .1, .2), out=(1, A0["out"][1] * .7, A0["out"][2] * .7))
AN = dict(A1, t8=(.2,) + A0["t8"][1:], t9=(0, 0, 0))  # mudar a norma: Conselho só em 10% dos casos, t9 no ato de assinatura
CENARIOS = {"atual": (A0, None), "sem_sistema": (A1, None), "automatizado": (A2, TRABALHO_NOVO), "norma": (AN, None)}


def horas(m, k, c, v=VOLUME):
    q, a, b = m[k]
    return v * q * {"min": a, "med": (a + b) / 2, "max": b}[c]


def total(nome, c, v=VOLUME, adesao=1.0):
    m, novo = CENARIOS[nome]
    t = sum(horas(m, k, c, v) for k in ORDEM)
    if novo:
        base = sum(horas(A1, k, c, v) for k in ORDEM)
        t = base - (base - t) * adesao + {"min": novo[0], "med": sum(novo) / 2, "max": novo[1]}[c]
    return t


def fator(r=TAXA, n=HORIZONTE):
    return sum(1 / (1 + r) ** t for t in range(1, n + 1))


def vpl(i, e, o, r=TAXA, n=HORIZONTE):
    return -i + (e - o - MANUT * i) * fator(r, n)


def teto(e, o, r=TAXA, n=HORIZONTE):
    return (e - o) * fator(r, n) / (1 + MANUT * fator(r, n))


def margem(i, e, o):
    return round((i * (1 + MANUT * fator()) / fator() + o) / e, 3) if e > 0 else None


def payback_anos(i, e, o):
    liq = e - o - MANUT * i
    return round(i / liq, 2) if liq > 0 else None


def custo_hora_liberada(i, o, h):
    return round((i / fator() + MANUT * i + o) / h, 2) if h > 0 else None


def investimento(prod=PRODUTIVIDADE, rh=CUSTO_HORA_DEV):
    return sum(h for _, h in COMPONENTES) * (1 - prod) * rh + VALIDACAO_H * CUSTO_HORA


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tarefas = {k: {n: {"ocorr_caso": round(m[k][0], 3), "h_ocorr": [round(m[k][1], 3), round(m[k][2], 3)],
                       **{f"h_ano_{c}": round(horas(m, k, c), 1) for c in CEN}} for n, (m, _) in CENARIOS.items()}
               for k in ORDEM}
    tot = {n: {c: {"horas": round(total(n, c), 1), "reais": round(total(n, c) * CUSTO_HORA),
                   "fte": round(total(n, c) / 1800, 3),
                   "concentrado": round(sum(horas(CENARIOS[n][0], k, c) for k in CONCENTRADO), 1)} for c in CEN}
           for n in CENARIOS}
    i_com, i_sem = investimento(), investimento(prod=0)
    i_a1, m_a1 = HORAS_SEM_SISTEMA * CUSTO_HORA, MANUT_SEM_SISTEMA * CUSTO_HORA
    i_an = (HORAS_SEM_SISTEMA + HORAS_NORMA) * CUSTO_HORA
    comp = {}
    for base, alvo in (("atual", "sem_sistema"), ("atual", "automatizado"), ("sem_sistema", "automatizado"), ("atual", "norma")):
        comp[f"{alvo}_x_{base}"] = {}
        for c in CEN:
            h = total(base, c) - total(alvo, c)
            e = h * CUSTO_HORA
            r = {"horas": round(h, 1), "reais": round(e), "fte": round(h / 1800, 4)}
            if alvo == "automatizado":
                for rot, i in (("com_produtividade", i_com), ("sem_produtividade", i_sem)):
                    r[rot] = {"vpl": round(vpl(i, e, OPERACAO)), "payback_anos": payback_anos(i, e, OPERACAO),
                              "teto": round(teto(e, OPERACAO)), "margem": margem(i, e, OPERACAO),
                              "custo_hora_liberada": custo_hora_liberada(i, OPERACAO, h)}
            else:
                i0 = i_an if alvo == "norma" else i_a1
                r["vpl"] = round(-i0 + (e - m_a1) * fator())
                r["payback_meses"] = round(i0 / (e - m_a1) * 12, 1) if e > m_a1 else None
            comp[f"{alvo}_x_{base}"][c] = r
    estresse = {"automatizado_x_atual": round(total("atual", "min") - total("automatizado", "max"), 1),
                "automatizado_x_sem_sistema": round(total("sem_sistema", "min") - total("automatizado", "max"), 1),
                "sem_sistema_x_atual": round(total("atual", "min") - total("sem_sistema", "max"), 1)}

    def inc(v=VOLUME, ch=CUSTO_HORA, ad=1.0):
        return (total("sem_sistema", "med", v) - total("automatizado", "med", v, ad)) * ch

    e0 = inc()
    sens = []
    for nome, vals, f in (("custo_hora", (40, CUSTO_HORA, 115.38), lambda x: (i_com, inc(ch=x), OPERACAO, TAXA, HORIZONTE)),
                          ("volume", (10, 20, 40, 80, 330), lambda x: (i_com, inc(v=x), OPERACAO, TAXA, HORIZONTE)),
                          ("horizonte", (3, 5, 10), lambda x: (i_com, e0, OPERACAO, TAXA, x)),
                          ("taxa", (0.05, TAXA, 0.12), lambda x: (i_com, e0, OPERACAO, x, HORIZONTE)),
                          ("adesao", (0.5, 0.75, 1.0), lambda x: (i_com, inc(ad=x), OPERACAO, TAXA, HORIZONTE)),
                          ("produtividade", (0, 0.5, 0.7), lambda x: (investimento(prod=x), e0, OPERACAO, TAXA, HORIZONTE)),
                          ("custo_hora_dev", (100, 150, 220), lambda x: (investimento(rh=x), e0, OPERACAO, TAXA, HORIZONTE)),
                          ("operacao", (0, OPERACAO, 2 * OPERACAO), lambda x: (i_com, e0, x, TAXA, HORIZONTE))):
        for x in vals:
            i, e, o, r, n = f(x)
            sens.append({"premissa": nome, "valor": x, "investimento": round(i), "economia": round(e),
                         "vpl": round(vpl(i, e, o, r, n)), "teto": round(teto(e, o, r, n))})
    out = {"premissas": {"volume": VOLUME, "custo_hora": CUSTO_HORA, "taxa": TAXA, "horizonte": HORIZONTE,
                         "manutencao": MANUT, "custo_hora_dev": CUSTO_HORA_DEV, "produtividade": PRODUTIVIDADE,
                         "operacao": OPERACAO, "trabalho_novo": TRABALHO_NOVO, "fator_vp": round(fator(), 4),
                         "hipotese": True},
           "investimento": {"componentes": COMPONENTES, "validacao_reais": round(VALIDACAO_H * CUSTO_HORA),
                            "com_produtividade": round(i_com), "sem_produtividade": round(i_sem),
                            "sem_sistema": round(i_a1), "sem_sistema_manutencao": round(m_a1), "norma": round(i_an)},
           "tarefas": tarefas, "totais": tot, "comparacoes": comp, "estresse_horas": estresse, "sensibilidade": sens}
    (OUT / "analise_investimento_CONV.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"I = R$ {i_com:,.0f} (sem produtividade R$ {i_sem:,.0f}); "
          f"sistema × sem sistema (médio): {comp['automatizado_x_sem_sistema']['med']}")
    print("saida/fase5/analise_investimento_CONV.json")


if __name__ == "__main__":
    main()
