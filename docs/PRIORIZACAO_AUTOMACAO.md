# Priorização da automação — celebração de instrumento de delegação

Fonte: `saida/fase4/matriz_automacao_CONV.json` e `matriz_automacao_CONV.csv` (`scripts/fase3_agergs.py priorizacao`). Critérios, pesos e réguas são os de `metodologia-repo/scripts/comum.py` (`PRIORIZACAO_CRITERIOS`).

## 1. Matriz de critérios

| Critério | Peso | Métrica | Régua (cortes 2–5) | Nota |
|---|---|---|---|---|
| Volume (processos/ano) | 25 | 5 | 5, 10, 25, 50 | 2 |
| Foco em análise (fração das horas em peças de análise) | 15 | 0,511 | 0,2, 0,35, 0,5, 0,65 | 4 |
| Dados (peças de análise com insumo ancorado) | 15 | 0,887 | 0,3, 0,45, 0,6, 0,75 | 5 |
| Regras claras (peças de análise com norma citada) | 20 | 0,566 | 0,4, 0,55, 0,7, 0,85 | 3 |
| Padronização (texto padrão e caminho mais frequente, média) | 15 | 0,234 | 0,3, 0,4, 0,5, 0,6 | 1 |
| Completude (fração das horas em atividades de potencial alto) | 10 | 0,609 | 0,2, 0,35, 0,5, 0,65 | 4 |

**Nota composta: 60** (Σ peso × nota ÷ 5, de 0 a 100), com 18 casos. No caso de referência, P01 (reajuste tarifário) teve nota 80,0 e foi indicado como piloto.

## 2. Portões do piloto

| Portão | Regra | Resultado |
|---|---|---|
| volume_minimo | ≥ 10 processos/ano (régua nota 3) | falha |
| procedimento | situação 'procedimento' (≥ 5 casos e auditoria ≥ 85%) | falha |
| padrao | caminho mais frequente ≥ 30% dos casos | falha |

Prioridade calculada: **não recomendado como piloto de automação completa**.

## 3. Custo × retorno (sistema de IA cobrindo as atividades de potencial alto e médio)

Capacidades necessárias: automação de tramitação (RPA no SEI), busca de precedentes e normas, classificação e triagem, extração de dados de documentos, monitoramento de prazos e alertas, painel e indicadores, redação assistida de minuta, sumarização e linha do tempo, verificação de conformidade. Horas de construção: 876 (isolado) e 416 (incremental, reaproveitando capacidades transversais de outros processos).

| Cenário | Horas liberadas/ano | Retorno/ano (R$) | Construção isolada (R$) | Construção incremental (R$) | Manutenção/ano (R$) | Líquido/ano isolado (R$) | Payback isolado | Payback incremental | Saldo 5 anos isolado (R$) |
|---|---|---|---|---|---|---|---|---|---|
| conservador | 18,3 | 1.610 | 198.000 | 96.800 | 39.600 | -37.990 | não se paga | não se paga | -387.948 |
| esperado | 28,6 | 2.517 | 136.680 | 67.680 | 27.336 | -24.819 | não se paga | não se paga | -260.776 |
| otimista | 39,5 | 3.476 | 92.880 | 46.880 | 18.576 | -15.100 | não se paga | não se paga | -168.380 |

Premissas (custo-hora de desenvolvimento, frações automatizáveis por potencial de IA, horas por capacidade, volume anual e custo-hora dos servidores): **hipótese**, em `premissas` do JSON.

## 4. Horas por atividade (ano, com volume hipotético)

| Atividade | Potencial IA | Horas-teto/ano | Liberadas (cons./esp./otim.) |
|---|---|---|---|
| t6 | alto | 19,9 | 8 / 11,9 / 15,9 |
| t5 | alto | 10,7 | 4,3 / 6,4 / 8,5 |
| t10 | médio | 7 | 1,1 / 2,1 / 3,2 |
| t8 | baixo | 6,5 | 0 / 0,3 / 0,7 |
| t13 | alto | 5,7 | 2,3 / 3,4 / 4,6 |
| t11 | médio | 4,2 | 0,6 / 1,3 / 1,9 |
| t16 | médio | 2,3 | 0,4 / 0,7 / 1,1 |
| t12 | alto | 2,2 | 0,9 / 1,3 / 1,8 |
| t4 | médio | 1,4 | 0,2 / 0,4 / 0,6 |
| t2 | médio | 1,1 | 0,2 / 0,3 / 0,5 |
| t7 | médio | 0,7 | 0,1 / 0,2 / 0,3 |
| t14 | médio | 0,5 | 0,1 / 0,1 / 0,2 |
| t15 | médio | 0,5 | 0,1 / 0,2 / 0,2 |
| t9 | baixo | 0,5 | 0 / 0 / 0 |
| t1 | baixo | 0 | 0 / 0 / 0 |
| t3 | alto | 0 | 0 / 0 / 0 |

## 5. Conclusão

A celebração de instrumento de delegação **não é bom piloto para um sistema de IA de automação completa**. A nota subiu para 60 com os 18 casos, mas os três portões continuam falhando: o volume é baixo (5 por ano, hipótese), não há caminho padrão (18 caminhos em 18 casos) e a situação é indicativa. Em nenhum cenário o retorno em horas cobre a manutenção (no esperado, R$ 2.517/ano de retorno contra R$ 27.336/ano de manutenção). O ganho do processo está nas fases 1 e 2 do TO-BE (fluxo, prazos, modelos e painel), não num sistema dedicado. As capacidades de IA úteis aqui (minuta assistida, verificação de conformidade, extração de documentos) valem a pena como capacidades transversais, construídas para processos de maior volume e reaproveitadas.

> **PARADA 10.** A matriz é insumo. A escolha do piloto do sistema é da gestão da AGERGS.
