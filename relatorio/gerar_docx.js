// Relatório final (Word) — celebração de convênios e contratos de delegação da regulação (AGERGS).
// Números lidos de dados_relatorio.json (scripts/relatorio_figuras.py); nenhum número de resultado é digitado aqui.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, AlignmentType, HeadingLevel,
  WidthType, ShadingType, BorderStyle, LevelFormat, PageBreak, Footer, Header, PageNumber, TableOfContents,
  VerticalAlign,
} = require("docx");

const D = JSON.parse(fs.readFileSync(path.join(__dirname, "dados_relatorio.json"), "utf8"));
const d = (k) => { if (!(k in D)) throw new Error("dado ausente: " + k); return D[k]; };
const FIG = (f) => fs.readFileSync(path.join(__dirname, "fig", f));

const AZUL = "1F4E79", AZUL_CLARO = "DCE6F0", VERDE = "2E7D6B", AMBAR = "C98A1B", CINZA = "5B6670", FUNDO = "F3F6F9";
const W = 9638; // largura útil A4 com margens de 2 cm

// ------------------------------------------------------------------ helpers
// texto com **negrito**
function runs(txt, extra = {}) {
  return txt.split(/(\*\*[^*]+\*\*)/).filter(Boolean).map((p) =>
    p.startsWith("**") ? new TextRun({ text: p.slice(2, -2), bold: true, ...extra }) : new TextRun({ text: p, ...extra }));
}
const P = (txt, o = {}) => new Paragraph({ children: runs(txt, o.run || {}), spacing: { after: 120, line: 288 }, ...o.par });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const B = (txt, nivel = 0) => new Paragraph({ numbering: { reference: "bul", level: nivel }, children: runs(txt), spacing: { after: 60, line: 276 } });
const N = (txt) => new Paragraph({ numbering: { reference: "num", level: 0 }, children: runs(txt), spacing: { after: 60, line: 276 } });
const QUEBRA = () => new Paragraph({ children: [new PageBreak()] });

function figura(arq, largura, altura, legenda) {
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60, after: 40 },
      children: [new ImageRun({ type: "png", data: FIG(arq), transformation: { width: largura, height: altura },
        altText: { title: legenda, description: legenda, name: arq } })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 },
      children: [new TextRun({ text: legenda, italics: true, size: 18, color: CINZA })] }),
  ];
}

const borda = { style: BorderStyle.SINGLE, size: 4, color: "C9D3DC" };
const bordas = { top: borda, bottom: borda, left: borda, right: borda };
function tabela(cab, linhas, larg, opt = {}) {
  const tot = larg.reduce((a, b) => a + b, 0);
  const cel = (t, i, head, zebra) => new TableCell({
    borders: bordas, width: { size: larg[i], type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
    shading: { fill: head ? AZUL : (zebra ? FUNDO : "FFFFFF"), type: ShadingType.CLEAR, color: "auto" },
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: [new Paragraph({ alignment: (opt.alinhar && opt.alinhar[i]) || AlignmentType.LEFT,
      children: runs(String(t), { size: opt.tam || 18, color: head ? "FFFFFF" : "222222", bold: head || undefined }) })],
  });
  return new Table({
    width: { size: tot, type: WidthType.DXA }, columnWidths: larg,
    rows: [new TableRow({ tableHeader: true, children: cab.map((c, i) => cel(c, i, true)) }),
      ...linhas.map((l, r) => new TableRow({ cantSplit: true, children: l.map((c, i) => cel(c, i, false, r % 2 === 1)) }))],
  });
}
// caixa de destaque (célula única sombreada)
function caixa(titulo, itens, cor = AZUL_CLARO) {
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [W],
    rows: [new TableRow({ children: [new TableCell({
      borders: { top: { style: BorderStyle.SINGLE, size: 12, color: AZUL }, bottom: borda, left: borda, right: borda },
      width: { size: W, type: WidthType.DXA }, shading: { fill: cor, type: ShadingType.CLEAR, color: "auto" },
      margins: { top: 120, bottom: 120, left: 200, right: 200 },
      children: [new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: titulo, bold: true, color: AZUL, size: 22 })] }),
        ...itens.map((t) => new Paragraph({ numbering: { reference: "bul", level: 0 }, spacing: { after: 50, line: 276 }, children: runs(t, { size: 20 }) }))],
    })] })],
  });
}
const esp = (n = 120) => new Paragraph({ spacing: { after: n }, children: [] });

