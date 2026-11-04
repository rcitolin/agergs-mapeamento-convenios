# Avaliação AS-IS — melhoria e automação com IA

Gerado a partir de `saida/bpmn/avaliacao_CONV.json`, validado por `scripts/fase3_agergs.py avaliacao` (0 número sem lastro; cada número cita um fato de `saida/bpmn/fatos_CONV.json`). Carimbo: fatos 896ab852fe9ab967, em 2026-11-04 16:23.

## Síntese

A celebração de instrumento de delegação da regulação é indicativa, não procedimento: são 18 casos, cada um com caminho próprio (18 caminhos), e a auditoria às cegas dos rótulos é a medida que decide se o tipo vira procedimento. O processo não tem dono nem rito fixo. Pedido, análise jurídica, minuta, autorização, assinatura e publicação aparecem em ordens diferentes, e parte da instrução dos contratos de 2025 fica em outro processo (inexigibilidade e TAAC). O tempo é espera, não trabalho: a execução cobre 14,3% do lead time somado da coorte, e a eficiência do ciclo, mesmo com as horas no teto, é de 1,7%. Só 10 casos terminam assinados e publicados nos autos.

## Leitura das métricas (VSM)

Por caso, o lead time tem mediana de 74,5 du (q3 de 135,8 du; máximo de 376 du), e o trabalho estimado tem mediana de 4,8 h no piso e 8,6 h no teto: horas, não semanas. A mediana por caso é de 7,5 passagens entre unidades, 3 encaminhamentos sem conteúdo próprio e 2 retornos a uma atividade já feita, com máximo de 64 passagens e 33 retornos (Passo Fundo). O tempo de resposta do município e do prestador responde por 14,6% da espera total: o resto é espera interna, inclusive o silêncio da agência diante de pedidos reiterados. Os convênios têm lead mediano de 79,5 du; os contratos de 2025–2026, de 15 du, porque três deles já chegam assinados e a instrução está em outro processo.

## Gargalo (Teoria das Restrições)

**Onde:** Fila sem dono antes e depois das decisões: o pedido do município que espera resposta, a minuta que espera nova versão, e a assinatura que espera publicação e comunicação. A análise jurídica é o maior ponto de espera antes do mérito.

**Evidência:** A espera antes da comunicação ao prestador e às unidades responde por 21,3% da espera total da coorte, a espera antes de um novo pedido do município (reiteração sem resposta) por 16,3%, a da publicação por 16,1%, a da minuta por 13,8% e a da análise jurídica por 10,5%. Na mediana as esperas por ocorrência são curtas (2 du antes da publicação, 3,5 du antes da análise jurídica). O peso vem das caudas: q3 de 34,5 du antes da publicação e máximo de 153 du antes da minuta.

Atividades: t13 (Comunicar prestador e unidades internas), t1 (Solicitar delegação da regulação), t12 (Publicar extrato no Diário Oficial), t5 (Elaborar ou ajustar minuta do instrumento), t6 (Analisar juridicamente o pedido).

## Variabilidade

A dispersão é a regra: 18 caminhos distintos em 18 casos; o lead vai de 3 du (aditivo de Chiapetta) e 13 du (Nova Bréscia) a 376 du (Mampituba), e o q3 é de 135,8 du. A variação tem quatro causas observadas: a forma do instrumento (convênio de 2013 a 2020; contrato com inexigibilidade a partir de 2025; aditivo), quem conduz (GP, DG, DAJ, DAI ou DQS conforme o caso), a resposta ao pedido do município (Unistalda reiterou o pedido sem resposta) e a negociação com a CORSAN, concentrada nos dois maiores casos de 2025–2026 (17 ocorrências de oitiva do prestador em 3 casos).

## Desperdícios (Lean)

