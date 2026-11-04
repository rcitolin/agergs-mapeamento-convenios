# TO-BE e simulação — celebração de convênio ou contrato de delegação da regulação

Processo `CONV` (18 casos: convênios, contratos de prestação de serviços de regulação e um aditivo, de 2013 a 2026). Fontes: `saida/fase3/linha_base_CONV.json`, `melhorias_CONV.json` e `resultado_tobe_CONV.json`, gerados por `scripts/fase3_agergs.py` (etapas `linha_base` e `tobe`). Nenhum número deste texto foi digitado: todos foram copiados das saídas.

> **Situação: indicativo.** São 18 casos (menos de 15 por tipo de instrumento, então as medianas são instáveis). As datas vêm das peças, não dos andamentos do SEI, e a auditoria às cegas dos rótulos ficou abaixo de 85% nas peças substantivas (81,6%). Horas, custo e todos os parâmetros dos cenários são **hipótese, a calibrar com os servidores**.

## 1. Linha de base (congelada)

Carimbo: `bfc078f1dd509dfa…`

| Medida | n | Média | Mediana | q1 | q3 | Máx |
|---|---|---|---|---|---|---|
| Lead time por caso (du) | 18 | 107,9 | 74,5 | 23 | 135,8 | 376 |
| Lead até a assinatura (du) | 12 | 75,1 | 37 | 1,5 | 107 | 299 |
| Horas-piso por caso (h) | 18 | 7 | 4,8 | 3,5 | 6,1 | 35,8 |
| Horas-teto por caso (h) | 18 | 14,6 | 8,6 | 6,3 | 12,1 | 88,4 |
| Espera de terceiros por caso (du) | 18 | 13,6 | 1 | 0 | 9 | 91 |

Por ano, com volume de 5 celebrações (**hipótese**: hipótese: celebrações iniciadas em 2025 na amostra (Lagoa Bonita do Sul, Nova Bréscia, Passa Sete, Minas do Leão, Passo Fundo); confirmar com o cadastro de municípios conveniados): 35–73 h, ou 0,02–0,05 FTE. Isso custa R$ 1.925 (piso), R$ 4.752 (esperado) e R$ 8.833 (teto), com custo-hora hipotético.

Conformidade temporal na linha de base: R-CONV-06 (extrato em até 10 du) 20%; R-CONV-09 (decisão em até 30 dias da instrução) 33,3%; R-CONV-10 (ato interno em até 5 dias) 74,6%.

## 2. Melhorias (três fases cumulativas)

| Id | Fase | Título | Efeito | Atividades | Conserv. | Esperado | Otim. | Benchmark | Hipótese |
|---|---|---|---|---|---|---|---|---|---|
| M-CONV-01 | 1 | Kit de adesão com checklist único de documentos mínimos | `elimina_laco_pct` | t3, t6, t10 | 30% | 50% | 70% | BM-05, BM-04 | sim |
| M-CONV-02 | 1 | Minuta padrão única aprovada previamente | `elimina_laco_pct` | t5, t7, t8 | 40% | 60% | 80% | BM-02, BM-03, BM-11 | sim |
| M-CONV-03 | 1 | Parecer jurídico referencial sobre a minuta padrão | `reduz_horas_pct` | t6, t7 | 30% | 50% | 70% | BM-01, BM-02 | sim |
| M-CONV-04 | 1 | Dono do processo e prazo interno por etapa | `teto_espera` | t4, t5, t6, t8, t9 | 20 du | 10 du | 5 du | — | sim |
| M-CONV-05 | 1 | Publicação do extrato em prazo contado da última assinatura | `teto_espera` | t12 | 10 du | 10 du | 5 du | BM-06, BM-10 | não |
| M-CONV-06 | 1 | Comunicado único pós-assinatura e encerramento em prazo fixo | `teto_espera` | t13, t15 | 15 du | 5 du | 2 du | — | sim |
| M-CONV-07 | 2 | Painel de prazos e alertas da celebração | `teto_espera` | t10, t16, t2 | 10 du | 5 du | 3 du | — | sim |
| M-CONV-08 | 2 | Documentos por modelo: extrato, comunicados, ofícios e termo de encerramento | `reduz_horas_pct` | t10, t12, t13, t15 | 20% | 40% | 60% | BM-11 | sim |
| M-CONV-09 | 2 | Assinatura eletrônica do prefeito como usuário externo do SEI | `reduz_espera_pct` | t11 | 20% | 40% | 60% | BM-13 | sim |
| M-CONV-10 | 3 | Conferência da documentação do município por IA | `elimina_laco_pct` | t3, t6 | 10% | 20% | 30% | — | sim |
| M-CONV-11 | 3 | Minuta assistida e checagem de erros materiais | `reduz_horas_pct` | t5, t14 | 15% | 30% | 45% | BM-11 | sim |
| M-CONV-12 | 3 | Pré-análise jurídica e relatório ao relator assistidos | `reduz_horas_pct` | t6, t7, t8 | 10% | 20% | 30% | — | sim |

As melhorias de fase 3 (IA) trazem `controle_humano` e o ganho de horas já descontado da revisão. A justificativa de cada parâmetro está em `justificativa_parametro`.

