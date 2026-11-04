# Fase 0 — base documental, trilhas e indicadores por processo

04/11/2026 · base: 20 processos SEI da AGERGS exportados em PDF (18 casos de celebração — convênios, contratos de
delegação da regulação e um termo aditivo — e 2 processos de gestão de 2026). Planilha:
`saida/Mapeamento_AGERGS_Celebracao.xlsx`. Scripts: `scripts/base_documentos.py` e `scripts/pipeline_agergs.py`.
Perfil do órgão: `metodologia-repo/perfis/rs_agergs.py`.

Atualização: entraram 6 processos (Alecrim, Campinas das Missões, Chiapetta, Liberato Salzano, Salvador do Sul e
Unistalda). Os 321 documentos da primeira rodada mantiveram numeração e conteúdo; os números agregados abaixo já são
os da base de 18 casos.

## 1. O que foi reconstruído

| Item | Quantidade |
|---|---|
| PDFs exportados do SEI | 20 (2.317 páginas) |
| Documentos (peças) identificados pelo rodapé "Nome (id) SEI … / pg. N" | 381 (358 nos 18 casos de celebração; 23 nos 2 processos de gestão) |
| Assinaturas eletrônicas lidas ("Documento assinado eletronicamente por …") | 233 |
| Peças nativas do SEI (com assinatura eletrônica) | 201 |
| Peças com pouco texto extraível (digitalizadas, imagem ou codificação corrompida) | 33 |
| Andamentos do SEI | **0**: o PDF exportado não traz o histórico de tramitação |

**Diferença em relação ao caso de referência.** Na AGENERSA a trilha vem dos andamentos da Pesquisa Pública do
SEI-RJ (quem abriu, quem recebeu, quando). Aqui só há as peças. A trilha foi reconstruída assim:

1. **Data de cada peça**: a data da primeira assinatura eletrônica (189 peças dos casos). Sem assinatura, vale a data
   escrita no texto, extraída na ficha (102 peças: ofícios do município, publicações no DOE, leis). As outras 67 peças
   herdam a data corrente do processo, uma aproximação da data de juntada.
2. **Unidade de cada peça**: o cargo do signatário (Conselheiro-Presidente → GP; Diretor-Geral → DG; OAB ou Assuntos
   Jurídicos → DAJ; Procuradoria Setorial → PSE; e assim por diante), ou a unidade escrita na ficha quando não há
   assinatura. Peças do município e do prestador ficam como MUN e EXT.
3. **Início do processo**: a primeira peça datada, **na ordem dos autos**, que não é anexo histórico. Leis municipais,
   planos e contratos de programa juntados pelo município não contam como início. Uma data escrita só no texto e
   anterior a esse início não é usada: a peça herda a data corrente. Essa regra nova veio de Campinas das Missões, cuja
   minuta traz "18 de maio de 2015" embora o pedido seja de 07/01/2016 (correção registrada em `docs/MITIGACOES.md`).
4. **Espera e posse**: a espera antes de cada atividade é o intervalo, em dias úteis (calendário do RS, com 20/09, de
   2010 a 2028), entre a última peça da atividade anterior e a primeira desta. Ela é atribuída à unidade que age em
   seguida. **Tempo de terceiro** (protegido no TO-BE) é só a espera antes de peça do município ou do prestador que
   responde a algo da AGERGS. Peça externa logo depois de outra peça externa (o município reiterando o pedido) é
   silêncio da agência e conta como espera interna. Essa regra nova veio de Unistalda, que reiterou em 2019 o pedido
   de 2018.

Consequência: **o tempo em fila dentro de cada unidade não é observável**, só o intervalo entre peças. Esse é um
limite declarado do diagnóstico.

## 2. Indicadores por processo

Fonte: `saida/processos_indicadores.csv`. du = dias úteis. Lead = da primeira à última peça datada. Horas são
**hipótese** (modelo por conteúdo, a calibrar com os servidores).