// números-chave (cartões)
function cartoes(itens) {
  const w = Math.floor(W / itens.length);
  const larg = itens.map(() => w);
  return new Table({
    width: { size: w * itens.length, type: WidthType.DXA }, columnWidths: larg,
    rows: [new TableRow({ children: itens.map(([v, r]) => new TableCell({
      width: { size: w, type: WidthType.DXA }, borders: { top: { style: BorderStyle.SINGLE, size: 18, color: AZUL }, bottom: borda, left: { style: BorderStyle.SINGLE, size: 4, color: "FFFFFF" }, right: { style: BorderStyle.SINGLE, size: 4, color: "FFFFFF" } },
      shading: { fill: FUNDO, type: ShadingType.CLEAR, color: "auto" }, margins: { top: 100, bottom: 100, left: 100, right: 100 },
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: v, bold: true, size: 34, color: AZUL })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: r, size: 17, color: CINZA })] })],
    })) })],
  });
}

// ------------------------------------------------------------------ conteúdo
const c = [];
// ---------- capa
c.push(new Paragraph({ spacing: { before: 2600 }, children: [new TextRun({ text: "AGERGS", bold: true, size: 28, color: AZUL })] }));
c.push(new Paragraph({ spacing: { after: 200 }, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: AZUL, space: 4 } },
  children: [new TextRun({ text: "Diagnóstico e Melhoria de Processos", size: 24, color: CINZA })] }));
c.push(new Paragraph({ spacing: { before: 400, after: 200 }, children: [new TextRun({ text: "Celebração de convênios e contratos de delegação da regulação", bold: true, size: 52, color: "1A1A1A" })] }));
c.push(new Paragraph({ spacing: { after: 600 }, children: [new TextRun({ text: "Diagnóstico do processo atual, boas práticas de outras agências e proposta de novo fluxo para a AGERGS", size: 28, color: CINZA })] }));
c.push(cartoes([[d("base.pdfs"), "processos SEI analisados"], [d("base.documentos"), "documentos lidos"], [d("coorte.caso.lead.mediana") + " du", "duração mediana hoje"], [d("tobe.1.esperado.lead") + " du", "meta com a fase 1"]]));
c.push(new Paragraph({ spacing: { before: 1800 }, children: [new TextRun({ text: "Porto Alegre, novembro de 2026", size: 22, color: CINZA })] }));
c.push(new Paragraph({ children: [new TextRun({ text: "Documento de trabalho para validação com as unidades. Horas e custos são estimativas a calibrar.", size: 18, italics: true, color: CINZA })] }));
c.push(QUEBRA());

// ---------- sumário
c.push(new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: "Sumário", bold: true, size: 32, color: AZUL })] }));
c.push(new TableOfContents("Sumário", { hyperlink: true, headingStyleRange: "1-2" }));
c.push(QUEBRA());

// ---------- 1. resumo executivo
c.push(H1("1. Resumo executivo"));
c.push(P(`Quando um município decide entregar à AGERGS a regulação do seu saneamento, começa um processo que deveria ser simples: reunir documentos, conferir a legalidade, assinar um instrumento e publicá-lo. Na prática, ele leva em mediana **${d("coorte.caso.lead.mediana")} dias úteis**, quase quatro meses, e alguns casos passam de um ano. Este relatório analisou ${d("coorte.casos")} celebrações registradas no SEI entre 2013 e 2026 para entender por quê e propor um caminho melhor.`));
c.push(caixa("O que encontramos, em cinco frases", [
  `**O tempo é espera, não trabalho.** Só ${d("coorte.pct_execucao_no_lead")}% da duração tem algum documento sendo produzido; o trabalho estimado é de cerca de ${d("coorte.caso.horas_teto.mediana")} horas por caso.`,
  `**Não existe um processo, existem ${d("coorte.n_caminhos")}.** Cada um dos ${d("coorte.casos")} casos seguiu um caminho diferente, com mediana de ${d("coorte.caso.passagens.mediana")} passagens entre unidades e ${d("coorte.caso.retornos.mediana")} retornos a etapas já feitas.`,
  `**A espera é quase toda interna.** Só ${d("coorte.pct_espera_terceiros")}% do tempo parado é resposta do município ou do prestador. O resto se acumula depois da assinatura, na minuta, na publicação e em pedidos do município que esperam resposta.`,
  `**A formalização tem lacunas.** A autorização formal antes da assinatura aparece em ${d("conf.R-CONV-04")}% dos casos, o parecer jurídico em ${d("conf.R-CONV-03")}% e a justificativa de inexigibilidade em ${d("conf.R-CONV-08")}% dos contratos.`,
  `**Dá para reduzir o prazo à metade sem tecnologia nova.** Com o fluxo proposto, a duração mediana simulada cai para ${d("tobe.1.esperado.lead")} dias úteis (−${d("tobe.1.esperado.ganho")}%) só com organização, e para ${d("tobe.3.esperado.lead")} (−${d("tobe.3.esperado.ganho")}%) com automação.`,
]));
c.push(esp());
c.push(P("**O que propomos.** Um fluxo único, com um dono (a DAI, como já indica a proposta do processo SEI 002594-39.00/26-9), um kit de adesão com documentação mínima, uma minuta padrão aprovada uma única vez com parecer jurídico referencial, prazos por etapa e publicação e comunicação em prazo fixo contado da assinatura. As medidas estão organizadas em três fases e acompanhadas de oito indicadores com metas."));