## 3. Resultado da simulação

| Fase | Cenário | Lead mediano (du) | Ganho no lead mediano | Lead médio (du) | q1–q3 (du) | Horas-teto médias (h) | Ganho em horas | R-CONV-06 | R-CONV-09 | R-CONV-10 |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 (AS-IS) | — | 74,5 | — | 107,9 | 23–135,8 | 14,6 | — | 20% | 33,3% | 74,6% |
| 1 | conservador | 41,8 | −43,9% | 71,1 | 16,8–78,6 | 12 | −17,8% | 40% | 50% | 74,6% |
| 1 | esperado | 31 | −58,4% | 60,6 | 14,2–77,4 | 10,6 | −27,4% | 40% | 66,7% | 79,7% |
| 1 | otimista | 26,4 | −64,6% | 51,5 | 11,2–62,8 | 9,4 | −35,6% | 40% | 66,7% | 91,1% |
| 2 | conservador | 40,4 | −45,8% | 68,8 | 16,8–74,9 | 11,5 | −21,2% | 40% | 66,7% | 74,6% |
| 2 | esperado | 26,2 | −64,8% | 55,9 | 13,2–69,9 | 9,6 | −34,2% | 40% | 83,3% | 84% |
| 2 | otimista | 17,6 | −76,4% | 45 | 10,2–61,4 | 8 | −45,2% | 40% | 83,3% | 95,2% |
| 3 | conservador | 39,1 | −47,5% | 68,4 | 16,8–74,8 | 10,7 | −26,7% | 40% | 66,7% | 74,6% |
| 3 | esperado | 24,6 | −67% | 55,4 | 13,2–69,9 | 8,5 | −41,8% | 40% | 83,3% | 84% |
| 3 | otimista | 16,2 | −78,3% | 44,6 | 10,2–61,4 | 6,7 | −54,1% | 40% | 83,3% | 95,2% |

Leitura: no cenário esperado, a fase 1 (só ajuste de fluxo) leva o lead mediano de 74,5 du para 31 du (−58,4%). As fases 2 e 3 levam a 24,6 du (−67%) e reduzem sobretudo horas (−41,8% nas horas-teto médias). É o mesmo padrão do caso de referência: o tempo é espera, e o ajuste do fluxo rende mais que a IA. O R-CONV-06 fica em 40% no cenário esperado, porque a espera antes da publicação inclui a assinatura do município, que é tempo de terceiro e é protegida (ver §5).

## 4. Sensibilidade (fase 3, cenário esperado: quanto piora sem cada melhoria)

| Melhoria | Fase | Δ lead mediano (du) | Δ lead médio (du) | Δ horas médias (h) |
|---|---|---|---|---|
| M-CONV-06 | 1 | 14,8 | 18,3 | 0 |
| M-CONV-04 | 1 | 2 | 7,1 | 0 |
| M-CONV-05 | 1 | 10,2 | 6,7 | 0 |
| M-CONV-01 | 1 | 5,8 | 5,6 | 0,6 |
| M-CONV-07 | 2 | 4 | 2,6 | 0 |
| M-CONV-09 | 2 | 2,8 | 2,1 | 0 |
| M-CONV-02 | 1 | 0 | 1,5 | 0,6 |
| M-CONV-10 | 3 | 1,6 | 0,5 | 0,1 |
| M-CONV-03 | 1 | 0 | 0 | 1,2 |
| M-CONV-08 | 2 | 0 | 0 | 1 |
| M-CONV-11 | 3 | 0 | 0 | 0,6 |
| M-CONV-12 | 3 | 0 | 0 | 0,4 |

As de maior peso no lead médio, e que mais precisam de validação, são M-CONV-06, M-CONV-04, M-CONV-05.

## 5. Premissas, proteções e hipóteses

- **Esperas protegidas.** A espera antes de uma peça do município ou do prestador que **responde a algo da AGERGS** é tempo de terceiro. `teto_espera` e `reduz_espera_pct` não a cortam. Reiteração do município depois de outra peça externa (pedido sem resposta) conta como espera da agência. A espera de terceiros responde por 14,6% da espera total da coorte (`coorte.pct_espera_terceiros`). Nenhuma melhoria corta prazo dado ao município ou ao prestador: o validador barra `teto_espera` em t1 e t3.
- **Lead simulado** = lead AS-IS − (redução de espera + redução de execução). O tempo não coberto por atividade continua igual.
- **Conformidade simulada.** O simulador refaz as datas das ocorrências em dias úteis e roda de novo os testes R-CONV-06, R-CONV-09 e R-CONV-10.
- **Volume anual: 5 celebrações (hipótese).** Custo-hora R$ 55/88/121 (piso/esperado/teto), **hipótese**.
- **Parâmetros dos cenários.** Nenhum benchmark encontrado reporta ganho numérico. Os casos citados sustentam a prática, não o percentual, e por isso 11 das 12 melhorias são `hipotese: true`. A exceção é M-CONV-05, cujo teto vem do prazo legal (Lei 14.133, art. 94, II).
- Validação: `validar_tobe` com 0 problema: fatos, requisitos e benchmarks existem, os cenários são monotônicos e a fase 3 tem controle humano.
