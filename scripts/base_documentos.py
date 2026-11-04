"""Fase 0 adaptada: monta a base de documentos a partir dos PDFs exportados do SEI-RS.

Os PDFs não trazem andamentos; cada página tem rodapé "Nome (id) SEI nnn / pg. N" e as peças
nativas trazem "Documento assinado eletronicamente por X, cargo, em dd/mm/aaaa".
Saída: dados/documentos.csv, dados/assinaturas.csv e dados/docs/<proc>/<seq>_<id>.txt
"""
import csv, re, sys, unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
TXT = RAIZ / "textos"
DADOS = RAIZ / "dados"
RODAPE = re.compile(r"^\s*(?P<nome>\S.*?)\s*\((?P<id>\d{6,8})\)\s+SEI\s+(?P<proc>[\d\-./]+)\s*/\s*pg\.\s*(?P<pg>\d+)\s*$")
ASSIN = re.compile(r"Documento assinado eletronicamente por (?P<quem>.+?), (?P<cargo>.+?), em (?P<data>\d{2}/\d{2}/\d{4}), às (?P<hora>\d{2}:\d{2})")

def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "_", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()).strip("_")

def main():
    DADOS.mkdir(exist_ok=True)
    docs, assins = [], []
    for arq in sorted(TXT.glob("*.txt")):
        m = re.match(r"SEI_(\S+)\s+(.*)\.txt", arq.name)
        proc_num, nome_proc = m.group(1), m.group(2)
        cod = slug(nome_proc)
        paginas = arq.read_text(errors="replace").split("\f")
        grupos = []  # (id, nome, [textos])
        for pg in paginas:
            linhas = [l for l in pg.splitlines() if l.strip()]
            rod = None
            for l in reversed(linhas[-4:]):
                r = RODAPE.match(l)
                if r:
                    rod = r; break
            if not pg.strip():
                continue
            did, dnome = (rod.group("id"), rod.group("nome")) if rod else (None, None)
            if grupos and (did is None or grupos[-1][0] == did):
                grupos[-1][2].append(pg)
                if grupos[-1][0] is None and did:
                    grupos[-1][0], grupos[-1][1] = did, dnome
            else:
                grupos.append([did, dnome, [pg]])
        outdir = DADOS / "docs" / cod
        outdir.mkdir(parents=True, exist_ok=True)
        for seq, (did, dnome, pgs) in enumerate(grupos, 1):
            texto = "\f".join(pgs)
            flat = re.sub(r"\s+", " ", texto)
            ass = [a.groupdict() for a in ASSIN.finditer(flat)]
            nchar = len(re.sub(r"\s+", "", texto))
            (outdir / f"{seq:03d}_{did or 'semid'}.txt").write_text(texto)
            datas = sorted({tuple(reversed(a["data"].split("/"))) for a in ass})
            docs.append(dict(processo=cod, numero_sei=proc_num, seq=seq, doc_id=did or "", nome=dnome or "",
                             paginas=len(pgs), caracteres=nchar, n_assinaturas=len(ass),
                             data_primeira_assinatura="-".join(datas[0]) if datas else "",
                             data_ultima_assinatura="-".join(datas[-1]) if datas else "",
                             nativo=bool(ass), baixo_texto=nchar < 200 * len(pgs)))
            for a in ass:
                d, mth, y = a["data"].split("/")
                assins.append(dict(processo=cod, seq=seq, doc_id=did or "", nome_doc=dnome or "",
                                   signatario=a["quem"].strip(), cargo=a["cargo"].strip(), data=f"{y}-{mth}-{d}", hora=a["hora"]))
    for nome, linhas in (("documentos.csv", docs), ("assinaturas.csv", assins)):
        with open(DADOS / nome, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)
    print(len(docs), "documentos;", len(assins), "assinaturas")

if __name__ == "__main__":
    main()