// ---------- 2. contexto e base
c.push(H1("2. O processo e como ele foi analisado"));
c.push(P("A Lei Federal 11.445/2007 permite que o município, titular do serviço de saneamento, delegue a regulação a uma agência. A Lei Estadual 16.266/2024 diz que a AGERGS regula serviços municipais delegados por **instrumento convenial ou contratual**. Esse instrumento é o produto do processo analisado aqui. Ao longo do tempo ele mudou de forma:"));
c.push(tabela(["Forma", "Período", "Casos", "Duração mediana", "Característica"], [
  ["Convênio de delegação", "2013–2020 e 2026", d("coorte.instrumento.convenio_delegacao.casos"), d("coorte.instrumento.convenio_delegacao.lead.mediana") + " du", "Pedido do prefeito, análise jurídica interna, minuta caso a caso"],
  ["Contrato de prestação de serviços de regulação", "2025–2026", d("coorte.instrumento.contrato_prestacao_servicos_regulacao.casos"), d("coorte.instrumento.contrato_prestacao_servicos_regulacao.lead.mediana") + " du", "Inexigibilidade (Lei 14.133, art. 74); parte da instrução fica em outro processo"],
  ["Termo aditivo", "2021", d("coorte.instrumento.aditivo.casos"), d("coorte.instrumento.aditivo.lead.mediana") + " du", "Inclusão de competência sancionatória"],
], [2700, 1500, 800, 1500, 3138], { alinhar: [null, null, AlignmentType.CENTER, AlignmentType.CENTER] }));
c.push(esp());
c.push(P(`**Como fizemos.** Em vez de partir de entrevistas, reconstruímos o processo real a partir do que ficou registrado no SEI: os ${d("base.documentos")} documentos de ${d("base.pdfs")} processos (as ${d("coorte.casos")} celebrações e dois processos de gestão: o orientativo e o da minuta padrão). Cada documento recebeu uma ficha (quem fez, o quê, quando, com que esforço e com que problemas), e cada etapa foi medida em dias úteis a partir das datas de assinatura. Exigências legais foram conferidas contra o texto integral das normas. Todos os números saem de cálculo reprodutível; horas de trabalho e custos são estimativas a calibrar com os servidores.`));
c.push(P("**Limites.** Os PDFs exportados do SEI não trazem o histórico de tramitação, só os documentos. Por isso, a espera é medida entre documentos, e o que ocorreu fora do SEI (telefonemas, assinaturas em papel) não aparece. Com 18 casos, os números indicam ordem de grandeza e tendência, não estatística fina."));

// ---------- 3. como funciona hoje
c.push(H1("3. Como o processo funciona hoje"));
c.push(P("O desenho abaixo é o caminho mais comum, montado a partir dos 18 casos. A porcentagem em cada etapa mostra em quantos casos ela de fato aparece nos autos. As setas tracejadas mostram os retornos mais frequentes."));
c.push(...figura("fluxo_asis.png", 620, 248, "Figura 1 — Fluxo atual (AS-IS), com a frequência de cada etapa nos 18 casos"));
c.push(P("Três coisas saltam aos olhos:"));
c.push(B(`**Etapas centrais são opcionais na prática.** A deliberação do Conselho aparece em ${d("coorte.t8.pct_casos")}% dos casos e a autorização formal da Presidência ou da Diretoria-Geral em apenas ${d("coorte.t9.casos")} caso. Três contratos de 2025 chegaram ao processo já assinados.`));
c.push(B(`**A documentação chega em rodadas.** A complementação pelo município aparece em ${d("coorte.t3.casos")} casos, com repetição em ${d("coorte.t3.casos_com_laco")}. Termo de cooperação com o Estado e contrato de programa costumam chegar depois da minuta, às vezes depois da assinatura.`));
c.push(B(`**Análise jurídica e minuta vão e voltam.** A análise jurídica se repete em ${d("coorte.t6.casos_com_laco")} casos e a minuta em ${d("coorte.t5.casos_com_laco")}. A oitiva do prestador aparece em só ${d("coorte.t16.casos")} casos, mas soma ${d("coorte.t16.ocorrencias")} rodadas; Passo Fundo, sozinho, acumulou ${d("coorte.caso.passagens.max")} passagens entre unidades.`));
c.push(...figura("lead_casos.png", 520, 361, "Figura 2 — Duração de cada celebração, em dias úteis"));

