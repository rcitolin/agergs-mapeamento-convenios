# Conformidade legal — celebração de instrumento de delegação da regulação

Requisitos em `saida/fase3/normas_CONV.json`. Cada trecho é cópia literal do texto integral da norma, conferida por `scripts/fase3_agergs.py normas` (`saida/fase3/verificacao_normas_CONV.json`). O teste de cada requisito roda por código em cada caso (`saida/fase3/conformidade_CONV.csv`).

## Base normativa

| Arquivo | Norma | Fonte | Situação | Observação |
|---|---|---|---|---|
| `normas/lei_11445_2007.txt` | Lei Federal 11.445/2007 (saneamento básico; texto consolidado com Lei 14.026/2020) | https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2007/lei/l11445.htm | ok | Planalto, texto consolidado. Arts. 8, 8-A, 8-B, 9, 21, 23, 25-A conferidos. |
| `normas/lei_14133_2021.txt` | Lei Federal 14.133/2021 (licitações e contratos) | https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm | ok | Planalto. Arts. 74 (inexigibilidade), 184 (aplicação subsidiária) e 184-A (convênios com a União) conferidos. |
| `normas/lei_14026_2020.txt` | Lei Federal 14.026/2020 (novo marco do saneamento) | https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/lei/l14026.htm | ok | Planalto. Texto de alteração da Lei 11.445 e da Lei 9.984 (ANA). |
| `normas/lei_11107_2005.txt` | Lei Federal 11.107/2005 (consórcios públicos) | https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2005/lei/l11107.htm | ok | Planalto, texto integral. Norma geral de consórcios públicos (base legal dos convênios de cooperação entre entes). |
| `normas/decreto_6017_2007.txt` | Decreto 6.017/2007 (regulamenta a Lei 11.107/2005) | https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2007/decreto/d6017.htm | ok | Planalto. Obtido com URL _ato2007-2010 (a URL _ato2004-2006 retornou 404). |
| `normas/lei_9784_1999.txt` | Lei Federal 9.784/1999 (processo administrativo federal) | https://www.planalto.gov.br/ccivil_03/leis/l9784.htm | ok | Planalto. Aplicável subsidiariamente só à Administração federal; usar como referência de princípios. |
| `normas/lei_rs_10931_1997_agergs.txt` | Lei RS 10.931/1997 (cria a AGERGS) - texto original | https://www.legisweb.com.br/legislacao/?id=153701 | ok | Fonte NAO oficial (LegisWeb; DOE-RS 10/01/1997 nao acessado). Marcada como REVOGADA pela Lei RS 16.266/2024. Arts. 7 e 8 com redacao da Lei 11.292/1998. Conferir com DOE-RS / AL-RS. |
| `normas/lei_rs_16266_2024_agergs_vigente.txt` | Lei RS 16.266/2024 (AGERGS vigente, revoga a Lei 10.931/1997) | https://www.normasbrasil.com.br/norma/lei-16266-2024-rs_471327.html | ok | Fonte secundaria (normasbrasil), nao oficial. Art. 2 trata da regulacao de servicos de titularidade municipal delegados a AGERGS por instrumento convenial ou contratual. Conferir com DOE-RS / AL-RS. |
| `normas/lei_rs_15612_2021_processo_adm.txt` | Lei RS 15.612/2021 (processo administrativo no RS) | https://www.legisweb.com.br/legislacao/?id=413912 | ok | Fonte NAO oficial (LegisWeb). Texto integral obtido, sem conferencia com DOE-RS/AL-RS. |
| `normas/resolucao_ana_177_2024_NR4_parcial.txt` | Resolução ANA 177/2024 (aprova NR 4/2024, governança de ERIs) | https://www.lex.com.br/resolucao-ana-no-177-de-12-de-janeiro-de-2024/ | incompleto | Apenas preambulo e arts. 1-2 da resolucao (LEX). O ANEXO (texto da NR 4/2024) e exclusivo para assinantes e NAO foi obtido. Pendente: manual gov.br https://www.gov.br/ana/pt-br/assuntos/saneamento-basico/Normativos-publicados-pela-ANA/manual-nr4-final.pdf (manual, nao a norma) ou DOU. Nao e sobre delegacao; a delegacao esta na NR 9/2024 (Res. ANA 211/2024), nao baixada. |