| Tipo | Severidade | Atividades | Evidência |
|---|---|---|---|
| Espera | alta | t1, t5, t12, t13 | A execução cobre 14,3% do lead time somado; o resto é processo parado entre peças. A maior espera isolada antes da minuta é de 153 du (Mampituba), e antes de um novo pedido do município, de 181 du. |
| Transporte | alta | t2, t6, t13 | Mediana de 7,5 passagens e de 3 encaminhamentos sem conteúdo próprio por caso; no máximo, 64 passagens. Os encaminhamentos não viram tarefa no modelo, mas são fila. |
| Defeitos/retrabalho | alta | t5, t6, t10 | Mediana de 2 retornos por caso (máximo de 33). A análise jurídica se repete em 8 casos, a minuta em 5 e o envio ao município em 4; nas fichas há erros materiais repetidos (ano da Lei 11.445, foro trocado ou de outro município, número de lei municipal divergente, CNPJ) e súmula publicada antes da assinatura, com errata. |
| Superprocessamento | média | t5 | Cada caso redige a minuta do zero ou a partir do último instrumento. A minuta tem mediana de 1,9 h no teto por ocorrência e passa por 12 casos; o processo da minuta padrão comparou contratos assinados e achou cláusulas divergentes (fundamento legal, vigência, rescisão, custeio). |
| Movimentação | média | t3, t10 | Documentação do município pedida em rodadas: a complementação aparece em 15 casos, com laço em 7. Não há lista mínima de documentos na entrada; termo de cooperação com o Estado e contrato de programa costumam chegar depois da minuta ou da assinatura. |
| Estoque | média | t12, t15 | Situação final: 1 caso aguardando o município, 2 aguardando a AGERGS e 5 assinados sem publicação nos autos, sem marco de encerramento. O arquivamento formal só aparece em 2 casos. |

## Análise de valor e potencial de IA por atividade