// ---------- 4. diagnóstico
c.push(H1("4. Diagnóstico"));
c.push(H2("4.1 Onde o tempo se perde"));
c.push(P(`A mediana esconde uma cauda longa: metade dos casos termina em até ${d("coorte.caso.lead.mediana")} du, mas um quarto passa de ${d("coorte.caso.lead.q3")} du, e o máximo chega a ${d("coorte.caso.lead.max")} du. Quando se soma toda a espera dos 18 casos e se pergunta **antes de qual etapa** o processo ficou parado, a resposta é clara:`));
c.push(...figura("espera.png", 560, 264, "Figura 3 — Em que ponto do fluxo a espera se acumula"));
c.push(P(`A maior fila está **depois da assinatura**: comunicar o prestador e as unidades (${d("coorte.t13.pct_espera_total")}%) e publicar o extrato (${d("coorte.t12.pct_espera_total")}%) somam ${d("espera.pos_assinatura")}% dos dias parados. Logo em seguida vem algo pouco visível: **pedidos do município que esperam resposta até ele reiterar** (${d("coorte.t1.pct_espera_total")}%). Em Unistalda, o pedido de 2018 só foi reiterado em 2019, e o processo ainda aguarda a AGERGS.`));
c.push(H2("4.2 Os desperdícios, em linguagem Lean"));
c.push(tabela(["Desperdício", "Como aparece no processo", "Gravidade"], [
  ["Espera", `Execução cobre ${d("coorte.pct_execucao_no_lead")}% do prazo; eficiência do ciclo de ${d("coorte.pce_teto")}%`, "Alta"],
  ["Transporte", `Mediana de ${d("coorte.caso.passagens.mediana")} passagens e ${d("coorte.caso.n_encaminhamentos.mediana")} encaminhamentos sem conteúdo por caso`, "Alta"],
  ["Retrabalho", `Mediana de ${d("coorte.caso.retornos.mediana")} retornos por caso (máximo de ${d("coorte.caso.retornos.max")}); erros materiais repetidos (ano da Lei 11.445, foro, número da lei municipal, CNPJ); súmula publicada antes da assinatura, com errata`, "Alta"],
  ["Superprocessamento", "Cada minuta é redigida do zero ou copiada do último caso; cláusulas divergem entre contratos (fundamento legal, vigência, rescisão, custeio)", "Média"],
  ["Movimentação", "Documentos pedidos em várias rodadas, sem lista mínima na entrada", "Média"],
  ["Estoque", `${d("coorte.situacao.assinado_sem_publicacao_no_processo")} casos assinados sem publicação nos autos e ${d("coorte.situacao.aguardando_agergs")} aguardando a AGERGS; arquivamento formal raro`, "Média"],
], [1900, 6338, 1400], { alinhar: [null, null, AlignmentType.CENTER] }));
c.push(esp());
c.push(H2("4.3 Conformidade legal"));
c.push(P("Dez requisitos foram tirados do texto literal da Lei 11.445/2007, da Lei 14.133/2021 e das Leis Estaduais 16.266/2024 e 15.612/2021. Oito deles podem ser testados nos autos:"));
c.push(...figura("conformidade.png", 560, 280, "Figura 4 — Quanto da exigência legal está nos autos"));
c.push(P(`O quadro não indica ilegalidade. Indica **instrução incompleta ou dispersa**: atos que provavelmente existiram (autorização, inexigibilidade, publicação), mas em outro processo, em papel ou sem juntada. A publicação em até 10 dias úteis da assinatura, prevista no art. 94 da Lei 14.133, é cumprida em ${d("conf.R-CONV-06")}% dos casos aplicáveis. Em um caso, a súmula saiu antes da assinatura e precisou de errata.`));
c.push(H2("4.4 Qualidade dos instrumentos"));
c.push(P("A comparação entre contratos assinados, feita no processo da minuta padrão (SEI 002840-39.00/26-3), e a leitura dos 18 casos mostram textos que mudam de um município para outro sem motivo registrado: fundamento legal (art. 74 da Lei 14.133 ou art. 8º da Lei 11.445), vigência (60 meses ou atrelada à concessão), hipóteses de rescisão e periodicidade do custeio. Aparecem também erros que se propagam por cópia: \"Lei n. 11.445/2027\", foro de outro município, \"Município de Xxx\", número de lei municipal divergente e CNPJ trocado."));

