"""Fase 3 e 4 (determinísticas) do mapeamento AGERGS — adaptação de verificar_normas.py, conformidade.py,
linha_base.py, validar_tobe.py, simular_tobe.py, validar_controles.py e priorizacao_automacao.py.

Etapas:
  normas       — confere cada trecho de requisito, literalmente, contra o texto integral da norma (portão)
  conformidade — roda o teste de cada requisito em cada caso da coorte
  linha_base   — congela a linha de base (com carimbo)
  tobe         — valida melhorias_CONV.json e simula 3 fases × 3 cenários (com sensibilidade)
  controles    — valida controles_CONV.json (linha de base e metas com origem)
  auditoria    — concordância da reclassificação às cegas dos rótulos de atividade
Uso: python3 scripts/fase3_agergs.py [etapa ...]   (sem argumento: todas, na ordem; para no primeiro portão que falhar)
"""
from __future__ import annotations

import copy
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pipeline_agergs import BPMN, F2, RAIZ, SAIDA, _norm_ev, du, estat  # noqa: E402

F3 = SAIDA / "fase3"
F3.mkdir(exist_ok=True)
NORMAS = RAIZ / "normas"
CENARIOS = ("conservador", "esperado", "otimista")

# Premissas de custo e volume: HIPÓTESE até a calibração com a AGERGS (perfil metodologia-repo/perfis/rs_agergs.py)
VOLUME_ANUAL = {"valor": 5, "origem": "hipótese: celebrações iniciadas em 2025 na amostra (Lagoa Bonita do Sul, Nova "
                "Bréscia, Passa Sete, Minas do Leão, Passo Fundo); confirmar com o cadastro de municípios conveniados"}
CUSTO_HORA = {"piso": 55.0, "esperado": 88.0, "teto": 121.0}  # R$/h: hipótese (vencimento estimado × fator 1,0/1,6/2,2)
HORAS_ANO_FTE = 1600


def _j(p):
    return json.loads(Path(p).read_text())


def _w(p, obj):
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=1))


class Portao(Exception):
    pass


# ================================================================ normas
def etapa_normas():
    d = _j(F3 / "normas_CONV.json")
    arqs = {n["id"]: n["arquivo"] for n in d["normas"]}
    probs, res = [], []
    for r in d["requisitos"]:
        txt = _norm_ev((NORMAS / arqs[r["norma"]]).read_text(errors="replace"))
        ok = _norm_ev(r["trecho"]) in txt
        res.append(dict(id=r["id"], norma=r["norma"], literal=ok))
        if not ok:
            probs.append(r["id"])
    _w(F3 / "verificacao_normas_CONV.json", dict(requisitos=res, problemas=probs))
    print(f"normas: {len(res) - len(probs)}/{len(res)} trechos conferidos literalmente")
    if probs:
        raise Portao(f"trechos não encontrados no texto integral: {probs}")


# ================================================================ conformidade
def _ocs(caso, ats):
    return [o for o in caso["ocorrencias"] if o["atividade"] in ats and o.get("inicio")]


def testar(r, caso, narr, fichas_caso):
    """(aplica, conforme, detalhe) de um requisito num caso. caso = linha do tempo (casos_CONV.json)."""
    t = r["teste"]
    inst = narr.get("instrumento", "")
    assin = _ocs(caso, ["t11"])
    if t["tipo"] == "fundamento":
        return False, None, "requisito-fundamento: não há teste por caso"
    if r["aplica"] == "contratos" and inst != "contrato_prestacao_servicos_regulacao":
        return False, None, "não é contrato de prestação de serviços de regulação"
    if r["aplica"].startswith("com_assinatura") and not assin:
        return False, None, "sem assinatura do instrumento nos autos"
    if r["aplica"] == "com_assinatura_lei_14133" and assin[0]["inicio"] < "2021-04-01":
        return False, None, "assinado antes da Lei 14.133/2021 (regime da Lei 8.666, fora da base)"
    if t["tipo"] == "presenca":
        oc = _ocs(caso, t["atividades"]) or [o for o in caso["ocorrencias"] if o["atividade"] in t["atividades"]]
        return True, bool(oc), f"{len(oc)} ocorrência(s) de {t['atividades']}"
    if t["tipo"] == "presenca_atividade_ficha":
        n = sum(1 for f in fichas_caso if f.get("atividade") == t["atividade_ficha"])
        return True, n > 0, f"{n} peça(s) {t['atividade_ficha']} nos autos"
    if t["tipo"] == "antes_de":
        ref = assin[0]["inicio"]
        oc = [o for o in _ocs(caso, t["atividades"]) if o["inicio"] <= ref]
        return True, bool(oc), f"{len(oc)} ocorrência(s) de {t['atividades']} até {ref}"
    if t["tipo"] == "prazo_max":
        if "de" in t:
            pub = [o for o in _ocs(caso, [t["ate"]]) if o["inicio"] >= assin[0]["inicio"]]
            if not pub:
                return True, False, "sem publicação após a assinatura nos autos"
            dias = du(assin[-1]["fim"] if assin[-1]["fim"] <= pub[0]["inicio"] else assin[0]["inicio"], pub[0]["inicio"])
            return True, dias <= t["dias_uteis"], f"{dias:.0f} du da assinatura à publicação"
        inst_oc = _ocs(caso, t["de_ultima"])
        if not inst_oc:
            return False, None, "sem peça de instrução nos autos"
        ultima = max(o["fim"] for o in inst_oc)
        dec = [o for o in _ocs(caso, t["ate_primeira"]) if o["inicio"] >= ultima]
        if not dec:
            return True, False, f"sem decisão após a última instrução ({ultima})"
        dias = du(ultima, dec[0]["inicio"])
        return True, dias <= t["dias_uteis"], f"{dias:.0f} du da última instrução à decisão"
    if t["tipo"] == "espera_max":
        oc = [o for o in caso["ocorrencias"] if o["atividade"] not in t["excluir"] and o.get("espera_antes_du") is not None]
        if not oc:
            return False, None, "sem ocorrência interna datada"
        dentro = sum(1 for o in oc if o["espera_antes_du"] <= t["dias_uteis"])
        return True, round(100 * dentro / len(oc), 1), f"{dentro}/{len(oc)} ocorrências internas com espera ≤ {t['dias_uteis']} du"
    raise ValueError(t["tipo"])