| Atividade | Valor | Potencial de IA | Tipos de IA | Aplicação da IA | Ganho esperado | Controle humano | Melhoria Lean |
|---|---|---|---|---|---|---|---|
| t1 · Solicitar delegação da regulação | necessária sem valor | baixo | classificação e triagem; monitoramento de prazos e alertas | Ler o ofício na chegada, identificar serviço, prestador e município e alertar pedido sem resposta. | Evita reiteração: espera antes de novo pedido com máximo de 181 du. | Gabinete confere o pedido. | Formulário de adesão padronizado, já com a lista de documentos mínimos, e resposta com prazo. |
| t2 · Autuar pedido e distribuir às unidades | necessária sem valor | médio | automação de tramitação (RPA no SEI); classificação e triagem | Abrir o processo com tipo SEI próprio e distribuir pelas regras do fluxo. | Pequeno: mediana de 1 du de espera antes e 0,1 h no piso. | GP confirma a distribuição. | Tipo de processo SEI único e dono do processo definido na abertura. |
| t3 · Complementar documentação e lei autorizativa | necessária sem valor | alto | extração de dados de documentos; verificação de conformidade | Conferir a documentação recebida contra o checklist mínimo e apontar o que falta numa única diligência. | Reduz rodadas: complementação em 15 casos, com laço em 7. | Servidor confirma a lista de pendências antes do envio. | Checklist único na entrada; uma só diligência consolidada. |
| t4 · Analisar aspectos técnicos da delegação | agrega valor | médio | sumarização e linha do tempo; extração de dados de documentos | Resumir o contrato de programa ou de concessão e o PMSB para a diretoria técnica. | Mediana de 2,5 h no teto por ocorrência, em 2 casos. | Diretoria técnica conclui sobre a viabilidade. | Fazer em paralelo à análise jurídica, com prazo. |
| t5 · Elaborar ou ajustar minuta do instrumento | agrega valor | alto | redação assistida de minuta; verificação de conformidade | Gerar a minuta a partir da minuta padrão, preenchendo município, serviço, prestador e percentual, e conferir cláusulas obrigatórias e erros materiais. | Mediana de 1,9 h no teto por ocorrência; o ganho maior é eliminar versões: laço em 5 casos. | DAJ revisa e aprova a minuta. | Minuta padrão única aprovada pela PSE e pelo Conselho; desvio só com justificativa. |
| t6 · Analisar juridicamente o pedido | agrega valor | alto | verificação de conformidade; busca de precedentes e normas; redação assistida de minuta | Pré-análise dos requisitos (lei autorizativa, fundamento, escopo, prestador) e minuta da informação jurídica a partir do checklist. | Mediana de 2,3 h no teto por ocorrência; espera antes com mediana de 3,5 du e máximo de 48 du. | Assessor jurídico conclui e assina. | Parecer referencial sobre a minuta padrão: análise individual só nos desvios. |
| t16 · Ouvir o prestador sobre a minuta | necessária sem valor | médio | monitoramento de prazos e alertas; sumarização e linha do tempo | Controlar o prazo dado à CORSAN e resumir as objeções em quadro comparativo. | Ocorre em 3 casos, com 17 ocorrências: o laço é o problema. | Presidência decide sobre as objeções. | Uma oitiva com prazo fixo, sobre a minuta padrão. |
| t7 · Emitir manifestação da Procuradoria Setorial | agrega valor | médio | verificação de conformidade | Destacar para a PSE só as cláusulas que fogem da minuta padrão. | Ocorre em 2 casos; mediana de 1,3 h no teto. | Procurador conclui. | Manifestação referencial da PSE sobre a minuta padrão. |
| t8 · Deliberar sobre a celebração no Conselho | necessária sem valor | baixo | sumarização e linha do tempo; redação assistida de minuta | Montar relatório do caso para o relator a partir dos autos. | Ocorre em 3 casos; mediana de 4,2 h no teto por ocorrência. | Voto e deliberação ficam com o Conselho. | Critério escrito de quando vai ao Conselho; com minuta padrão aprovada, a regra é a Presidência. |
| t9 · Autorizar celebração e inexigibilidade | necessária sem valor | baixo | redação assistida de minuta | Gerar o despacho de autorização e a justificativa de inexigibilidade a partir do processo. | Aparece em 1 caso: a autorização falta nos autos. | Presidência assina. | Autorização formal sempre no processo de celebração, não em processo apartado. |
| t10 · Enviar minuta e tratar com município | necessária sem valor | médio | monitoramento de prazos e alertas; redação assistida de minuta | Ofício por modelo com prazo e alerta de vencimento. | Trabalho pequeno (mediana de 0,6 h no teto); laço em 4 casos. | GP assina. | Envio único da minuta final com prazo e acesso externo no SEI. |
| t11 · Assinar o instrumento pelas partes | agrega valor | médio | automação de tramitação (RPA no SEI) | Liberar assinatura do prefeito como usuário externo do SEI e acompanhar. | Espera antes com q3 de 14 du e máximo de 32 du. | As partes assinam. | Assinatura eletrônica no SEI pelas duas partes, sem via em papel. |
| t12 · Publicar extrato no Diário Oficial | necessária sem valor | alto | automação de tramitação (RPA no SEI); monitoramento de prazos e alertas | Gerar o extrato a partir do instrumento assinado e controlar o prazo de divulgação. | Espera antes com mediana de 2 du e q3 de 34,5 du; 16,1% da espera total. | DG confere o extrato. | Publicar em prazo fixo contado da última assinatura, nunca antes dela. |
| t13 · Comunicar prestador e unidades internas | necessária sem valor | alto | automação de tramitação (RPA no SEI); painel e indicadores | Disparar de uma vez os comunicados e o cadastro do município regulado. | 21,3% da espera total; laço em 4 casos. | DG confere os destinatários. | Comunicado único com lista de distribuição padrão. |
| t14 · Instruir aditivo ao instrumento | necessária sem valor | médio | redação assistida de minuta | Minuta do aditivo a partir do instrumento vigente. | A medir: 2 casos. | DAJ e Presidência. | Cláusulas de competência completas na minuta padrão evitam aditivo. |
| t15 · Arquivar o processo | necessária sem valor | médio | monitoramento de prazos e alertas; automação de tramitação (RPA no SEI) | Gerar o termo quando publicação e comunicados estiverem nos autos. | Ocorre em 2 casos; espera antes com mediana de 21,5 du. | GP assina. | Encerramento em prazo fixo após o último comunicado. |

Contagem: 16 atividades. Por valor: necessária sem valor 11; agrega valor 5. Por potencial de IA: baixo 3; médio 8; alto 5.

## Oportunidades priorizadas

1. **Kit de adesão: formulário, checklist de documentos mínimos e minuta padrão com parecer referencial** (Lean; impacto alto, esforço baixo): Entrada única com a documentação mínima do processo da minuta padrão; minuta padrão aprovada uma vez pela PSE e pelo Conselho; análise jurídica individual só dos desvios.
   - Ganho esperado: Ataca os laços de análise jurídica (8 casos) e de minuta (5 casos) e a espera antes da minuta, 13,8% do total.
   - Pré-requisitos: Aprovação da minuta padrão e do checklist (processos SEI 002840-39.00/26-3 e 002594-39.00/26-9).
   - Riscos: Caso atípico (outro prestador ou serviço) forçado à minuta padrão; mitigar com análise de desvio.