// ---------- 5. benchmarking
c.push(H1("5. O que outras agências fazem"));
c.push(P("Uma pesquisa rápida em agências reguladoras, na ANA e em órgãos de controle mostrou práticas que respondem diretamente aos problemas encontrados:"));
c.push(tabela(["Quem", "Prática", "Problema que resolve"], [
  ["ANA — NR 4/2024", "Ato de delegação com 4 elementos mínimos: atribuições com poder fiscalizatório, escopo, deveres das partes e origem dos recursos. Comprovação anual da agência à ANA", "Instrumentos diferentes entre si"],
  ["AGEPAR (PR)", "Guia para novos convênios; pedido do prefeito só por protocolo eletrônico; minuta sugestiva anexa a uma resolução", "Documentação em rodadas; minuta caso a caso"],
  ["AGU e PGE-PR", "Minutas-padrão com parecer jurídico referencial e lista de verificação: a análise individual só confere o enquadramento", "Análise jurídica repetida"],
  ["ARES-PCJ (SP)", "Concessionária assina como interveniente e paga a taxa; vigência acompanha a concessão; rescisão só com contraditório", "Negociação longa com o prestador"],
  ["AGIR e ARIS (SC)", "Rito de adesão escrito: pedido formal, aprovação em assembleia, lei de ratificação que já institui a taxa", "Falta de rito e de critério de decisão"],
  ["AGR-GO", "Lei municipal autorizativa como entrada; publicação em até 30 dias e comunicação à Câmara Municipal", "Publicação sem prazo"],
  ["ARSAE-MG", "Lei estadual fixa o conteúdo mínimo do convênio", "Cláusulas divergentes"],
  ["SEI (usuário externo)", "Assinatura eletrônica do prefeito no próprio processo", "Assinatura em papel, fora dos autos"],
], [1900, 4838, 2900]));
c.push(esp());
c.push(P("Nenhuma das fontes publica a redução de prazo obtida com essas práticas. Por isso, os ganhos deste relatório são simulações sobre os casos da AGERGS, não promessas importadas de outro lugar."));

// ---------- 6. proposta orientativa
c.push(H1("6. A proposta do processo SEI 002594-39.00/26-9"));
c.push(P("A própria AGERGS já deu o primeiro passo. O processo orientativo propõe um procedimento institucional único para todos os instrumentos de cooperação, delegação e parceria, em **11 etapas**, com a DAI como coordenadora institucional desde a origem nos casos de delegação da regulação. O diagnóstico confirma o problema que ela aponta: não há fluxo formal, e as competências indefinidas geram retrabalho."));
c.push(tabela(["Etapa proposta", "Responsável", "O diagnóstico recomenda"], [
  ["1. Necessidade, abertura e instrução inicial", "Unidade proponente / DAI", "Formulário de adesão e checklist mínimo na abertura"],
  ["2. Articulação, objeto e coleta documental", "DAI", "Diligência única, com prazo, em vez de rodadas"],
  ["3. Análise técnica e de viabilidade", "Unidade técnica", "Em paralelo à minuta e à oitiva do prestador"],
  ["4. Validação institucional pela DG", "DG", "Pode ser dispensada quando o caso segue a minuta padrão"],
  ["5. Estruturação jurídica (PSE)", "PSE", "Parecer referencial sobre a minuta padrão; análise só dos desvios"],
  ["6. Definição do rito decisório", "GP", "Critério escrito: Presidência sem desvio, Conselho com desvio relevante"],
  ["7. Deliberação", "Presidência ou CS", "Autorização e inexigibilidade sempre nos autos"],
  ["8. Formalização e assinatura", "DAI", "Assinatura eletrônica do prefeito no SEI"],
  ["9. Publicação e comunicação", "DG", "Prazo de 10 du da última assinatura; comunicado único"],
  ["10. Implantação", "DG", "Cadastro do município e envio de informações à ANA"],
  ["11. Monitoramento, alteração e encerramento", "DAI", "Plano de trabalho anual; aditivos pela mesma minuta"],
], [3300, 1900, 4438]));
c.push(esp());
c.push(P("**O que falta na proposta**, segundo o próprio processo e o diagnóstico:"));
c.push(B("**Prazos por etapa.** O único prazo citado é o de 15 dias úteis para as unidades se manifestarem sobre a proposta."));
c.push(B("**Checklist por tipo de instrumento.** A lista de documentos é indicativa (\"poderão ser solicitados\")."));
c.push(B("**Critério objetivo** para levar o caso à Presidência ou ao Conselho Superior."));
c.push(B("**Ajustes de redação:** a DG aparece como executora nas etapas 4, 9 e 10, embora o texto diga que ela não deve executar; o escopo da DSI diverge entre a justificativa e o anexo; o regramento da deliberação cita a etapa 8 quando é a 7."));
c.push(B("**Manifestações pendentes:** a DTM pediu prazo adicional, e as demais unidades ainda não se manifestaram nos autos."));
c.push(P("A proposta é um bom guarda-chuva para todos os instrumentos da agência. Para a delegação da regulação, que é o caso mais frequente e mais padronizável, sugerimos um **rito simplificado dentro dela**, descrito a seguir."));