def _contexto():
    casos = _j(F2 / "casos_CONV.json")
    narr = {}
    for arq in sorted((RAIZ / "dados" / "narrativas").glob("*.json")):
        proc = arq.stem.replace("_p1", "").replace("_p2", "")
        narr[proc] = {**narr.get(proc, {}), **{k: v for k, v in _j(arq).items() if v}}
    fichas = [json.loads(l) for l in (SAIDA / "fichas_trabalho.jsonl").read_text().splitlines() if l.strip()]
    return casos, narr, fichas


def conformidade(casos, narr, fichas, reqs):
    linhas, resumo = [], {}
    for r in reqs:
        vals = []
        for proc, c in sorted(casos.items()):
            ap, conf, det = testar(r, c, narr.get(proc, {}), [f for f in fichas if f["processo"] == proc])
            linhas.append(dict(requisito=r["id"], processo=proc, aplica=ap, conforme=conf, detalhe=det))
            if ap:
                vals.append(100.0 if conf is True else (0.0 if conf is False else float(conf)))
        resumo[r["id"]] = dict(casos_aplicaveis=len(vals),
                               pct_conforme=round(sum(vals) / len(vals), 1) if vals else None)
    return linhas, resumo


def etapa_conformidade():
    casos, narr, fichas = _contexto()
    reqs = _j(F3 / "normas_CONV.json")["requisitos"]
    linhas, resumo = conformidade(casos, narr, fichas, reqs)
    with open(F3 / "conformidade_CONV.csv", "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    _w(F3 / "conformidade_CONV.json", dict(codigo="CONV", requisitos=resumo))
    for k, v in resumo.items():
        print(f"  {k}: {v['pct_conforme']}% em {v['casos_aplicaveis']} casos")


# ================================================================ linha de base
def _custo(horas):
    return {k: round(horas * v) for k, v in CUSTO_HORA.items()}


def etapa_linha_base():
    casos = _j(F2 / "casos_CONV.json")
    conf = _j(F3 / "conformidade_CONV.json")["requisitos"]
    por_caso = {k: estat([c[k] for c in casos.values() if c[k] is not None]) for k in
                ("lead_du", "lead_ate_assinatura_du", "espera_entre_atividades_du", "execucao_atividades_du",
                 "terceiros_du", "horas_piso", "horas_teto", "passagens", "retornos", "n_encaminhamentos")}
    hp, ht = por_caso["horas_piso"]["media"], por_caso["horas_teto"]["media"]
    vol = VOLUME_ANUAL["valor"]
    lb = dict(codigo="CONV", nome="Celebração de convênio ou contrato de delegação da regulação",
              situacao="indicativo" if len(casos) >= 5 else "estudo_de_caso", casos_coorte=len(casos),
              aviso="Menos de 15 casos: medianas instáveis; datas inferidas das peças (sem andamentos do SEI).",
              por_caso=por_caso, volume_anual=VOLUME_ANUAL,
              anual=dict(horas={"piso": round(hp * vol, 1), "teto": round(ht * vol, 1)},
                         fte={"piso": round(hp * vol / HORAS_ANO_FTE, 2), "teto": round(ht * vol / HORAS_ANO_FTE, 2)},
                         custo_reais=dict(piso=_custo(hp * vol)["piso"], esperado=_custo((hp + ht) / 2 * vol)["esperado"],
                                          teto=_custo(ht * vol)["teto"])),
              custo_hora=CUSTO_HORA, custo_hora_hipotese=True,
              conformidade={k: v["pct_conforme"] for k, v in conf.items() if v["pct_conforme"] is not None})
    lb["carimbo"] = hashlib.sha256(json.dumps(lb, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    _w(F3 / "linha_base_CONV.json", lb)
    print(f"linha de base: lead mediano {por_caso['lead_du']['mediana']} du em {len(casos)} casos; carimbo {lb['carimbo'][:12]}")


# ================================================================ TO-BE: validação e simulação
def validar_tobe(mel, fatos_ids, reqs, bench_ids, tarefas):
    probs = []
    prazo_min = {r["id"] for r in reqs if r.get("tipo_prazo") == "prazo_min"}
    for m in mel["melhorias"]:
        i = m["id"]
        if not m.get("fatos") or any(f not in fatos_ids for f in m["fatos"]):
            probs.append(f"{i}: fato inexistente ou ausente {[f for f in m.get('fatos', []) if f not in fatos_ids]}")
        if any(r not in {x['id'] for x in reqs} for r in m.get("requisitos", [])):
            probs.append(f"{i}: requisito inexistente")
        if any(b not in bench_ids for b in m.get("benchmark", [])):
            probs.append(f"{i}: benchmark inexistente {m.get('benchmark')}")
        if not m.get("benchmark") and not m.get("hipotese"):
            probs.append(f"{i}: sem benchmark e sem hipotese=true")
        e = m["efeito"]
        for t in e.get("atividades", []) + [e.get("a"), e.get("b")]:
            if t and t not in tarefas:
                probs.append(f"{i}: atividade {t} não existe no modelo")
        if any(t in ("t1", "t3") for t in e.get("atividades", [])) and e["tipo"] in ("teto_espera", "reduz_espera_pct"):
            probs.append(f"{i}: corta espera de terceiro (município) — protegida")
        if set(m.get("requisitos", [])) & prazo_min and e["tipo"] in ("teto_espera", "reduz_espera_pct"):
            probs.append(f"{i}: reduz espera protegida por prazo mínimo legal")
        c = e.get("cenarios")
        if c:
            v = [c[k] for k in CENARIOS]
            ok = v[0] >= v[1] >= v[2] if e["tipo"] == "teto_espera" else v[0] <= v[1] <= v[2]
            if not ok:
                probs.append(f"{i}: cenários não monotônicos {v}")
        if m["fase"] == 3 and (not m.get("controle_humano") or m["controle_humano"] == "só na fase 3"):
            probs.append(f"{i}: fase 3 sem controle_humano")
    return probs


def aplicar(caso, mels, cenario):
    c = copy.deepcopy(caso)
    oc = c["ocorrencias"]
    for m in mels:
        e = m["efeito"]
        v = e.get("cenarios", {}).get(cenario)
        ats = set(e.get("atividades", []))
        for i, o in enumerate(oc):
            prot = o.get("espera_terceiros_du") or 0
            if e["tipo"] == "teto_espera" and o["atividade"] in ats and o.get("espera_antes_du") is not None:
                o["espera_antes_du"] = min(o["espera_antes_du"], max(v, prot))
            elif e["tipo"] == "reduz_espera_pct" and o["atividade"] in ats and o.get("espera_antes_du"):
                ag = o["espera_antes_du"] - prot
                o["espera_antes_du"] = prot + ag * (1 - v / 100)
            elif e["tipo"] == "reduz_execucao_pct" and o["atividade"] in ats and o.get("execucao_du"):
                o["execucao_du"] *= 1 - v / 100
            elif e["tipo"] == "reduz_horas_pct" and o["atividade"] in ats:
                o["horas_piso"] *= 1 - v / 100
                o["horas_teto"] *= 1 - v / 100
            elif e["tipo"] == "elimina_laco_pct" and o["atividade"] in ats and o["n"] > 1:
                for k in ("espera_antes_du", "execucao_du", "horas_piso", "horas_teto"):
                    if o.get(k):
                        o[k] *= 1 - v / 100
            elif e["tipo"] == "paralelo" and o["atividade"] == e["b"] and i and oc[i - 1]["atividade"] == e["a"]:
                o["espera_antes_du"] = 0.0
    return c


def medir(c, base):
    """Lead simulado = lead AS-IS − redução de espera e execução (o tempo não coberto por atividades fica igual)."""
    d_esp = base["espera_entre_atividades_du"] - sum(o.get("espera_antes_du") or 0 for o in c["ocorrencias"])
    d_exe = base["execucao_atividades_du"] - sum(o.get("execucao_du") or 0 for o in c["ocorrencias"])
    lead = None if base["lead_du"] is None else max(0.0, base["lead_du"] - d_esp - d_exe)
    hp = base["horas_piso"] - sum(o0["horas_piso"] - o1["horas_piso"] for o0, o1 in zip(base["ocorrencias"], c["ocorrencias"]))
    ht = base["horas_teto"] - sum(o0["horas_teto"] - o1["horas_teto"] for o0, o1 in zip(base["ocorrencias"], c["ocorrencias"]))
    return lead, hp, ht


def simular(casos, mels, cenario, reqs, narr, fichas):
    leads, hps, hts, sims = [], [], [], {}
    for proc, caso in casos.items():
        s = aplicar(caso, mels, cenario)
        lead, hp, ht = medir(s, caso)
        sims[proc] = s
        if lead is not None:
            leads.append(lead)
        hps.append(hp)
        hts.append(ht)
    # conformidade temporal simulada: refaz as datas das ocorrências pela soma de espera + execução
    for s in sims.values():
        if not s["inicio"]:
            continue
        cur = s["inicio"]
        import numpy as np
        from pipeline_agergs import _FER
        for o in s["ocorrencias"]:
            if o.get("inicio") is None:
                continue
            ini = np.busday_offset(np.datetime64(cur), int(round(o.get("espera_antes_du") or 0)), roll="forward", holidays=_FER)
            fim = np.busday_offset(ini, int(round(o.get("execucao_du") or 0)), roll="forward", holidays=_FER)
            o["inicio"], o["fim"] = str(ini), str(fim)
            cur = o["fim"]
    _, conf = conformidade(sims, narr, fichas, [r for r in reqs if r.get("tipo_prazo") == "prazo_max"])
    hp, ht = estat(hps), estat(hts)
    vol = VOLUME_ANUAL["valor"]
    return dict(lead=estat(leads), horas_piso=hp, horas_teto=ht,
                anual=dict(horas={"piso": round(hp["media"] * vol, 1), "teto": round(ht["media"] * vol, 1)},
                           custo_reais=dict(piso=_custo(hp["media"] * vol)["piso"], teto=_custo(ht["media"] * vol)["teto"])),
                conformidade_temporal={k: v["pct_conforme"] for k, v in conf.items()})


def etapa_tobe():
    casos, narr, fichas = _contexto()
    mel = _j(F3 / "melhorias_CONV.json")
    fatos_ids = {f["id"] for f in _j(BPMN / "fatos_CONV.json")["fatos"]}
    fatos_ids |= {f"conformidade.{k}" for k in _j(F3 / "conformidade_CONV.json")["requisitos"]}
    reqs = _j(F3 / "normas_CONV.json")["requisitos"]
    bench_ids = {b["id"] for b in _j(RAIZ / "dados" / "referencia" / "benchmark.json")}
    modelo = _j(BPMN / "modelo_CONV.json")
    tarefas = {e["id"] for e in modelo["elementos"] if e["tipo"] == "tarefa"}
    probs = validar_tobe(mel, fatos_ids, reqs, bench_ids, tarefas)
    if probs:
        for p in probs:
            print("  PROBLEMA", p)
        raise Portao(f"validar_tobe: {len(probs)} problema(s)")
    lb = _j(F3 / "linha_base_CONV.json")
    fases = {}
    for f in (1, 2, 3):
        ms = [m for m in mel["melhorias"] if m["fase"] <= f]
        fases[str(f)] = {c: simular(casos, ms, c, reqs, narr, fichas) for c in CENARIOS}
        for c in CENARIOS:  # ganho contra a linha de base
            r_, b_ = fases[str(f)][c], lb["por_caso"]
            r_["ganho_pct"] = dict(
                lead_mediano=round(100 * (1 - r_["lead"]["mediana"] / b_["lead_du"]["mediana"]), 1),
                lead_medio=round(100 * (1 - r_["lead"]["media"] / b_["lead_du"]["media"]), 1),
                horas_teto_medias=round(100 * (1 - r_["horas_teto"]["media"] / b_["horas_teto"]["media"]), 1))
    ms3 = mel["melhorias"]
    ref = fases["3"]["esperado"]
    sens = []
    for m in ms3:
        r = simular(casos, [x for x in ms3 if x["id"] != m["id"]], "esperado", reqs, narr, fichas)
        sens.append(dict(melhoria=m["id"], fase=m["fase"],
                         lead_mediano_du=round(r["lead"]["mediana"] - ref["lead"]["mediana"], 1),
                         lead_medio_du=round(r["lead"]["media"] - ref["lead"]["media"], 1),
                         horas_medias=round(r["horas_teto"]["media"] - ref["horas_teto"]["media"], 2)))
    sens.sort(key=lambda x: (-x["lead_medio_du"], x["melhoria"]))
    out = dict(codigo="CONV", casos=len(casos), carimbo_linha_base=lb["carimbo"],
               linha_base=dict(lead=lb["por_caso"]["lead_du"], horas_piso=lb["por_caso"]["horas_piso"],
                               horas_teto=lb["por_caso"]["horas_teto"], anual=lb["anual"],
                               conformidade_temporal={k: lb["conformidade"].get(k) for k in ("R-CONV-06", "R-CONV-09", "R-CONV-10")}),
               fases=fases, sensibilidade=dict(fase=3, cenario="esperado", sem_cada_melhoria=sens),
               premissas=dict(volume_anual=VOLUME_ANUAL, custo_hora=CUSTO_HORA, hipotese=True))
    _w(F3 / "resultado_tobe_CONV.json", out)
    b = lb["por_caso"]["lead_du"]["mediana"]
    for f in ("1", "2", "3"):
        print(f"  fase {f}: lead mediano " + " / ".join(f"{c} {fases[f][c]['lead']['mediana']}" for c in CENARIOS)
              + f" du (base {b})")


# ================================================================ controles
def _caminho(obj, ref):
    for k in ref.split("."):
        obj = obj[k]
    return obj


def etapa_controles():
    ctl = _j(F3 / "controles_CONV.json")
    fatos = {f["id"]: f["valor"] for f in _j(BPMN / "fatos_CONV.json")["fatos"]}
    res = _j(F3 / "resultado_tobe_CONV.json")
    conf = _j(F3 / "conformidade_CONV.json")["requisitos"]
    reqs = {r["id"] for r in _j(F3 / "normas_CONV.json")["requisitos"]}
    mel = {m["id"]: m for m in _j(F3 / "melhorias_CONV.json")["melhorias"]}
    bench = {b["id"] for b in _j(RAIZ / "dados" / "referencia" / "benchmark.json")}
    probs = []
    for i in ctl["indicadores"]:
        lb = i["linha_base"]
        if i["calculo"]["tipo"] == "conformidade":
            v = conf[i["calculo"]["requisito"]]["pct_conforme"]
            v = 0.0 if v is None else v
        elif lb.get("fato") in fatos:
            v = fatos[lb["fato"]]
        else:
            probs.append(f"{i['id']}: fato da linha de base inexistente {lb.get('fato')}")
            continue
        if v is not None and abs(float(v) - float(lb["valor"])) > 0.051:
            probs.append(f"{i['id']}: linha de base {lb['valor']} ≠ {v}")
        for mt in i["metas"]:
            o = mt["origem"]
            if o["tipo"] == "simulacao":
                try:
                    vv = _caminho(res, o["ref"])
                except (KeyError, TypeError):
                    probs.append(f"{i['id']}: meta com caminho inexistente {o['ref']}")
                    continue
                if abs(float(vv) - float(mt["valor"])) > 0.051:
                    probs.append(f"{i['id']}: meta {mt['valor']} ≠ {vv} ({o['ref']})")
            elif o["tipo"] == "norma" and o["ref"] not in reqs:
                probs.append(f"{i['id']}: meta com requisito inexistente")
            elif o["tipo"] == "benchmark" and o["ref"] not in bench:
                probs.append(f"{i['id']}: meta com benchmark inexistente")
            elif o["tipo"] not in ("simulacao", "norma", "benchmark"):
                probs.append(f"{i['id']}: meta sem origem válida")
        for m in i.get("melhorias", []):
            if m not in mel:
                probs.append(f"{i['id']}: melhoria inexistente {m}")
    cobertas = {m for q in ctl["controles_qualidade_ia"] for m in q["melhorias"]}
    for m in mel.values():
        if m["fase"] == 3 and m["id"] not in cobertas:
            probs.append(f"{m['id']}: melhoria de fase 3 sem controle de qualidade da IA")
    _w(F3 / "validacao_controles_CONV.json", dict(problemas=probs))
    print(f"controles: {len(ctl['indicadores'])} indicadores, {len(ctl['controles_qualidade_ia'])} controles de IA; "
          f"{len(probs)} problema(s)")
    if probs:
        for p in probs:
            print("  PROBLEMA", p)
        raise Portao("validar_controles")


# ================================================================ auditoria às cegas
def etapa_auditoria():
    from pipeline_agergs import ATIV_TAREFA
    # rodadas: gabarito_oculto[_N].json × rotulos_auditor[_N].json (cada rodada com amostra e auditor próprios)
    gab, aud = {}, {}
    for g in sorted((SAIDA / "auditoria").glob("gabarito_oculto*.json")):
        sufixo = g.stem.replace("gabarito_oculto", "")
        r_ = SAIDA / "auditoria" / f"rotulos_auditor{sufixo}.json"
        if r_.exists():
            gab |= _j(g)
            aud |= _j(r_)
    # o gabarito reflete as correções já aplicadas às fichas (dados/correcoes_rotulos.json)
    fichas_at = {f"{f['processo']}#{f['seq']}": f.get("atividade_original", f["atividade"])
                 for f in (json.loads(l) for l in (SAIDA / "fichas_trabalho.jsonl").read_text().splitlines() if l.strip())}
    gab = {k: fichas_at.get(k, v) for k, v in gab.items()}
    ids = sorted(gab)
    linhas = []
    for i in ids:
        a, b = gab[i], aud.get(i)
        linhas.append(dict(id=i, rotulo_ficha=a, rotulo_auditor=b, mesma_atividade=a == b,
                           mesma_tarefa=ATIV_TAREFA.get(a) == ATIV_TAREFA.get(b),
                           substantiva=ATIV_TAREFA.get(a) is not None))
    sub = [x for x in linhas if x["substantiva"]]
    r = dict(pecas=len(linhas), rotuladas_auditor=sum(1 for x in linhas if x["rotulo_auditor"]),
             concordancia_atividade=round(100 * sum(x["mesma_atividade"] for x in linhas) / len(linhas), 1),
             concordancia_tarefa=round(100 * sum(x["mesma_tarefa"] for x in linhas) / len(linhas), 1),
             substantivas=len(sub),
             concordancia_tarefa_substantivas=round(100 * sum(x["mesma_tarefa"] for x in sub) / max(1, len(sub)), 1),
             criterio="≥ 85% nas peças substantivas (concordância na tarefa do modelo)", divergencias=[x for x in linhas if not x["mesma_tarefa"]])
    _w(SAIDA / "auditoria" / "auditoria_classificador_CONV.json", r)
    print(f"auditoria às cegas: tarefa {r['concordancia_tarefa']}% ({len(linhas)} peças); "
          f"substantivas {r['concordancia_tarefa_substantivas']}% ({len(sub)})")


# ================================================================ avaliação AS-IS (portão de ancoragem dos números)
_NUM = re.compile(r"(?<![\w.,-])(\d+(?:,\d+)?)\s*(du|%|h\b|casos?|ocorrências|passagens|retornos|caminhos|encaminhamentos)")


def _bloco(texto, fatos_ids, fatos):
    vals = set()
    for f in fatos_ids:
        v = fatos.get(f)
        if isinstance(v, (int, float)):
            vals |= {f"{float(v):g}".replace(".", ","), f"{round(float(v), 1):g}".replace(".", ",")}
    return [m.group(0) for m in _NUM.finditer(texto) if m.group(1) not in vals]


_MARC = re.compile(r"\{F:([^}]+)\}")


def _fmt(v):
    return f"{float(v):g}".replace(".", ",") if isinstance(v, (int, float)) else str(v)


def renderizar_avaliacao(fatos):
    """avaliacao_CONV.modelo.json → avaliacao_CONV.json: troca {F:id} pelo valor e anota o fato no bloco."""
    m = _j(BPMN / "avaliacao_CONV.modelo.json")
    m.pop("_leia", None)
    faltam = []

    def sub(txt, usados):
        def r(mt):
            i = mt.group(1)
            if i not in fatos:
                faltam.append(i)
                return mt.group(0)
            if i not in usados:
                usados.append(i)
            return _fmt(fatos[i])
        return _MARC.sub(r, txt)

    for campo in ("sintese", "leitura_metricas", "variabilidade"):
        m[campo] = sub(m[campo], m[f"fatos_{campo}"])
    blocos = [m["gargalo"]] + m["desperdicios"] + m["oportunidades"] + list(m["atividades"].values())
    for b in blocos:
        for k, v in list(b.items()):
            if isinstance(v, str):
                b[k] = sub(v, b.setdefault("fatos_usados", []))
    if faltam:
        raise Portao(f"modelo da avaliação cita fatos inexistentes: {sorted(set(faltam))}")
    _w(BPMN / "avaliacao_CONV.json", m)


def etapa_avaliacao():
    fatos = {f["id"]: f["valor"] for f in _j(BPMN / "fatos_CONV.json")["fatos"]}
    fatos |= {f"conformidade.{k}": v["pct_conforme"] for k, v in _j(F3 / "conformidade_CONV.json")["requisitos"].items()}
    if (BPMN / "avaliacao_CONV.modelo.json").exists():
        renderizar_avaliacao(fatos)
    av = _j(BPMN / "avaliacao_CONV.json")
    modelo = _j(BPMN / "modelo_CONV.json")
    probs = []
    inexist = lambda ids: [i for i in ids if i not in fatos]  # noqa: E731
    for campo in ("sintese", "leitura_metricas", "variabilidade"):
        ids = av[f"fatos_{campo}"]
        probs += [f"{campo}: fato inexistente {i}" for i in inexist(ids)]
        probs += [f"{campo}: número sem lastro '{n}'" for n in _bloco(av[campo], ids, fatos)]
    blocos = [("gargalo", av["gargalo"])] + [(f"desperdicios[{i}]", d) for i, d in enumerate(av["desperdicios"])] + \
             [(f"oportunidades[{i}]", d) for i, d in enumerate(av["oportunidades"])] + list(av["atividades"].items())
    for nome, b in blocos:
        ids = b.get("fatos_usados", [])
        probs += [f"{nome}: fato inexistente {i}" for i in inexist(ids)]
        txt = " ".join(str(v) for k, v in b.items() if isinstance(v, str))
        probs += [f"{nome}: número sem lastro '{n}'" for n in _bloco(txt, ids, fatos)]
    tarefas = {e["id"] for e in modelo["elementos"] if e["tipo"] == "tarefa"}
    probs += [f"tarefa sem avaliação: {t}" for t in sorted(tarefas - set(av["atividades"]))]
    _w(BPMN / "validacao_avaliacao_CONV.json", dict(problemas=probs))
    print(f"avaliação: {len(probs)} problema(s)")
    for p_ in probs:
        print("  ", p_)
    if probs:
        raise Portao("validar_avaliacao")
    sha = _j(BPMN / "fatos_CONV.json")["sha"]
    if av.get("validado_contra", {}).get("fatos_sha") != sha:
        from datetime import datetime
        av["validado_contra"] = dict(fatos_sha=sha, data=datetime.now().strftime("%Y-%m-%d %H:%M"))
        _w(BPMN / "avaliacao_CONV.json", av)


ETAPAS = dict(auditoria=etapa_auditoria, normas=etapa_normas, conformidade=etapa_conformidade, avaliacao=etapa_avaliacao, linha_base=etapa_linha_base, tobe=etapa_tobe,
              montar_controles=lambda: __import__("runpy").run_path(str(Path(__file__).parent / "controles_agergs.py")),
              controles=etapa_controles)

# ================================================================ fase 4: priorização da automação
# Critérios, pesos e réguas de metodologia-repo/scripts/comum.py (PRIORIZACAO_CRITERIOS); premissas de custo: HIPÓTESE.
CRITERIOS = {"volume": (25, (5, 10, 25, 50)), "analise": (15, (0.2, 0.35, 0.5, 0.65)),
             "dados": (15, (0.3, 0.45, 0.6, 0.75)), "regras": (20, (0.4, 0.55, 0.7, 0.85)),
             "padrao": (15, (0.3, 0.4, 0.5, 0.6)), "completude": (10, (0.2, 0.35, 0.5, 0.65))}
NATUREZAS_ANALISE = {"analise_juridica", "analise_tecnica_engenharia", "analise_economico_financeira",
                     "relatoria_decisao", "auditoria_conferencia"}
FRACAO_AUTOMATIZAVEL = {"alto": (0.4, 0.6, 0.8), "médio": (0.15, 0.3, 0.45), "baixo": (0.0, 0.05, 0.1)}
HORAS_CAPACIDADE = {"automação de tramitação (RPA no SEI)": 40, "monitoramento de prazos e alertas": 24,
                    "painel e indicadores": 24, "classificação e triagem": 60, "extração de dados de documentos": 80,
                    "sumarização e linha do tempo": 40, "busca de precedentes e normas": 60,
                    "verificação de conformidade": 100, "cálculo e conferência automática": 80,
                    "redação assistida de minuta": 80}
HORAS_PLATAFORMA, HORAS_CONFIG_ATIVIDADE, CASOS_VALIDACAO, HORAS_VALIDACAO_CASO = 160, 16, 30, 2
CUSTO_HORA_DEV = (220, 150, 100)
MANUTENCAO_ANUAL, HORIZONTE_ANOS = 0.2, 5


def _nota(v, cortes):
    return 1 + sum(v >= c for c in cortes)


def etapa_priorizacao():
    F4 = SAIDA / "fase4"
    F4.mkdir(exist_ok=True)
    casos, narr, fichas = _contexto()
    av = _j(BPMN / "avaliacao_CONV.json")
    proc = _j(F2 / "procedimento_CONV.json")
    fc = [f for f in fichas if f["processo"] in casos and f["autoria"] == "AGERGS"]
    h_tot = sum(f["horas_teto"] for f in fc) or 1
    anal = [f for f in fc if f.get("natureza_trabalho") in NATUREZAS_ANALISE]
    tar_h = {}
    for c in casos.values():
        for o in c["ocorrencias"]:
            tar_h[o["atividade"]] = tar_h.get(o["atividade"], 0) + o["horas_teto"]
    h_alto = sum(h for t, h in tar_h.items() if av["atividades"].get(t, {}).get("potencial_ia") == "alto")
    mais_freq = max(x["casos"] for x in proc["caminhos"]) / len(casos)
    metr = dict(
        volume=VOLUME_ANUAL["valor"],
        analise=round(sum(f["horas_teto"] for f in anal) / h_tot, 3),
        dados=round(sum(1 for f in anal if any(i.get("ancorado") for i in f.get("insumos") or [])) / max(1, len(anal)), 3),
        regras=round(sum(1 for f in anal if any(n.get("ancorado") for n in f.get("normas_citadas") or [])) / max(1, len(anal)), 3),
        padrao=round((sum((f.get("composicao_texto") or {}).get("pct_padrao", 0) for f in fc) / max(1, len(fc)) / 100 + mais_freq) / 2, 3),
        completude=round(h_alto / max(1e-9, sum(tar_h.values())), 3))
    notas = {k: _nota(v, CRITERIOS[k][1]) for k, v in metr.items()}
    composta = round(sum(CRITERIOS[k][0] * notas[k] for k in notas) / 5, 1)
    # custo × retorno por cenário: atividades com potencial alto/médio automatizadas
    lb = _j(F3 / "linha_base_CONV.json")
    vol = VOLUME_ANUAL["valor"]
    ativ = []
    caps = set()
    for t, h in sorted(tar_h.items()):
        a = av["atividades"].get(t, {})
        pot = a.get("potencial_ia", "baixo")
        h_ano = h / len(casos) * vol
        ativ.append(dict(atividade=t, potencial_ia=pot, tipos_ia="; ".join(a.get("tipos_ia", [])), horas_teto_ano=round(h_ano, 1),
                         **{f"horas_liberadas_{c}": round(h_ano * FRACAO_AUTOMATIZAVEL[pot][i], 1) for i, c in enumerate(CENARIOS)}))
        if pot in ("alto", "médio"):
            caps |= set(a.get("tipos_ia", []))
    n_auto = sum(1 for x in ativ if x["potencial_ia"] in ("alto", "médio"))
    h_constr = HORAS_PLATAFORMA + sum(HORAS_CAPACIDADE.get(c, 40) for c in sorted(caps)) + n_auto * HORAS_CONFIG_ATIVIDADE
    h_incr = sum(HORAS_CAPACIDADE.get(c, 40) for c in sorted(caps) if c not in ("redação assistida de minuta", "verificação de conformidade", "extração de dados de documentos", "sumarização e linha do tempo")) + n_auto * HORAS_CONFIG_ATIVIDADE
    cen = {}
    for i, c in enumerate(CENARIOS):
        h_lib = sum(x[f"horas_liberadas_{c}"] for x in ativ)
        ret = h_lib * CUSTO_HORA["esperado"]
        constr = h_constr * CUSTO_HORA_DEV[i] + CASOS_VALIDACAO * HORAS_VALIDACAO_CASO * CUSTO_HORA["esperado"]
        incr = h_incr * CUSTO_HORA_DEV[i] + CASOS_VALIDACAO * HORAS_VALIDACAO_CASO * CUSTO_HORA["esperado"]
        manut = MANUTENCAO_ANUAL * constr
        cen[c] = dict(horas_liberadas_ano=round(h_lib, 1), retorno_ano=round(ret), custo_construcao_isolado=round(constr),
                      custo_construcao_incremental=round(incr), manutencao_ano=round(manut),
                      liquido_ano_isolado=round(ret - manut),
                      payback_anos_isolado=round(constr / (ret - manut), 1) if ret > manut else None,
                      payback_anos_incremental=round(incr / (ret - MANUTENCAO_ANUAL * incr), 1) if ret > MANUTENCAO_ANUAL * incr else None,
                      saldo_5_anos_isolado=round(HORIZONTE_ANOS * (ret - manut) - constr))
    portoes = dict(volume_minimo=dict(regra="≥ 10 processos/ano (régua nota 3)", ok=metr["volume"] >= 10),
                   procedimento=dict(regra="situação 'procedimento' (≥ 5 casos e auditoria ≥ 85%)", ok=proc["situacao"] == "procedimento"),
                   padrao=dict(regra="caminho mais frequente ≥ 30% dos casos", ok=mais_freq >= 0.3))
    out = dict(codigo="CONV", processo=lb["nome"], metricas=metr, notas=notas, pesos={k: v[0] for k, v in CRITERIOS.items()},
               nota_composta=composta, portoes_piloto=portoes,
               prioridade="piloto" if all(p["ok"] for p in portoes.values()) and composta >= 60 else "não recomendado como piloto de automação completa",
               referencia_agenersa="P01 (reajuste tarifário) teve nota 80,0 e foi indicado como piloto no caso de referência",
               atividades=ativ, capacidades=sorted(caps), horas_construcao=dict(isolado=h_constr, incremental=h_incr),
               cenarios=cen, premissas=dict(volume_anual=VOLUME_ANUAL, custo_hora=CUSTO_HORA, custo_hora_dev=CUSTO_HORA_DEV,
                                            fracao_automatizavel=FRACAO_AUTOMATIZAVEL, hipotese=True))
    _w(F4 / "matriz_automacao_CONV.json", out)
    with open(F4 / "matriz_automacao_CONV.csv", "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(ativ[0]))
        w.writeheader()
        w.writerows(ativ)
    print(f"priorização: nota {composta} {notas}; portões {[k for k, p in portoes.items() if not p['ok']]} falham; "
          f"esperado: retorno R$ {cen['esperado']['retorno_ano']}/ano × construção R$ {cen['esperado']['custo_construcao_isolado']}")


ETAPAS["priorizacao"] = etapa_priorizacao


if __name__ == "__main__":
    pedidas = sys.argv[1:] or list(ETAPAS)
    for e in pedidas:
        print(f"[{e}]")
        try:
            ETAPAS[e]()
        except Portao as x:
            print("PORTÃO FALHOU:", x)
            sys.exit(1)
