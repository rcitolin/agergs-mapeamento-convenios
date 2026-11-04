# Método adaptado — AGERGS, celebração de convênios e contratos de delegação da regulação

Este documento registra como a metodologia do repositório
[`mapeamento-processos-sei`](https://github.com/RaulAraujoSilva/mapeamento-processos-sei) foi aplicada ao processo de **celebração de convênio ou
contrato pelo qual um município delega à AGERGS a regulação de serviço público** (em regra, água e esgoto prestados
pela CORSAN), e o que precisou mudar em relação ao caso de referência (AGENERSA/RJ).

## 1. Base disponível × base do método

| Item | Caso de referência (AGENERSA) | Este caso (AGERGS) | Consequência |
|---|---|---|---|
| Origem | Coleta na Pesquisa Pública do SEI-RJ (andamentos + peças) | 20 PDFs exportados do SEI-RS, entregues pelo aluno (14 na 1ª entrega, 6 na 2ª) | Coletor (`coleta/`) não usado |
| Andamentos (trilha de unidades) | Sim | **Não** (o PDF só traz as peças) | Trilha, posse e espera reconstruídas pela data de assinatura de cada peça |
| Processos | 251, vários tipos | 18 processos de celebração (2013–2026, um deles aditivo) + 2 processos de gestão (orientativo e minuta padrão) | Um só tipo de processo; coorte = piloto |
| Texto das peças | Extraído do SEI | `pdftotext -layout`; peças digitalizadas sem texto ficam marcadas `baixo_texto` | Fichas dessas peças só com o cabeçalho |

## 2. Etapas executadas e equivalência com o repositório

| Fase | Etapa do método | Aqui | Script ou especificação | Verificação |
|---|---|---|---|---|
| 0 | Coleta e base | Segmentação dos PDFs por rodapé SEI e captura das assinaturas | `scripts/base_documentos.py` → `dados/documentos.csv`, `dados/assinaturas.csv` | 381 documentos, 233 assinaturas |
| 0 | Trilha, tempo e posse | Linha do tempo por peça datada; espera atribuída à unidade que age depois; tempo de terceiros por unidade (município/prestador) | `scripts/pipeline_agergs.py` (etapas `linha`, `fase0`) | Testes de regra embutidos (dias úteis com feriados do RS) |
| 0 | Classificação no catálogo | Catálogo de um tipo (CONV), dois instrumentos (convênio 2018–2020; contrato de prestação de serviços de regulação 2025–2026) | narrativas por caso | — |
| 1 | Ficha de trabalho por peça | 21 agentes em paralelo, um por processo (Passo Fundo em dois) | `ESPECIFICACAO_FICHAS.md` (adaptação do prompt ficha-v2) | Ancoragem literal por código: 100% das evidências |
| 1 | Esforço piso–teto | Regra de `comum.horas_modelo` (lauda, complexidade, insumos) | `pipeline_agergs.py::esforco` | Hipótese até calibração |
| 1–2 | Modelo BPMN canônico | AS-IS com 24 elementos e 7 raias; TO-BE com 22 elementos | `saida/bpmn/modelo_CONV*.json` (ESPECIFICACAO_MODELO) | Gerador do repositório (`gerar_bpmn.py`) via `scripts/gerar_bpmn_agergs.py`: 0 falha |
| 2 | Rótulo de atividade e auditoria às cegas | Rótulo na ficha; mapa atividade → tarefa no código; auditor independente sem acesso às fichas | `ATIV_TAREFA`; `fase3_agergs.py auditoria` | 2 rodadas, 97 peças: **81,6% nas substantivas, abaixo de 85% → PARADA** |
| 2 | Procedimento e fatos | `procedimento_CONV.json`, `fatos_CONV.json` (fatos com sha) | `pipeline_agergs.py` | Duas rodadas, arquivos idênticos |
| 2 | Avaliação AS-IS | Lean, VSM, TOC, análise de valor e IA | `saida/bpmn/avaliacao_CONV.modelo.json` → `avaliacao_CONV.json` (ESPECIFICACAO_AVALIACAO v3; números entram por marcador `{F:id}`) | Validador de números sem lastro: 0 problema |
| 3 | Base normativa e conformidade | 10 arquivos de norma (9 integrais, 1 parcial); 10 requisitos com trecho literal; 8 testáveis | `normas/`, `saida/fase3/normas_CONV.json`, `fase3_agergs.py normas conformidade` | 10/10 trechos conferidos literalmente |
| 3 | Benchmarking | 13 práticas com URL aberta | `dados/referencia/benchmark.json` | Ressalvas de verificação registradas |
| 3 | Linha de base, TO-BE e simulação | 12 melhorias em 3 fases, 3 cenários, sensibilidade | `melhorias_CONV.json`, `fase3_agergs.py linha_base tobe` | Validador do TO-BE: 0 problema |
| 3 | Controles e metas | 8 indicadores, 3 controles de qualidade da IA | `controles_CONV.json`, `fase3_agergs.py controles` | 0 problema |
| 4 | Priorização da automação | Mesmos critérios, pesos e réguas de `comum.PRIORIZACAO_CRITERIOS` | `fase3_agergs.py priorizacao` | Premissas marcadas como hipótese |

## 3. Regras novas criadas para esta base (e por quê)

1. **Data da peça** = data da primeira assinatura eletrônica; sem assinatura, a data escrita no texto (extraída na
   ficha); sem nenhuma, herda a data corrente do processo (juntada aproximada).
2. **Início do processo** = primeira peça datada, na ordem dos autos, que não é anexo histórico (lei municipal,
   plano, contrato do prestador); peça com data só no texto e anterior a esse início herda a data corrente. Sem essa
   regra, anexos de 2009–2010 inflavam o lead time de Mata e Panambi para mais de 2.000 du, e uma data errada na
   minuta de Campinas das Missões antecipava o início em oito meses.
3. **Espera de terceiros** = espera antes de peça do município ou do prestador que responde a algo da AGERGS. Peça
   externa logo depois de outra peça externa (reiteração do pedido, como em Unistalda) é silêncio da agência e conta
   como espera interna. A espera de terceiros é protegida no TO-BE (nenhuma melhoria a corta).
4. **Consulta ao prestador antes da assinatura** vira tarefa própria (t16); depois da assinatura é comunicação (t13).
5. **Encaminhamento sem conteúdo** não vira tarefa: conta como passagem (regra 2 da ESPECIFICACAO_MODELO).
6. **Dias da Lei RS 15.612** (arts. 29 e 53) medidos em dias úteis: 5 dias → 5 du (leitura favorável ao órgão);
   30 dias → 21 du (aproximação). Fica declarado no requisito.

## 4. PARADAS para o aluno (validação humana obrigatória)

| Parada | Motivo | O que decidir |
|---|---|---|
| Auditoria às cegas | Concordância de 81,6% nas peças substantivas (2 rodadas, 97 peças), abaixo de 85% | Revisar as divergências em `saida/auditoria/auditoria_classificador_CONV.json`; 3 já corrigidas em `dados/correcoes_rotulos.json` |
| Normas de fonte secundária | Leis RS 16.266/2024, 15.612/2021 e 10.931/1997 vieram de sites não oficiais | Conferir no DOE-RS ou na AL-RS os trechos citados |
| Premissas de custo e volume | Volume anual (5) e custo-hora são hipótese | Informar o número real de celebrações por ano e o custo-hora |
| Dono do processo | A DAI como dono segue a proposta do processo orientativo; a DTM contestou | Decisão da gestão |
| Piloto de automação | A matriz é insumo; a escolha é da gestão (PARADA 10 do roteiro) | — |

## 5. Limites declarados

- O mapa cobre o que está nas peças: telefonemas, reuniões e assinaturas em papel fora do SEI não aparecem.
- Sem andamentos, não se separa a fila dentro de uma unidade do trabalho em si; a espera é inferida entre peças.
- Com 18 casos, medianas ainda são instáveis (menos de 15 casos): os números são indicativos.
- Parte da instrução dos contratos de 2025 (inexigibilidade, TAAC) está em processos-mãe que não foram entregues.
- Peças digitalizadas sem texto (OCR pendente) só têm ficha pelo cabeçalho.