// ---------- 7. novo processo
c.push(H1("7. O novo processo proposto"));
c.push(P("O novo fluxo segue a lógica \"padrão primeiro, exceção depois\": tudo o que pode ser decidido uma vez (documentos exigidos, texto do instrumento, parecer jurídico) é decidido uma vez, e cada caso só discute o que foge do padrão."));
c.push(...figura("fluxo_tobe.png", 630, 286, "Figura 5 — Fluxo proposto (TO-BE)"));
c.push(H2("7.1 Gatilhos, entradas, análises e saídas"));
c.push(tabela(["Elemento", "Como fica"], [
  ["Gatilhos de início", "Pedido formal do prefeito pelo formulário de adesão; lei autorizativa já aprovada; nova concessão ou novo contrato de programa; necessidade de ajustar competências (aditivo)"],
  ["Entradas (kit mínimo)", "Manifestação do titular com serviços e prestador; lei autorizativa; contrato de concessão ou de programa; PMSB, se houver; regulação anterior por outra entidade; parecer do conselho municipal de saneamento, se existir; cadastro do prefeito como usuário externo do SEI"],
  ["Análises", "Admissibilidade (checklist, pela DAI); técnica (escopo e prestador, em paralelo); jurídica (enquadramento no parecer referencial e desvios); econômico-financeira (taxa de regulação e quem paga); oitiva do prestador, uma vez e com prazo; aderência aos 4 elementos da NR 4 da ANA"],
  ["Decisão", "Presidência quando o caso segue a minuta padrão; Conselho Superior quando há desvio relevante; autorização e justificativa da inexigibilidade sempre nos autos"],
  ["Saídas", "Instrumento assinado eletronicamente; extrato publicado em até 10 du da última assinatura; comunicado único ao prestador, à Câmara Municipal e às unidades; cadastro do município regulado; plano de trabalho anual de fiscalização"],
], [2000, 7638]));
c.push(esp());
c.push(H2("7.2 Prazos internos sugeridos"));
c.push(P("Os prazos seguem a Lei Estadual 15.612/2021, que fixa 5 dias para atos sem prazo próprio (prorrogáveis ao dobro) e 30 dias para decidir após concluída a instrução:"));
c.push(tabela(["Etapa", "Prazo sugerido", "Contagem"], [
  ["Conferência do checklist e diligência única", "5 du", "Do recebimento do formulário"],
  ["Resposta do município à diligência", "Prazo fixado no ofício (tempo do município)", "Protegido: não é cortado"],
  ["Análise técnica, minuta e oitiva do prestador (em paralelo)", "10 du", "Do checklist completo"],
  ["Conferência jurídica do enquadramento", "5 du (10 du se houver desvio)", "Da minuta preenchida"],
  ["Decisão (Presidência ou Conselho)", "Até 30 dias", "Da instrução concluída"],
  ["Publicação do extrato", "10 du", "Da última assinatura"],
  ["Comunicado único e encerramento", "5 du", "Da publicação"],
], [4300, 2900, 2438]));