| Processo SEI | Município | Instrumento | Situação final | Início | Fim | Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 13.3900.00759-4 | Alecrim | convênio | assinado, sem publicação nos autos | 2013-11-05 | 2014-01-28 | 56 | 24 | 8 | 7 | 2 | 3,1–5,1 |
| 000067-39.00/16-9 | Campinas das Missões | convênio | assinado, sem publicação nos autos | 2016-01-07 | 2016-05-30 | 97 | 97 | 9 | 6 | 1 | 4,7–7,2 |
| 000771-39.00/18-8 | Panambi | convênio | assinado, sem publicação nos autos | 2018-07-09 | 2018-08-08 | 22 | 2 | 13 | 9 | 1 | 3,4–6,2 |
| 001086-39.00/18-3 | Salvador do Sul | convênio | assinado e publicado | 2018-09-04 | 2018-12-21 | 72 | 45 | 13 | 8 | 2 | 4,8–9,7 |
| 001283-39.00/18-1 | Unistalda | convênio | aguardando AGERGS | 2018-10-22 | 2019-08-09 | 199 | — | 12 | 6 | 3 | 4,9–7,6 |
| 000212-39.00/19-7 | Mampituba | convênio | aguardando município | 2019-02-18 | 2020-08-19 | 376 | — | 38 | 15 | 6 | 11,3–21,5 |
| 000734-39.00/19-7 | Mata | convênio | assinado e publicado | 2019-06-10 | 2019-11-06 | 105 | — | 21 | 10 | 2 | 6,1–11,4 |
| 000765-39.00/19-5 | Liberato Salzano | convênio | assinado e publicado | 2019-06-19 | 2019-09-25 | 68 | 68 | 12 | 7 | 1 | 4,8–8,6 |
| 000972-39.00/19-5 | Jaguari | convênio | assinado e publicado | 2019-08-01 | 2019-11-20 | 77 | — | 13 | 6 | 2 | 5,5–8,7 |
| 001132-39.00/19-0 | Vila Nova do Sul | convênio | assinado e publicado | 2019-09-17 | 2020-01-16 | 82 | 29 | 17 | 8 | 3 | 6,1–12,0 |
| 001470-39.00/19-6 | Arambaré | convênio | assinado, sem publicação nos autos | 2019-11-28 | 2020-11-10 | 237 | 200 | 17 | 11 | 3 | 6,6–12,1 |
| 000802-39.00/21-6 | Chiapetta | aditivo | assinado e publicado | 2021-05-17 | 2021-05-20 | 3 | — | 6 | 3 | 0 | 1,1–2,6 |
| 000495-39.00/25-0 | Passa Sete | contrato | assinado, sem publicação nos autos | 2025-02-20 | 2025-03-14 | 14 | 0 | 5 | 4 | 0 | 1,9–3,0 |
| 000684-39.00/25-2 | Lagoa Bonita do Sul | contrato | assinado e publicado | 2025-02-19 | 2025-03-14 | 15 | 0 | 5 | 4 | 0 | 0,9–2,5 |
| 000681-39.00/25-4 | Nova Bréscia | contrato | assinado e publicado | 2025-02-28 | 2025-03-21 | 13 | 0 | 10 | 6 | 1 | 4,0–6,8 |
| 001165-39.00/25-8 | Passo Fundo | contrato | assinado e publicado | 2025-05-23 | 2026-09-18 | 334 | 299 | 99 | 64 | 33 | 35,8–88,4 |
| 002063-39.00/25-1 | Minas do Leão | contrato | assinado e publicado | 2025-09-28 | 2026-04-30 | 146 | 137 | 43 | 33 | 21 | 16,9–33,1 |
| 002718-39.00/26-1 | Capão Bonito do Sul | convênio | aguardando AGERGS | 2026-09-11 | 2026-10-20 | 26 | — | 17 | 12 | 1 | 4,7–15,7 |

"—" = sem peça de assinatura do instrumento datada nos autos. "Contrato" = contrato de prestação de serviços de
regulação (modelo de 2025 em diante, com inexigibilidade); "convênio" = convênio de delegação; "aditivo" = termo
aditivo a convênio vigente (Chiapetta: inclusão de competência sancionatória, com o convênio original em outro
processo).

**Situação final** (de `dados/narrativas/*.json`; fatos `coorte.situacao.*`): 10 assinados e publicados nos autos,
5 assinados sem publicação nos autos, 1 aguardando o município (Mampituba, parado desde 08/2020) e 2 aguardando a
AGERGS (Unistalda, com pedido reiterado em 2019 sem resposta nos autos, e Capão Bonito do Sul, em triagem documental).

