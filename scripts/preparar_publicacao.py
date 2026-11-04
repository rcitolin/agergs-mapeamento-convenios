"""Prepara docs/site/index.html para publicação como página: tira o esqueleto (o publicador o acrescenta),
ajusta título, margens seguras e o caminho do visualizador BPMN. Saída: publicacao/index.html e publicacao/bpmn/index.html"""
import re
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
OUT = RAIZ / "publicacao"
(OUT / "bpmn").mkdir(parents=True, exist_ok=True)
s = (RAIZ / "docs" / "site" / "index.html").read_text(encoding="utf-8")
s = re.sub(r"<!doctype html><html[^>]*><head>.*?(?=<title>)", "", s, flags=re.S | re.I)
s = re.sub(r"<title>.*?</title>", '<title>Mapeamento de Convênios AGERGS</title>'
           '<meta name="claude:viewport-fit-sides" content="cover">', s, count=1)
s = s.replace("</style></head><body>", "\nheader,main,nav{padding-left:max(16px,env(safe-area-inset-left,0px));"
              "padding-right:max(16px,env(safe-area-inset-right,0px))}"
              "nav{top:env(safe-area-inset-top,0px)}"
              'body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}'
              "</style>")
s = re.sub(r"</body>\s*</html>\s*$", "", s)
s = s.replace('src="../bpmn/index.html"', 'src="bpmn/index.html"')
(OUT / "index.html").write_text(s, encoding="utf-8")
shutil.copy(RAIZ / "docs" / "bpmn" / "index.html", OUT / "bpmn" / "index.html")
print("publicacao/index.html e publicacao/bpmn/index.html")