// ---------- 8. melhorias e ganhos
c.push(H1("8. Melhorias e ganhos esperados"));
c.push(P("As 12 melhorias estão em três fases cumulativas. A fase 1 muda só a organização; a fase 2 automatiza regras e documentos; a fase 3 usa inteligência artificial para conferir e redigir, sempre com revisão de um servidor."));
const fases = { 1: "Fase 1 — fluxo", 2: "Fase 2 — regras e dados", 3: "Fase 3 — IA assistida" };
c.push(tabela(["Fase", "Melhoria", "O que muda"], D.melhorias.map((m) => [fases[m.fase].split(" — ")[0], m.titulo, m.descricao.split(";")[0].split(". ")[0].replace(/\.$/, "") + "."]), [1000, 3300, 5338], { tam: 17 }));
c.push(esp());
c.push(P("Para estimar o ganho, cada melhoria foi aplicada aos 18 casos reais em três cenários (conservador, esperado e otimista), sem cortar o tempo de resposta do município e do prestador:"));
c.push(...figura("tobe.png", 560, 257, "Figura 6 — Duração mediana simulada por fase e cenário (dias úteis)"));
c.push(tabela(["", "Hoje", "Fase 1", "Fase 2", "Fase 3"], [
  ["Duração mediana (du), cenário esperado", d("base.lead"), d("tobe.1.esperado.lead"), d("tobe.2.esperado.lead"), d("tobe.3.esperado.lead")],
  ["Redução da duração", "—", "−" + d("tobe.1.esperado.ganho") + "%", "−" + d("tobe.2.esperado.ganho") + "%", "−" + d("tobe.3.esperado.ganho") + "%"],
  ["Faixa de redução (conservador a otimista)", "—", `−${d("tobe.1.conservador.ganho")}% a −${d("tobe.1.otimista.ganho")}%`, `−${d("tobe.2.conservador.ganho")}% a −${d("tobe.2.otimista.ganho")}%`, `−${d("tobe.3.conservador.ganho")}% a −${d("tobe.3.otimista.ganho")}%`],
  ["Horas de trabalho por caso (mediana, estimativa)", d("base.horas"), d("tobe.1.esperado.horas"), d("tobe.2.esperado.horas"), d("tobe.3.esperado.horas")],
], [3638, 1500, 1500, 1500, 1500], { alinhar: [null, AlignmentType.CENTER, AlignmentType.CENTER, AlignmentType.CENTER, AlignmentType.CENTER] }));
c.push(esp());
c.push(P(`A maior parte do ganho vem da **fase 1**. Entre as medidas, as que mais pesam são o comunicado único pós-assinatura, a publicação em prazo fixo, o kit de adesão e os prazos internos por etapa. A IA reduz sobretudo horas de trabalho, que já são poucas, e quase não mexe no prazo.`));

// ---------- 9. indicadores
c.push(H1("9. Como acompanhar: indicadores e metas"));
c.push(P("Cada meta vem da simulação (fases 1 a 3) ou da própria lei (100%). Os indicadores podem ser apurados a partir do SEI, de preferência num painel mensal."));
c.push(tabela(["Indicador", "Hoje", "Meta fase 1", "Meta fase 3", "Responsável"],
  D.indicadores.map((i) => [i.nome, i.base + (i.unidade === "%" ? "%" : " " + i.unidade), i.metas["1"] ? i.metas["1"] + (i.unidade === "%" ? "%" : " " + i.unidade) : "acompanhar",
    i.metas["3"] ? i.metas["3"] + (i.unidade === "%" ? "%" : " " + i.unidade) : (i.metas["1"] ? i.metas["1"] + (i.unidade === "%" ? "%" : "") : "acompanhar"), i.resp]),
  [3838, 1300, 1450, 1450, 1600], { alinhar: [null, AlignmentType.CENTER, AlignmentType.CENTER, AlignmentType.CENTER, AlignmentType.CENTER] }));
c.push(esp());
c.push(P(`A publicação em até 10 du não chega a 100% na simulação porque parte da espera é a assinatura do município. Chegar lá depende da assinatura eletrônica no SEI e de prazo para o município assinar. O indicador de retornos por caso serve de contrapeso: prazo menor não pode virar mais retrabalho.`));

// ---------- 10. automação
c.push(H1("10. Vale automatizar o processo inteiro?"));
c.push(P(`Ainda não. Pelos critérios de priorização da metodologia (volume, peso das análises, dados, regras claras, padronização e completude), o processo obtém nota **${d("prio.nota")} de 100**. O processo indicado como piloto no caso de referência obteve 80. Três condições para um piloto de automação completa não são atendidas: volume anual baixo, fluxo ainda não padronizado e nenhum caminho que se repita. Na estimativa (hipótese), um sistema dedicado custaria cerca de R$ ${d("prio.construcao")} para devolver R$ ${d("prio.retorno")} por ano em horas.`));
c.push(P("A recomendação é **padronizar primeiro (fases 1 e 2)** e usar IA em tarefas pontuais e reaproveitáveis em outros processos da agência: conferência de documentos contra checklist, minuta a partir do padrão com checagem de erros materiais e pré-análise jurídica, sempre com revisão humana."));

