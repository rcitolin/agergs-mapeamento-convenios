"""Gera o BPMN 2.0 e o visualizador com o gerador do repositório (metodologia-repo/scripts/gerar_bpmn.py),
apontando para as saídas da AGERGS. Uso: python3 scripts/gerar_bpmn_agergs.py"""
import json
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
REPO = RAIZ.parent / "metodologia-repo"
os.environ.setdefault("PERFIL", "rs_agergs")
sys.path.insert(0, str(REPO / "scripts"))
import gerar_bpmn as g  # noqa: E402

g.DIR = RAIZ / "saida" / "bpmn"
g.F2 = RAIZ / "saida" / "fase2"
g.ORDEM_CODIGOS = ["CONV", "CONV-TOBE"]
_proc = g.procedimento


def procedimento(cod):
    p = _proc(cod)
    if p and "transicoes_por_origem" in p:
        p["transicoes"] = p["transicoes_por_origem"]
    return p


g.procedimento = procedimento
sys.argv = [sys.argv[0], "--modelos", str(g.DIR), "--visualizador", str(RAIZ / "docs" / "bpmn")]
g.main()
