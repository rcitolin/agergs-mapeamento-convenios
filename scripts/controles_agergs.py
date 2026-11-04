"""Monta saida/fase3/controles_CONV.json: indicadores (definição escrita aqui) com linha de base lida dos fatos e da
conformidade e metas lidas da simulação (resultado_tobe_CONV.json). Nenhum número é digitado.
Uso: python3 scripts/controles_agergs.py  (depois: python3 scripts/fase3_agergs.py controles)"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
S = RAIZ / "saida"
r = json.loads((S / "fase3" / "resultado_tobe_CONV.json").read_text())
F = {f["id"]: f["valor"] for f in json.loads((S / "bpmn" / "fatos_CONV.json").read_text())["fatos"]}
conf = json.loads((S / "fase3" / "conformidade_CONV.json").read_text())["requisitos"]


def meta(path):
    o = r
    for k in path.split("."):
        o = o[k]
    return {"valor": o, "origem": {"tipo": "simulacao", "ref": path}}


def metas(tmpl):
    return [{"fase": int(f), **meta(tmpl.format(f=f))} for f in "123"]


def lb_conf(req):
    v = conf[req]["pct_conforme"]
    return {"valor": 0.0 if v is None else v, "unidade": "%", "fato": f"conformidade.{req}"}


ind = [
    dict(id="I-CONV-01", nome="Lead time da celebração",
         definicao="Dias úteis da primeira peça datada do processo (pedido ou autuação) à última peça (publicação, comunicado ou encerramento); mediana dos processos encerrados no período",
         calculo={"tipo": "lead", "atividades": ["t1", "t15"]}, fonte_dados="peças e andamentos do SEI", frequencia="trimestral",
         linha_base={"valor": F["coorte.caso.lead.mediana"], "unidade": "du", "fato": "coorte.caso.lead.mediana"},
         metas=metas("fases.{f}.esperado.lead.mediana"),
         alerta={"regra": "Processo aberto com idade acima do q3 simulado da fase vigente", "destinatario": "Dono do processo (DAI) e Diretoria-Geral"},
         melhorias=["M-CONV-04", "M-CONV-05", "M-CONV-06", "M-CONV-07"], responsavel="DAI"),
    dict(id="I-CONV-02", nome="Divulgação do extrato em até 10 dias úteis da assinatura",
         definicao="% dos instrumentos assinados com extrato publicado em até 10 du da última assinatura",
         calculo={"tipo": "conformidade", "requisito": "R-CONV-06"}, fonte_dados="peças do SEI e DOE", frequencia="mensal",
         linha_base=lb_conf("R-CONV-06"), metas=metas("fases.{f}.esperado.conformidade_temporal.R-CONV-06"),
         referencia_legal="100% (Lei 14.133, art. 94, II)",
         observacao="O TO-BE não chega a 100% porque a espera pela assinatura do município é tempo de terceiro: exige assinatura eletrônica e prazo contratual para o município assinar.",
         alerta={"regra": "Instrumento assinado há 7 du sem extrato publicado", "destinatario": "DG"},
         melhorias=["M-CONV-05", "M-CONV-09"], responsavel="DG"),
    dict(id="I-CONV-03", nome="Decisão em até 30 dias após a instrução",
         definicao="% dos processos com autorização, deliberação ou assinatura em até 21 du da última peça de instrução",
         calculo={"tipo": "conformidade", "requisito": "R-CONV-09"}, fonte_dados="peças do SEI", frequencia="trimestral",
         linha_base=lb_conf("R-CONV-09"), metas=metas("fases.{f}.esperado.conformidade_temporal.R-CONV-09"),
         referencia_legal="100% (Lei RS 15.612, art. 53)",
         alerta={"regra": "15 du desde a última instrução sem decisão", "destinatario": "Gabinete da Presidência"},
         melhorias=["M-CONV-04"], responsavel="GP"),
    dict(id="I-CONV-04", nome="Atos internos em até 5 dias",
         definicao="% das ocorrências de tarefa interna com espera antes de até 5 du",
         calculo={"tipo": "conformidade", "requisito": "R-CONV-10"}, fonte_dados="peças do SEI", frequencia="mensal",
         linha_base=lb_conf("R-CONV-10"), metas=metas("fases.{f}.esperado.conformidade_temporal.R-CONV-10"),
         referencia_legal="100% (Lei RS 15.612, art. 29)",
         alerta={"regra": "Processo parado há 5 du na mesma unidade", "destinatario": "Unidade com o processo e DAI"},
         melhorias=["M-CONV-04", "M-CONV-06", "M-CONV-07"], responsavel="DAI"),
    dict(id="I-CONV-05", nome="Horas de trabalho por celebração",
         definicao="Horas-teto estimadas das peças da AGERGS por processo (mediana); calibrar com medição de tempo",
         calculo={"tipo": "horas"}, fonte_dados="peças do SEI + calibração", frequencia="semestral",
         linha_base={"valor": F["coorte.caso.horas_teto.mediana"], "unidade": "h", "fato": "coorte.caso.horas_teto.mediana"},
         metas=metas("fases.{f}.esperado.horas_teto.mediana"),
         alerta={"regra": "Processo acima do q3 de horas", "destinatario": "DAI"},
         melhorias=["M-CONV-03", "M-CONV-08", "M-CONV-11", "M-CONV-12"], responsavel="DAI"),
    dict(id="I-CONV-06", nome="Retornos por caso (qualidade)",
         definicao="Número de retornos a atividade já realizada (nova análise jurídica, nova minuta, reenvio) por processo; mediana",
         calculo={"tipo": "laco", "atividades": ["t5", "t6", "t10"]}, fonte_dados="peças do SEI", frequencia="trimestral",
         linha_base={"valor": F["coorte.caso.retornos.mediana"], "unidade": "retornos", "fato": "coorte.caso.retornos.mediana"},
         metas=[], observacao="Indicador de qualidade sem meta simulada: acompanha se a redução de prazo não empurra retrabalho.",
         alerta={"regra": "Terceira versão de minuta no mesmo processo", "destinatario": "DAJ"},
         melhorias=["M-CONV-01", "M-CONV-02"], responsavel="DAJ"),
    dict(id="I-CONV-07", nome="Parecer jurídico antes da assinatura",
         definicao="% dos instrumentos assinados com informação jurídica da DAJ ou da PSE nos autos antes da assinatura",
         calculo={"tipo": "conformidade", "requisito": "R-CONV-03"}, fonte_dados="peças do SEI", frequencia="trimestral",
         linha_base=lb_conf("R-CONV-03"), metas=[{"fase": 1, "valor": 100, "origem": {"tipo": "norma", "ref": "R-CONV-03"}}],
         alerta={"regra": "Minuta enviada para assinatura sem parecer nos autos", "destinatario": "DAJ"},
         melhorias=["M-CONV-03"], responsavel="DAJ"),
    dict(id="I-CONV-08", nome="Instrução completa no processo de celebração",
         definicao="% dos contratos com justificativa de inexigibilidade e autorização no próprio processo",
         calculo={"tipo": "conformidade", "requisito": "R-CONV-08"}, fonte_dados="peças do SEI", frequencia="trimestral",
         linha_base=lb_conf("R-CONV-08"), metas=[{"fase": 1, "valor": 100, "origem": {"tipo": "norma", "ref": "R-CONV-08"}}],
         alerta={"regra": "Contrato encaminhado à assinatura sem inexigibilidade nos autos", "destinatario": "GP"},
         melhorias=["M-CONV-02"], responsavel="GP"),
]
ctl = dict(codigo="CONV", indicadores=ind, controles_qualidade_ia=[
    dict(id="Q-CONV-01", melhorias=["M-CONV-10"],
         verificacao="Cada pendência e cada dado extraído (escopo, prestador, número e data da lei) conferido contra a peça de origem",
         amostragem="100% das listas de pendência; 2 processos por mês refeitos sem IA",
         criterio_aceite="Nenhuma pendência falsa enviada ao município; nenhum documento obrigatório omitido",
         indicador="taxa de erro de extração (campos corrigidos / campos extraídos)",
         meta="0 pendência indevida enviada; erro de extração até 5% dos campos (hipótese a calibrar)", responsavel="DAI"),
    dict(id="Q-CONV-02", melhorias=["M-CONV-11"],
         verificacao="Diferença entre a minuta gerada e a minuta padrão; cada citação de norma conferida contra o texto integral",
         amostragem="100% das minutas", criterio_aceite="Minuta assinada sem desvio não justificado e sem erro material",
         indicador="desvios não justificados e erratas por instrumento", meta="0 errata de publicação por erro material", responsavel="DAJ"),
    dict(id="Q-CONV-03", melhorias=["M-CONV-12"],
         verificacao="Conclusão e fundamentos da pré-análise conferidos pelo assessor; citações conferidas contra a base normativa",
         amostragem="100% das citações; 1 pré-análise por mês refeita às cegas",
         criterio_aceite="Nenhuma citação inválida em peça assinada",
         indicador="taxa de citação inválida e de conclusão divergente na amostra cega",
         meta="0 citação inválida; divergência de conclusão registrada e analisada", responsavel="DAJ e Conselho Superior")],
    auditoria_continua=["Testes R-CONV-01 a R-CONV-10 rodando a cada processo encerrado (scripts/fase3_agergs.py conformidade)"])
(S / "fase3" / "controles_CONV.json").write_text(json.dumps(ctl, ensure_ascii=False, indent=1))
print("controles_CONV.json:", len(ind), "indicadores")
