# Controles, indicadores e metas — celebração de instrumento de delegação

Fonte: `saida/fase3/controles_CONV.json`, montado por `scripts/controles_agergs.py` (linha de base lida dos fatos e da conformidade; metas lidas da simulação) e validado por `scripts/fase3_agergs.py controles`, com 0 problema. Cada meta tem origem em simulação (caminho em `resultado_tobe_CONV.json`) ou em norma (requisito).

## Indicadores

| Id | Indicador | Linha de base | Fato | Meta fase 1 | Meta fase 2 | Meta fase 3 | Origem das metas | Frequência | Responsável |
|---|---|---|---|---|---|---|---|---|---|
| I-CONV-01 | Lead time da celebração | 74,5 du | `coorte.caso.lead.mediana` | 31 | 26,2 | 24,6 | simulacao: fases.<f>.esperado.lead.mediana | trimestral | DAI |
| I-CONV-02 | Divulgação do extrato em até 10 dias úteis da assinatura | 20 % | `conformidade.R-CONV-06` | 40 | 40 | 40 | simulacao: fases.<f>.esperado.conformidade_temporal.R-CONV-06 | mensal | DG |
| I-CONV-03 | Decisão em até 30 dias após a instrução | 33,3 % | `conformidade.R-CONV-09` | 66,7 | 83,3 | 83,3 | simulacao: fases.<f>.esperado.conformidade_temporal.R-CONV-09 | trimestral | GP |
| I-CONV-04 | Atos internos em até 5 dias | 74,6 % | `conformidade.R-CONV-10` | 79,7 | 84 | 84 | simulacao: fases.<f>.esperado.conformidade_temporal.R-CONV-10 | mensal | DAI |
| I-CONV-05 | Horas de trabalho por celebração | 8,6 h | `coorte.caso.horas_teto.mediana` | 6,5 | 5,9 | 5,1 | simulacao: fases.<f>.esperado.horas_teto.mediana | semestral | DAI |
| I-CONV-06 | Retornos por caso (qualidade) | 2 retornos | `coorte.caso.retornos.mediana` | — | — | — | sem meta (qualidade) | trimestral | DAJ |
| I-CONV-07 | Parecer jurídico antes da assinatura | 50 % | `conformidade.R-CONV-03` | 100 | — | — | norma: R-CONV-03 | trimestral | DAJ |
| I-CONV-08 | Instrução completa no processo de celebração | 0 % | `conformidade.R-CONV-08` | 100 | — | — | norma: R-CONV-08 | trimestral | GP |

Definições exatas, alertas e observações:

- **I-CONV-01 — Lead time da celebração.** Dias úteis da primeira peça datada do processo (pedido ou autuação) à última peça (publicação, comunicado ou encerramento); mediana dos processos encerrados no período. Alerta: Processo aberto com idade acima do q3 simulado da fase vigente → Dono do processo (DAI) e Diretoria-Geral. Melhorias: M-CONV-04, M-CONV-05, M-CONV-06, M-CONV-07.
- **I-CONV-02 — Divulgação do extrato em até 10 dias úteis da assinatura.** % dos instrumentos assinados com extrato publicado em até 10 du da última assinatura. Alerta: Instrumento assinado há 7 du sem extrato publicado → DG. Melhorias: M-CONV-05, M-CONV-09. Referência legal: 100% (Lei 14.133, art. 94, II). O TO-BE não chega a 100% porque a espera pela assinatura do município é tempo de terceiro: exige assinatura eletrônica e prazo contratual para o município assinar.
- **I-CONV-03 — Decisão em até 30 dias após a instrução.** % dos processos com autorização, deliberação ou assinatura em até 21 du da última peça de instrução. Alerta: 15 du desde a última instrução sem decisão → Gabinete da Presidência. Melhorias: M-CONV-04. Referência legal: 100% (Lei RS 15.612, art. 53).
- **I-CONV-04 — Atos internos em até 5 dias.** % das ocorrências de tarefa interna com espera antes de até 5 du. Alerta: Processo parado há 5 du na mesma unidade → Unidade com o processo e DAI. Melhorias: M-CONV-04, M-CONV-06, M-CONV-07. Referência legal: 100% (Lei RS 15.612, art. 29).
- **I-CONV-05 — Horas de trabalho por celebração.** Horas-teto estimadas das peças da AGERGS por processo (mediana); calibrar com medição de tempo. Alerta: Processo acima do q3 de horas → DAI. Melhorias: M-CONV-03, M-CONV-08, M-CONV-11, M-CONV-12.
- **I-CONV-06 — Retornos por caso (qualidade).** Número de retornos a atividade já realizada (nova análise jurídica, nova minuta, reenvio) por processo; mediana. Alerta: Terceira versão de minuta no mesmo processo → DAJ. Melhorias: M-CONV-01, M-CONV-02. Indicador de qualidade sem meta simulada: acompanha se a redução de prazo não empurra retrabalho.
- **I-CONV-07 — Parecer jurídico antes da assinatura.** % dos instrumentos assinados com informação jurídica da DAJ ou da PSE nos autos antes da assinatura. Alerta: Minuta enviada para assinatura sem parecer nos autos → DAJ. Melhorias: M-CONV-03.
- **I-CONV-08 — Instrução completa no processo de celebração.** % dos contratos com justificativa de inexigibilidade e autorização no próprio processo. Alerta: Contrato encaminhado à assinatura sem inexigibilidade nos autos → GP. Melhorias: M-CONV-02.

## Controles de qualidade da IA (melhorias de fase 3)

| Id | Melhorias | O que se confere | Amostragem | Critério de aceite | Indicador | Meta | Responsável |
|---|---|---|---|---|---|---|---|
| Q-CONV-01 | M-CONV-10 | Cada pendência e cada dado extraído (escopo, prestador, número e data da lei) conferido contra a peça de origem | 100% das listas de pendência; 2 processos por mês refeitos sem IA | Nenhuma pendência falsa enviada ao município; nenhum documento obrigatório omitido | taxa de erro de extração (campos corrigidos / campos extraídos) | 0 pendência indevida enviada; erro de extração até 5% dos campos (hipótese a calibrar) | DAI |
| Q-CONV-02 | M-CONV-11 | Diferença entre a minuta gerada e a minuta padrão; cada citação de norma conferida contra o texto integral | 100% das minutas | Minuta assinada sem desvio não justificado e sem erro material | desvios não justificados e erratas por instrumento | 0 errata de publicação por erro material | DAJ |
| Q-CONV-03 | M-CONV-12 | Conclusão e fundamentos da pré-análise conferidos pelo assessor; citações conferidas contra a base normativa | 100% das citações; 1 pré-análise por mês refeita às cegas | Nenhuma citação inválida em peça assinada | taxa de citação inválida e de conclusão divergente na amostra cega | 0 citação inválida; divergência de conclusão registrada e analisada | DAJ e Conselho Superior |

## Auditoria contínua

- Testes R-CONV-01 a R-CONV-10 rodando a cada processo encerrado (scripts/fase3_agergs.py conformidade)