2. **Dono do processo e rito com prazos por etapa, inclusive para responder ao município** (Lean; impacto alto, esforço baixo): Uma unidade gestora (a DAI, como propõe o processo orientativo) conduz do pedido ao arquivamento, com prazo interno por etapa, resposta ao pedido em prazo fixo e sem encaminhamentos sem conteúdo.
   - Ganho esperado: Reduz as 7,5 passagens medianas, a espera antes de novo pedido do município (16,3% da espera) e as esperas de cauda antes da publicação (q3 de 34,5 du).
   - Pré-requisitos: Instrução normativa do fluxo.
   - Riscos: Conflito de atribuições com DTM e DSI, já levantado no processo orientativo.
3. **Instrução completa num só processo** (Lean; impacto médio, esforço baixo): Inexigibilidade, autorização, parecer, instrumento, publicação e comunicados no mesmo processo de celebração.
   - Ganho esperado: Rastreabilidade e conformidade: a justificativa de inexigibilidade está nos autos em 0% dos contratos (R-CONV-08) e a autorização formal antes da assinatura em 16,7% dos casos.
   - Pré-requisitos: Tipo de processo SEI e modelo de documentos.
   - Riscos: Baixo.
4. **Assinatura eletrônica do município no SEI e publicação por prazo** (IA + Lean; impacto alto, esforço médio): Prefeito assina como usuário externo; extrato gerado do instrumento e publicado em prazo contado da última assinatura; comunicados disparados juntos.
   - Ganho esperado: A publicação responde por 16,1% e a comunicação por 21,3% da espera total.
   - Pré-requisitos: Cadastro de usuário externo; modelo de extrato.
   - Riscos: Município sem certificado ou sem cadastro: manter alternativa.
5. **Painel de prazos e alertas da celebração** (IA + Lean; impacto médio, esforço médio): Idade de cada processo por etapa e unidade, alerta de pedido sem resposta, de prazo vencido do município e do prestador e de processo sem dono.
   - Ganho esperado: Reduz a espera interna (só 14,6% da espera é de terceiros) e o estoque sem marco de encerramento.
   - Pré-requisitos: Relatórios ou API do SEI.
   - Riscos: Painel sem rotina de cobrança não muda nada.
6. **Minuta e checagem assistidas por IA** (IA; impacto médio, esforço médio): Geração da minuta a partir da padrão e verificação automática de cláusulas obrigatórias, fundamento legal e erros materiais (ano de lei, foro, nome do município, número da lei municipal).
   - Ganho esperado: Horas pequenas (mediana de 1,9 h e 2,3 h no teto por ocorrência); o ganho é evitar versões e erratas.
   - Pré-requisitos: Minuta padrão aprovada e base normativa.
   - Riscos: Cláusula alterada sem revisão; mitigar com revisão de toda minuta pela DAJ.

## Indicadores sugeridos

- Lead time do pedido à publicação
- Tempo de resposta ao pedido do município
- Espera antes da publicação contada da assinatura
- Retornos por caso (análise jurídica e minuta)
- Conformidade com os requisitos R-CONV-03 a R-CONV-06
- Processos sem marco de encerramento
- Desvios da minuta padrão por caso

## Perguntas de validação com os servidores

1. As divergências da auditoria às cegas (lista em saida/auditoria) estão corretamente rotuladas na ficha ou pelo auditor?
2. Assinaturas de convênios de 2013–2020 ocorreram em papel ou em sessão do Conselho (Alecrim), fora do SEI? Isso explica a espera antes da publicação.
3. Quem é hoje o dono do processo de celebração: GP, DG, DAJ ou DAI?
4. A inexigibilidade e o TAAC dos contratos de 2025 ficam em processo-mãe? Qual?
5. Em que casos a deliberação do Conselho Superior é obrigatória?
6. Por que pedidos como o de Unistalda ficaram sem resposta até a reiteração?
7. O volume anual de celebrações (hipótese) e o custo-hora estão corretos?

Horas de trabalho são estimativa por peça: hipótese até a calibração com os servidores. A IA não decide: o juízo jurídico, a deliberação e a assinatura ficam com os servidores.