**Ressalvas.**
- As Leis RS 10.931/1997, 15.612/2021 e 16.266/2024 vieram de fonte secundária (LegisWeb e Normas Brasil). Conferir no DOE-RS ou na AL-RS antes de citar como texto oficial.
- A Lei 10.931/1997 foi revogada pela Lei RS 16.266/2024, que é a norma vigente da AGERGS.
- A Resolução ANA 177/2024 (NR 4) está só parcial na base, e a NR 9/2024 não foi obtida.
- Leis RS 16.266/2024 e 15.612/2021 vieram de fonte secundária (ver normas/indice.json): conferir no DOE-RS antes de citar como texto oficial. Lei 8.666/1993 (regime dos convênios de 2018–2020) não está na base: o requisito de prazo de publicação só é testado nos instrumentos assinados na vigência da Lei 14.133/2021.

## Requisitos e resultado

| Requisito | Norma | Trecho literal | Requisito testado | Literal conferido | Casos aplicáveis | % conforme |
|---|---|---|---|---|---|---|
| R-CONV-01 | Lei Federal 11.445/2007, art. 23, § 1º (redação da Lei 14.026/2020) | “o ato de delegação explicitará a forma de atuação e a abrangência das atividades a serem desempenhadas pelas partes envolvidas” | O instrumento de delegação (convênio ou contrato) assinado está nos autos e define forma de atuação e abrangência | sim | 18 | 66,7% |
| R-CONV-02 | Lei Estadual RS 16.266/2024, art. 2º (AGERGS) | “delegados à Agência por instrumento convenial ou contratual” | A competência da AGERGS sobre serviço municipal nasce de instrumento convenial ou contratual: sem instrumento assinado não há regulação delegada | sim | 0 | fundamento (sem teste) |
| R-CONV-03 | Lei Federal 14.133/2021, art. 72 | “parecer jurídico e pareceres técnicos, se for o caso, que demonstrem o atendimento dos requisitos exigidos” | Há parecer jurídico (DAJ ou PSE) nos autos antes da assinatura do instrumento | sim | 12 | 50% |
| R-CONV-04 | Lei Federal 14.133/2021, art. 72 | “autorização da autoridade competente” | Há autorização da Presidência, da Diretoria-Geral ou deliberação do Conselho antes da assinatura | sim | 12 | 16,7% |
| R-CONV-05 | Lei Federal 14.133/2021, art. 72 | “O ato que autoriza a contratação direta ou o extrato decorrente do contrato deverá ser divulgado e mantido à disposição do público em sítio eletrônico oficial” | O extrato do instrumento assinado é publicado e a publicação está nos autos | sim | 12 | 66,7% |
| R-CONV-06 | Lei Federal 14.133/2021, art. 94 | “deverá ocorrer nos seguintes prazos, contados da data de sua assinatura: I - 20 (vinte) dias úteis, no caso de licitação; II - 10 (dez) dias úteis, no caso de contratação direta” | Divulgação do extrato em até 10 dias úteis da assinatura (contratação direta); a publicação no DOE nos autos é o indicador disponível (o PNCP não aparece nos processos) | sim | 5 | 20% |
| R-CONV-07 | Lei Federal 14.133/2021, art. 184 | “Aplicam-se as disposições desta Lei, no que couber e na ausência de norma específica, aos convênios, acordos, ajustes e outros instrumentos congêneres” | O rito da Lei 14.133 (instrução, parecer, autorização, publicação) vale também para os convênios de delegação | sim | 0 | fundamento (sem teste) |
| R-CONV-08 | Lei Federal 14.133/2021, art. 74 | “É inexigível a licitação quando inviável a competição” | Nos contratos de prestação de serviços de regulação, a justificativa de inexigibilidade e a razão da escolha da AGERGS estão nos autos do processo de celebração | sim | 5 | 0% |
| R-CONV-09 | Lei Estadual RS 15.612/2021, arts. 29 e 53 | “Concluída a instrução de processo administrativo, a Administração tem o prazo de até 30 (trinta) dias para decidir, prorrogável por igual período, havendo motivo justificado” | Da última peça de instrução (análise técnica, jurídica ou da PSE) até a autorização ou assinatura: até 30 dias, medidos como 21 dias úteis (aproximação de 30 dias corridos) | sim | 6 | 33,3% |
| R-CONV-10 | Lei Estadual RS 15.612/2021, arts. 29 e 53 | “Inexistindo disposição específica, os atos do órgão ou autoridade responsável pelo processo e dos administrados que dele participem devem ser praticados no prazo de 5 (cinco) dias, salvo motivo de força maior” | Cada ato interno da AGERGS sem prazo próprio sai em até 5 dias da peça anterior (lidos como dias úteis, leitura favorável ao órgão); medido por ocorrência de tarefa interna | sim | 18 | 74,6% |