// ---------- 11. implementação
c.push(H1("11. Plano de implementação"));
c.push(tabela(["Quando", "O que fazer", "Quem"], [
  ["0 a 3 meses", "Concluir o processo orientativo com o rito simplificado da delegação; aprovar a minuta padrão e o parecer referencial; publicar o formulário e o checklist; definir a DAI como dona do processo; criar tipo de processo SEI próprio", "GP, DAI, PSE, Conselho Superior"],
  ["3 a 6 meses", "Prazos internos em vigor; modelos SEI de ofício, extrato, comunicado e termo de encerramento; assinatura eletrônica do prefeito como usuário externo; primeiro painel de indicadores", "DAI, DG, DTI"],
  ["6 a 12 meses", "Painel com alertas de prazo e de pedido sem resposta; integração com a comprovação anual à ANA; piloto de conferência de documentos e de minuta assistidas, com controle de qualidade", "DAI, DTI, DAJ"],
  ["Contínuo", "Revisão trimestral dos indicadores; calibração das horas com as unidades; atualização da minuta padrão quando a ANA ou a lei mudarem", "DAI e unidades"],
], [1500, 6038, 2100]));
c.push(esp());
c.push(caixa("Decisões que dependem da gestão", [
  "Confirmar a DAI como dona do processo de delegação e alinhar as atribuições com DSI e DTM.",
  "Definir o instrumento-padrão (convênio de cooperação ou contrato com inexigibilidade), com manifestação da PSE.",
  "Aprovar a minuta padrão e o critério de quando o caso vai ao Conselho Superior.",
  "Decidir se a AGERGS publicará um guia de adesão para os municípios, como fazem outras agências.",
]));
c.push(esp());
c.push(H2("Próximos passos de validação"));
c.push(B(`Validar com as unidades os rótulos das etapas: a conferência independente concordou em ${d("aud.subst")}% das ${d("aud.pecas")} peças auditadas, abaixo da meta de 85%.`));
c.push(B("Conferir no DOE-RS os textos das Leis Estaduais 16.266/2024 e 15.612/2021 usados nos requisitos."));
c.push(B("Informar o número real de celebrações por ano e o custo-hora, hoje estimados."));
c.push(B("Localizar os processos de inexigibilidade e os TAAC dos contratos de 2025, que estão fora dos autos analisados."));

// ---------- anexo
c.push(H1("Anexo — Processos analisados"));
c.push(tabela(["Município", "Processo SEI", "Instrumento", "Início", "Duração (du)", "Docs.", "Situação nos autos"],
  D.casos.map((x) => [x.municipio, x.sei, x.instrumento, x.ano, x.lead, x.docs, x.situacao]),
  [1750, 1750, 1100, 750, 1050, 700, 2538], { tam: 16, alinhar: [null, null, null, AlignmentType.CENTER, AlignmentType.CENTER, AlignmentType.CENTER] }));
c.push(esp(80));
c.push(P("Duração: dias úteis da primeira à última peça datada do processo. Também foram analisados os processos SEI 002594-39.00/26-9 (processo orientativo) e 002840-39.00/26-3 (minuta padrão).", { run: { size: 18, color: CINZA } }));

// ------------------------------------------------------------------ documento
const doc = new Document({
  creator: "AGERGS", title: "Celebração de convênios e contratos de delegação da regulação — diagnóstico e proposta",
  styles: {
    default: { document: { run: { font: "Calibri", size: 21 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: "Calibri", size: 32, bold: true, color: AZUL },
        paragraph: { spacing: { before: 360, after: 140 }, keepNext: true, outlineLevel: 0,
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: AZUL_CLARO, space: 4 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: "Calibri", size: 25, bold: true, color: "2B5D8A" },
        paragraph: { spacing: { before: 220, after: 100 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [
    { reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 400, hanging: 260 } } } }] },
    { reference: "num", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 400, hanging: 300 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } },
      titlePage: true },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
      children: [new TextRun({ text: "AGERGS · Celebração de instrumentos de delegação da regulação", size: 16, color: CINZA })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: CINZA })] })] }) },
    children: c,
  }],
});
Packer.toBuffer(doc).then((buf) => {
  const out = path.join(__dirname, "Relatorio_Celebracao_Convenios_AGERGS.docx");
  fs.writeFileSync(out, buf);
  console.log("gravado:", out);
});