## 3. Primeiros achados

- **O tempo é espera, não trabalho.** Lead time mediano de 74,5 du por caso (q3 135,8; máximo 376), contra mediana de
  0,5 du de execução de atividades e de 4,8–8,6 h de trabalho estimado. A execução cobre 14,3% do lead time somado da
  coorte (fatos `coorte.caso.*` e `coorte.pct_execucao_no_lead` em `saida/bpmn/fatos_CONV.json`).
- **Três regimes.** Os 12 convênios (2013–2020 e 2026) têm lead mediano de 79,5 du. Os 5 contratos de 2025–2026 têm
  15 du, mas isso é efeito de instrução fragmentada: três contratos (Passa Sete, Lagoa Bonita do Sul, Nova Bréscia)
  chegam ao processo já assinados pelo prefeito, com inexigibilidade e TAAC em outro processo; os dois instruídos no
  próprio processo (Passo Fundo e Minas do Leão) levam 334 e 146 du. O aditivo de Chiapetta (3 du) só registra súmula,
  publicação e comunicação.
- **Passagens e retornos.** Mediana de 7,5 passagens entre unidades e de 3 encaminhamentos sem conteúdo próprio por
  caso. Passo Fundo chega a 64 passagens e 33 retornos a atividades já feitas.
- **Tempo de terceiros.** A espera antes de respostas do município ou do prestador responde por 14,6% da espera total
  (`coorte.pct_espera_terceiros`). O resto é espera interna da AGERGS, inclusive o silêncio diante de pedidos
  reiterados.
- **Etapas formais raras nos convênios antigos.** Em Alecrim, Campinas das Missões, Salvador do Sul, Liberato Salzano e
  Unistalda não há manifestação da PGE nem deliberação do Conselho Superior nos autos; a minuta-padrão aprovada pelo
  Conselho é citada como já existente. Em Alecrim a assinatura se deu em sessão do Conselho.

## 4. Limitações da base

| Limitação | Efeito | Tratamento |
|---|---|---|
| Sem andamentos do SEI | Não se sabe quando cada unidade recebeu o processo nem o tempo em fila dentro dela | Espera inferida pelo intervalo entre peças; limite declarado |
| 33 peças com pouco texto (contratos de programa, ARs, publicações e ofícios digitalizados; contrato de Passa Sete com codificação corrompida) | Conteúdo não verificado; ficha só com título e cabeçalho | Marcado na ficha (`baixo_texto`); pedir nova cópia ou OCR |
| Rodapés sem parênteses ("Comunicado DG 0483362 SEI …") | Comunicados curtos (DTI, DAU, GP, DG) ficaram agrupados na peça anterior (Passa Sete, Lagoa Bonita do Sul, Nova Bréscia, Arambaré, Mata, Capão Bonito do Sul); em Chiapetta a peça 1 ficou sem id | Numeração mantida para não quebrar as fichas; assinaturas desses comunicados contam na peça que os contém. Corrigir a regex numa próxima rodada |
| Instrução em processo apartado (inexigibilidade, TAAC, processo-mãe; convênio original do aditivo de Chiapetta) | Contratos de 2025 e o aditivo parecem rápidos e sem análise jurídica | Explicitado na avaliação e no requisito R-CONV-08 |
| Datas inconsistentes nas peças (minuta de Campinas das Missões com data de 2015; cabeçalho de 2025 com assinatura de 2026; voto com cabeçalho de fevereiro e assinatura de maio) | Datas de texto podem deslocar ocorrências | A data de assinatura tem precedência; data só do texto anterior ao início do processo é ignorada |
| Assinaturas fora do SEI (convênios em papel; Alecrim assinado em sessão do Conselho em 2013, sem assinatura eletrônica lida) | Datas de assinatura e de publicação faltam ou vêm só do texto | A espera antes da publicação inclui a coleta de assinatura fora do SEI; pergunta de validação |
| Rótulos dos arquivos ("Mapituba", "Campinas das Missões") | Os municípios são Mampituba/RS e Campina das Missões/RS | Mantido o código do arquivo; nome correto nos relatórios quando citado em texto |