R-CONV-10 é medido por ocorrência de tarefa interna: o valor do caso é a % das ocorrências dentro do prazo, e o resultado é a média entre os casos.

## Resultado por caso

| Caso | R-CONV-01 | R-CONV-03 | R-CONV-04 | R-CONV-05 | R-CONV-06 | R-CONV-08 | R-CONV-09 | R-CONV-10 |
|---|---|---|---|---|---|---|---|---|
| Alecrim | ✔ | ✘ | ✘ | ✘ | n/a | n/a | n/a | 50% |
| Arambare | ✔ | ✔ | ✘ | ✘ | n/a | n/a | ✘ | 70% |
| Campinas das Missoes | ✔ | ✘ | ✘ | ✘ | n/a | n/a | n/a | 80% |
| Capao Bonito do Sul | ✘ | n/a | n/a | n/a | n/a | n/a | n/a | 83,3% |
| Chiapetta | ✘ | n/a | n/a | n/a | n/a | n/a | n/a | 100% |
| Jaguari | ✘ | n/a | n/a | n/a | n/a | n/a | n/a | 66,7% |
| Lagoa Bonita do Sul | ✔ | ✘ | ✘ | ✔ | ✘ | ✘ | n/a | 50% |
| Liberato Salzano | ✔ | ✔ | ✘ | ✔ | n/a | n/a | ✘ | 66,7% |
| Mapituba | ✘ | n/a | n/a | n/a | n/a | n/a | n/a | 66,7% |
| Mata | ✘ | n/a | n/a | n/a | n/a | n/a | n/a | 83,3% |
| Minas do Leao | ✔ | ✔ | ✔ | ✔ | ✘ | ✘ | ✘ | 86,2% |
| Nova Brescia | ✔ | ✘ | ✘ | ✔ | ✔ | ✘ | n/a | 100% |
| Panambi | ✔ | ✘ | ✘ | ✘ | n/a | n/a | n/a | 50% |
| Passa Sete | ✔ | ✘ | ✘ | ✔ | ✘ | ✘ | n/a | 100% |
| Passo Fundo | ✔ | ✔ | ✔ | ✔ | ✘ | ✘ | ✔ | 69% |
| Salvador do Sul | ✔ | ✔ | ✘ | ✔ | n/a | n/a | ✔ | 66,7% |
| Unistalda | ✘ | n/a | n/a | n/a | n/a | n/a | n/a | 80% |
| Vila nova do Sul | ✔ | ✔ | ✘ | ✔ | n/a | n/a | ✘ | 75% |

n/a = o requisito não se aplica ao caso (sem assinatura nos autos, instrumento anterior à Lei 14.133/2021 ou não é contrato). O detalhe de cada teste está na coluna `detalhe` de `saida/fase3/conformidade_CONV.csv`.

## Leitura

- Os testes medem o que está **nos autos** do processo de celebração. Peça que existe em outro processo (inexigibilidade e TAAC dos contratos de 2025) conta como ausente. Esse é o achado de R-CONV-08: a instrução está fragmentada entre processos.
- R-CONV-06 usa a publicação no DOE como indicador, porque o PNCP não aparece nos processos. O prazo conta da assinatura; nos convênios de 2013–2020, regidos pela Lei 8.666, o teste não se aplica.
- R-CONV-09 mede 30 dias como 21 dias úteis (aproximação). R-CONV-10 lê os 5 dias do art. 29 como úteis, leitura favorável ao órgão.
