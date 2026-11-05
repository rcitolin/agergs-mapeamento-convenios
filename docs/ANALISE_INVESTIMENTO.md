# Análise de investimento — automação da celebração de convênios

04/11/2026 · números de `saida/fase5/analise_investimento_CONV.json`, gerado por `scripts/analise_investimento.py`
(`python3 scripts/analise_investimento.py`). Para refazer com outras premissas, troque as constantes no topo do script.

## 1. Resumo executivo

**Recomendação: não desenvolver o sistema. Fazer antes a alternativa sem sistema (minuta padrão, parecer referencial, checklist e modelos), medindo os tempos reais.**

- Investimento estimado do sistema: R$ 72.161 (com produtividade de 50%, HIPÓTESE) a R$ 140.861 (sem ela), mais R$ 3.700/ano de operação e 20%/ano de manutenção.
- Economia que só o sistema traz, sobre a alternativa sem sistema: 15,9 h/ano, ou R$ 918/ano (faixa R$ 749 a R$ 1.086).
- VPL em 5 anos (8,5% a.a.): −R$ 140.000. Não há payback. O teto de investimento é zero: a operação e a manutenção já superam a economia.
- A alternativa sem sistema custa R$ 5.769, libera 63,8 h/ano (R$ 3.683), paga-se em cerca de 25 meses e tem VPL de +R$ 5.108.
- Todas as horas liberadas são capacidade, não caixa. O sistema geraria saída de caixa real; a economia não.

## 2. O processo hoje

O processo atual consome de 141 a 291 h/ano (médio 216 h), ou R$ 8.115 a R$ 16.807/ano, o equivalente a 0,08 a 0,16 servidor em tempo integral.

**Processo.** Celebração de convênio ou contrato de delegação da regulação entre a AGERGS e municípios, incluindo aditivos e inclusão de novos serviços. Objetivo: formalizar a delegação com base legal, publicidade e comunicação ao prestador.

**Ordem das etapas (AS-IS).** Pedido do município → autuação → análise jurídica → minuta → oitiva do prestador → PSE e Conselho (quando há) → autorização → assinatura → publicação → comunicação → arquivamento. Os 18 casos analisados seguiram 18 caminhos diferentes, com idas e voltas entre jurídico, município e prestador.

**Base de cálculo.**

- Volume: 20 casos/ano (dado do gestor; inclui aditivos).
- Ocorrências por caso: média dos 18 processos do SEI (2013–2026).
- Horas por ocorrência: regra de esforço por peça do diagnóstico (HIPÓTESE, não medida).
- Custo-hora: R$ 10.000/mês ÷ 173,3 h = R$ 57,69/h.
- Horas/ano = 20 × ocorrências por caso × horas por ocorrência. Médio = (mínimo + máximo) ÷ 2.

| Tarefa | Executor | Ocorr./caso | h/ocorr. (mín–máx) | h/ano mín | h/ano médio | h/ano máx | R$/ano médio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| t6 Análise jurídica | DAJ | 1,11 | 1,37–3,58 | 30,4 | 55,0 | 79,6 | 3.173 |
| t5 Elaborar/ajustar minuta | DAJ | 1,06 | 1,20–2,02 | 25,4 | 34,1 | 42,7 | 1.967 |
| Outras peças (encaminhamentos) | várias | 1,00 | 0,65–1,93 | 13,0 | 25,8 | 38,6 | 1.488 |
| t10 Enviar minuta e tratar com o município | GP, DAJ, CS | 1,61 | 0,50–0,87 | 16,1 | 22,1 | 28,1 | 1.275 |
| t8 Deliberação no Conselho | CS, GP | 0,33 | 1,93–3,91 | 12,9 | 19,5 | 26,1 | 1.125 |
| t13 Comunicar prestador e unidades | DG, GP e outras | 1,28 | 0,40–0,89 | 10,1 | 16,5 | 22,8 | 952 |
| t11 Assinatura | CS, GP | 0,72 | 0,90–1,16 | 13,0 | 14,9 | 16,7 | 860 |
| t16 Ouvir o prestador | GP, CS, DG | 0,94 | 0,28–0,49 | 5,3 | 7,3 | 9,3 | 421 |
| t12 Publicar extrato | DG, DTI, CS | 0,83 | 0,27–0,53 | 4,5 | 6,7 | 8,8 | 387 |
| t4 Análise técnica | DSI, DQS, DT | 0,11 | 1,32–2,46 | 2,9 | 4,2 | 5,5 | 242 |
| t2 Autuar e distribuir | GP, DG | 0,50 | 0,17–0,43 | 1,7 | 3,0 | 4,3 | 173 |
| t7 Manifestação da PSE | PSE | 0,11 | 1,03–1,27 | 2,3 | 2,6 | 2,8 | 150 |
| t15 Arquivar | DAJ, DG | 0,11 | 0,58–0,98 | 1,3 | 1,7 | 2,2 | 98 |
| t9 Autorizar e declarar inexigibilidade | DG | 0,06 | 1,06–1,72 | 1,2 | 1,5 | 1,9 | 87 |
| t14 Aditivo | GP | 0,11 | 0,27–0,82 | 0,6 | 1,2 | 1,8 | 69 |
| t1 e t3 Pedido e complementação | Município | 2,11 | 0 (externo) | 0 | 0 | 0 | 0 |
| **Total** |  |  |  | **140,7** | **216,0** | **291,3** | **12.461** |

**Onde está o trabalho.** Análise jurídica e minuta (DAJ) somam 89 h/ano no médio, 41% do total. O restante está espalhado em tramitação, ofícios, assinatura e comunicação, em frações de hora de muitas pessoas.

| Cenário | Mínimo | Médio | Máximo |
| --- | --- | --- | --- |
| Horas/ano | 140,7 | 216,0 | 291,3 |
| Custo/ano (R$) | 8.115 | 12.461 | 16.807 |
| Servidores em tempo integral (÷ 1.800 h) | 0,08 | 0,12 | 0,16 |

## 3. A proposta

A maior parte da mudança é de fluxo e padronização, e não depende de sistema. O sistema acrescenta automação de tramitação e IA sobre um processo já padronizado.

**Três cenários comparados.**

- **Atual (AS-IS):** como mapeado na seção 2.
- **Sem sistema (ganhos rápidos):** dono único (DAI), kit de adesão com checklist, diligência única, minuta padrão, parecer jurídico referencial, modelos de documento no SEI, assinatura do prefeito como usuário externo do SEI, prazos por etapa e painel em planilha. Tudo isso usa recursos que a AGERGS já tem.
- **Automatizado:** os ganhos rápidos mais um sistema com integração ao SEI-RS, conferência de documentos por IA, preenchimento assistido da minuta, pré-análise jurídica, geração automática de ofícios, extrato e comunicados, e alertas de prazo.

**Tempos por tarefa.** Formato: ocorrências por caso × horas por ocorrência (mínimo–máximo). Todos os tempos dos cenários futuros são HIPÓTESE.

| Tarefa | Atual | Sem sistema | Automatizado | Justificativa: o que some, o que fica manual, trabalho novo |
| --- | --- | --- | --- | --- |
| t2 Abrir processo e conferir checklist | 0,50 × 0,17–0,43 | 1 × 0,25–0,50 | 1 × 0,15–0,30 | Passa a ocorrer em todo caso, com o dono único. No sistema, a triagem confere o checklist; o servidor confirma. |
| t3 Diligência ao município | 1,39 × 0 (externo) | 0,50 × 0,30–0,50 | 0,50 × 0,20–0,40 | Uma diligência única em vez de rodadas. É trabalho novo da AGERGS em 50% dos casos (HIPÓTESE). No sistema, o ofício sai do checklist. |
| t4 Análise técnica | 0,11 × 1,32–2,46 | igual | igual | Nenhuma melhoria atua aqui. Continua manual. |
| t5 Minuta | 1,06 × 1,20–2,02 | 1 × 0,60–1,20 | 1 × 0,40–0,80 | Some o ajuste caso a caso: só se preenchem campos da minuta padrão. No sistema, os campos vêm dos documentos; a revisão continua humana. |
| t16 Ouvir o prestador | 0,94 × 0,28–0,49 | 1 × 0,20–0,40 | 1 × 0,15–0,30 | Um ofício com prazo fixo. No sistema, ofício por modelo e alerta de prazo. |
| t6 Análise jurídica | 1,11 × 1,37–3,58 | 1 × 0,60–1,80 | 1 × 0,50–1,50 | O parecer referencial reduz a análise à conferência do enquadramento. A IA faz uma pré-análise; a responsabilidade e a revisão continuam com a DAJ. |
| t7 PSE | 0,11 × 1,03–1,27 | 0,20 × 1,03–1,27 | 0,20 × 1,03–1,27 | Só nos casos com desvio da minuta padrão (20%, HIPÓTESE). Continua manual. |
| t8 Conselho | 0,33 × 1,93–3,91 | 0,40 × 1,93–3,91 | 0,40 × 1,55–3,13 | Só nos desvios (20% dos casos × 2 ocorrências, HIPÓTESE). O relatório assistido ao relator tira 20% do tempo; a deliberação é humana. |
| t9 Autorização e inexigibilidade | 0,06 × 1,06–1,72 | 1 × 0,30–0,60 | 1 × 0,20–0,40 | Passa a ocorrer em todo caso, por modelo. |
| t10 Tratar com o município | 1,61 × 0,50–0,87 | eliminada | eliminada | Absorvida por t3, t16 e t11. |
| t11 Assinatura | 0,72 × 0,90–1,16 | 1 × 0,30–0,50 | 1 × 0,25–0,40 | Assinatura eletrônica no SEI, sem sessão nem correio. Recurso que o SEI já oferece. |
| t12 Publicar extrato | 0,83 × 0,27–0,53 | 1 × 0,15–0,30 | 1 × 0,10–0,20 | Extrato por modelo. No sistema, gerado a partir do instrumento. |
| t13 Comunicar | 1,28 × 0,40–0,89 | 1 × 0,20–0,40 | 1 × 0,10–0,20 | Um comunicado único. No sistema, gerado e enviado pela tramitação. |
| t14 Aditivo | 0,11 × 0,27–0,82 | igual | igual | Fora do escopo da proposta. |
| t15 Encerrar e cadastrar | 0,11 × 0,58–0,98 | 1 × 0,20–0,40 | 1 × 0,10–0,20 | Passa a ocorrer em todo caso. No sistema, o cadastro é automático. |
| Outras peças (encaminhamentos) | 1 × 0,65–1,93 | igual | 1 × 0,45–1,35 | A automação de tramitação tira 30% dos encaminhamentos (HIPÓTESE). Sem sistema, mantido igual. |
| Trabalho novo do sistema | — | — | 12–36 h/ano | Cadastro de modelos e parâmetros, suporte a usuários, tratamento de falhas e de casos que o sistema não resolve: 1 a 3 h/mês (HIPÓTESE). |

**O que continua manual nos dois cenários futuros.** Análise técnica, decisão jurídica, manifestação da PSE, deliberação do Conselho, autorização e assinatura. O sistema só prepara insumos para essas etapas.

**Restrições consideradas (HIPÓTESE, a confirmar).** LGPD (Lei 13.709/2018) para dados de signatários e servidores. Integração com o SEI-RS, provavelmente por RPA, se não houver API disponível. Publicação do extrato no prazo do art. 94 da Lei 14.133/2021. Rito do Conselho Superior no Regimento Interno. Nenhum prazo de entrega foi informado.

## 4. Custo depois da mudança

A alternativa sem sistema captura 80% da economia total (63,8 de 79,7 h/ano no médio). O sistema acrescenta 15,9 h/ano, R$ 918/ano.

| Cenário | Horas/ano mín | médio | máx | R$/ano mín | médio | máx | Servidores (médio) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Atual | 140,7 | 216,0 | 291,3 | 8.115 | 12.461 | 16.807 | 0,12 |
| Sem sistema | 95,1 | 152,2 | 209,2 | 5.486 | 8.778 | 12.070 | 0,08 |
| Automatizado (inclui trabalho novo) | 82,1 | 136,3 | 190,4 | 4.736 | 7.860 | 10.984 | 0,08 |

**Economia anual.** A terceira linha é o ganho que só o sistema traz. É ela que orienta a decisão.

| Comparação | h/ano mín | médio | máx | R$/ano mín | médio | máx | Servidores (médio) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sem sistema × atual | 45,6 | 63,8 | 82,1 | 2.630 | 3.683 | 4.737 | 0,035 |
| Automatizado × atual | 58,6 | 79,7 | 100,9 | 3.379 | 4.601 | 5.823 | 0,044 |
| **Automatizado × sem sistema** | **13,0** | **15,9** | **18,8** | **749** | **918** | **1.086** | **0,009** |

**Ganho concentrado e ganho diluído** (horas/ano, mínimo / médio / máximo).

- *Concentrado* é o das tarefas de análise e decisão, feitas por equipes identificáveis: t4 a t9 (DAJ, PSE, Conselho, Presidência).
- *Diluído* é o de tramitação, ofícios, assinatura, publicação e comunicação, em minutos de muitas pessoas.

| Comparação | Concentrado | Diluído |
| --- | --- | --- |
| Sem sistema × atual | 22,6 / 33,7 / 44,8 | 23,0 / 30,1 / 37,3 |
| Automatizado × atual | 33,7 / 51,4 / 69,0 | 24,9 / 28,4 / 31,9 |
| Automatizado × sem sistema | 11,1 / 17,7 / 24,2 | 1,9 / −1,7 / −5,4 |

- O ganho concentrado do sistema é de 17,7 h/ano no médio, quase todo na DAJ. Isso equivale a pouco mais de duas jornadas por ano e não libera nenhum posto.
- O ganho diluído do sistema é nulo ou negativo: o trabalho novo (cadastro, suporte, falhas) consome o que a automação da tramitação libera.

**Capacidade × caixa.** Nenhuma das economias acima reduz despesa: a folha continua a mesma. São horas que a equipe pode usar em outras tarefas. Do lado do custo, o sistema gera saída de caixa real (construção, operação e manutenção). A alternativa sem sistema consome só horas de servidor.

## 5. Investimento

O sistema custa R$ 72.161 com a premissa de produtividade e R$ 140.861 sem ela. A alternativa sem sistema custa R$ 5.769 em horas de servidor.

**Premissas de construção.**

- Horas por componente: tabela de esforço da metodologia do diagnóstico (HIPÓTESE).
- Desenvolvimento contratado a R$ 150/h técnica: valor central da faixa de R$ 100 a R$ 220 da metodologia (HIPÓTESE).
- Produtividade: as ferramentas atuais reduzem as horas de desenvolvimento em 50% (HIPÓTESE). Não se aplica à validação feita pelos servidores.

| Componente | Horas | R$ sem produtividade | R$ com produtividade (−50%) |
| --- | --- | --- | --- |
| Plataforma: integração SEI-RS, ambiente, trilha de auditoria | 160 | 24.000 | 12.000 |
| Configuração de 13 atividades (16 h cada) | 208 | 31.200 | 15.600 |
| Verificação de conformidade | 100 | 15.000 | 7.500 |
| Extração de dados de documentos | 80 | 12.000 | 6.000 |
| Redação assistida de minuta | 80 | 12.000 | 6.000 |
| Classificação e triagem | 60 | 9.000 | 4.500 |
| Busca de precedentes e normas | 60 | 9.000 | 4.500 |
| Automação de tramitação (RPA no SEI) | 40 | 6.000 | 3.000 |
| Sumarização e linha do tempo | 40 | 6.000 | 3.000 |
| Adequação LGPD e segurança (HIPÓTESE) | 40 | 6.000 | 3.000 |
| Monitoramento de prazos e alertas | 24 | 3.600 | 1.800 |
| Painel e indicadores | 24 | 3.600 | 1.800 |
| Validação por servidores: 30 casos × 2 h × R$ 57,69 | 60 | 3.461 | 3.461 |
| **Total do investimento (I)** | **976** | **140.861** | **72.161** |

**Custos anuais do sistema.**

| Item | R$/ano | Origem |
| --- | --- | --- |
| Manutenção: 20% de I | 14.432 (com produtividade) / 28.172 (sem) | Premissa do roteiro de análise |
| Operação: hospedagem | 3.600 | HIPÓTESE: R$ 300/mês de servidor em nuvem ou PROCERGS |
| Operação: uso de IA | 100 | HIPÓTESE: cerca de 1 milhão de caracteres por caso × 20 casos × R$ 5 por milhão |
| **Operação total (O)** | **3.700** |  |

**Alternativa sem sistema (HIPÓTESE).**

| Item | Horas |
| --- | --- |
| Minuta padrão e parecer referencial (DAJ, com PSE) | 40 |
| Kit de adesão e checklist (DAI) | 16 |
| Modelos de documento no SEI | 16 |
| Treinamento: 10 pessoas × 2 h | 20 |
| Painel de prazos em planilha | 8 |
| **Total** | **100 h = R$ 5.769** |

A manutenção é de 16 h/ano de revisão dos modelos, ou R$ 923/ano.

Esses valores são horas de servidor (custo de capacidade). Não há desembolso.

## 6. Retorno

O sistema não se paga em nenhuma comparação. Contra a alternativa sem sistema, cada hora liberada custa R$ 2.291, 40 vezes o custo-hora do servidor (R$ 57,69).

**Fórmulas.** I = investimento; E = economia anual (R$); O = operação anual; m = 0,20 (manutenção); r = 8,5% a.a.; n = 5 anos; h = horas liberadas por ano.

```
F = Σ (t = 1 a n) 1 / (1 + r)^t = 3,9406
VPL = −I + (E − O − m × I) × F
Payback (anos) = I / (E − O − m × I)          (só se o denominador for positivo)
I_teto = (E − O) × F / (1 + m × F)
Margem (fração da economia que precisa se confirmar) = (I × (1 + m × F) / F + O) / E
Custo por hora liberada = (I / F + m × I + O) / h
```

Na alternativa sem sistema, a manutenção é um valor fixo M = R$ 923/ano, no lugar de m × I, e O = 0.

**Indicadores no cenário médio.**

| Indicador | Sistema × sem sistema (com produtividade) | Sistema × sem sistema (sem produtividade) | Sistema × atual (com produtividade) | Sem sistema × atual |
| --- | --- | --- | --- | --- |
| I (R$) | 72.161 | 140.861 | 72.161 | 5.769 |
| E (R$/ano) | 918 | 918 | 4.601 | 3.683 |
| Custo anual (O + manutenção, R$) | 18.132 | 31.872 | 18.132 | 923 |
| VPL 5 anos (R$) | −139.999 | −262.843 | −125.484 | +5.108 |
| Payback | não há | não há | não há | 25 meses |
| Teto de investimento (R$) | 0 (cálculo dá −6.132) | 0 (−6.132) | 1.985 | 10.876 |
| Fração da economia que precisa se confirmar | 3.972% | 7.369% | 792% | 65% |
| Custo por hora liberada (R$/h) | 2.291 | 4.251 | 457 | 37 |

**Faixa mínimo–máximo** (sistema × sem sistema, com produtividade): VPL de −R$ 140.662 a −R$ 139.335. A largura das faixas de tempo não muda a conclusão.

**Faixa da alternativa sem sistema:** VPL de +R$ 956 a +R$ 9.260 e payback de 41 a 18 meses.

**Leitura.**

- O teto é zero porque a operação (R$ 3.700/ano) já supera a economia incremental (R$ 918/ano). Mesmo um sistema gratuito daria prejuízo.
- Com operação zero, o teto contra a alternativa sem sistema seria de R$ 2.022.
- A alternativa sem sistema se paga se pelo menos 65% da economia estimada se confirmar.

## 7. Incerteza

Nenhuma variação razoável de premissa torna o VPL do sistema positivo. O volume precisaria passar de 20 para cerca de 330 casos/ano.

**Teste de estresse:** tempos atuais no mínimo e tempos futuros no máximo.

| Comparação | Horas/ano antes | Horas/ano depois | Diferença (h/ano) | Diferença (R$/ano) |
| --- | --- | --- | --- | --- |
| Automatizado × atual | 140,7 | 190,4 | −49,7 | −2.867 |
| Automatizado × sem sistema | 95,1 | 190,4 | −95,3 | −5.498 |
| Sem sistema × atual | 140,7 | 209,2 | −68,6 | −3.958 |

- No estresse, nenhum cenário futuro economiza horas, nem mesmo a alternativa sem sistema.
- Causa: as faixas atuais são largas (o máximo é cerca de 2 vezes o mínimo). Além disso, t2, t9 e t15 passam a ocorrer em todos os casos.
- Implicação: a alternativa sem sistema também precisa ser medida antes de ser consolidada. Ela custa R$ 5.769 e é reversível. O sistema custa R$ 72.161 ou mais e não é reversível.

**Sensibilidade, uma premissa por vez.** Base: sistema × sem sistema, cenário médio, com produtividade (I = R$ 72.161, E = R$ 918/ano, O = R$ 3.700/ano, VPL = −R$ 139.999).

| Premissa | Valor testado | Economia (R$/ano) | VPL 5 anos (R$) | Teto (R$) |
| --- | --- | --- | --- | --- |
| Custo-hora do servidor | R$ 40/h | 636 | −141.107 | 0 |
|  | R$ 115,38/h (dobro) | 1.835 | −136.383 | 0 |
| Volume | 10 casos/ano | −234 | −144.534 | 0 |
|  | 40 casos/ano | 3.220 | −130.927 | 0 |
|  | 80 casos/ano | 7.824 | −112.783 | 9.088 |
|  | 330 casos/ano | 36.600 | ≈ 0 | ≈ 72.000 |
| Horizonte | 3 anos | 918 | −116.128 | 0 |
|  | 10 anos | 918 | −185.113 | 0 |
| Taxa de desconto | 5% a.a. | 918 | −146.692 | 0 |
|  | 12% a.a. | 918 | −134.217 | 0 |
| Adesão ao sistema | 50% dos casos | −234 | −144.534 | 0 |
|  | 75% dos casos | 342 | −142.266 | 0 |
| Produtividade no desenvolvimento | 0% | 918 | −262.843 | 0 |
|  | 70% | 918 | −90.861 | 0 |
| R$/h de desenvolvimento | R$ 100/h | 918 | −99.050 | 0 |
|  | R$ 220/h | 918 | −197.326 | 0 |
| Operação anual | R$ 0 | 918 | −125.418 | 2.022 |
|  | R$ 7.400 | 918 | −154.579 | 0 |

- Um horizonte maior piora o VPL: a manutenção e a operação anuais superam a economia, e cada ano a mais soma prejuízo.
- Com menos de 100% de adesão, o trabalho fixo do sistema passa a pesar mais que a economia.
- Teto 0 significa que o cálculo dá negativo: nenhum investimento se paga.

## 8. Alternativas lado a lado

Mudar a norma junto com os ganhos rápidos tem o maior VPL (+R$ 8.427). Desenvolver tem o pior (−R$ 134.887).

Valores no cenário médio, contra o processo atual e em 5 anos a 8,5% a.a.

| Alternativa | Investimento (R$) | Custo anual (R$) | Economia (h/ano) | Economia (R$/ano) | VPL 5 anos (R$) | Payback | Principal risco |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Não fazer nada | 0 | 0 | 0 | 0 | 0 | — | Mantém o lead time mediano de 74,5 dias úteis e o extrato publicado no prazo em só 20% dos casos. |
| Só ganhos rápidos | 5.769 | 923 | 63,8 | 3.683 | +5.108 | 25 meses | Adesão das unidades. Depende da aprovação da minuta padrão e do parecer referencial. |
| Mudar a norma + ganhos rápidos | 7.154 (HIPÓTESE: 124 h) | 923 | 84,5 | 4.877 | +8.427 | 22 meses | Competência e rito para dispensar a deliberação do Conselho (Lei 16.266/2024 e Regimento Interno). |
| Desenvolver (inclui os ganhos rápidos) | 77.930 | 19.055 | 79,7 | 4.601 | −134.887 | não há | Custo anual maior que a economia. Dependência de fornecedor e de integração com o SEI-RS. |
| Comprar solução pronta | desconhecido | desconhecido | ≤ 79,7 | ≤ 4.601 | não calculado | — | Só compensa se o custo total ficar abaixo de R$ 918/ano acima da alternativa sem sistema. |

- **Mudar a norma** (HIPÓTESE): resolução do Conselho Superior que aprova a minuta padrão como modelo. O Conselho passa a deliberar só sobre desvios relevantes (10% dos casos, no lugar de 20%), e a autorização fica no próprio ato de assinatura (t9 eliminada).
- **Faixa do VPL:** de +R$ 2.694 a +R$ 14.157 para mudar a norma, e de +R$ 956 a +R$ 9.260 para só ganhos rápidos.
- **Comprar pronta:** não há preço de mercado nos dados. O limite de R$ 918/ano inclui licença, implantação anualizada e suporte. Na prática, só se aplica a uma ferramenta já contratada pelo Estado, sem custo adicional.
- **Benefício não monetizado:** segundo o diagnóstico, fluxo, modelos e painel (fases 1 e 2, equivalentes à alternativa sem sistema) reduzem o lead time mediano de 74,5 para 26,2 dias úteis (−65%). Com IA, a redução chega a 24,6 dias úteis (−67%). O sistema ganha só 1,6 dia útil a mais.

## 9. Riscos e condições em que o investimento não vale

Com os dados atuais, o investimento no sistema não vale. As condições abaixo dizem o que teria de mudar para a análise ser refeita.

**O sistema não vale se qualquer uma destas condições se mantiver:**

1. Volume abaixo de cerca de 330 casos/ano, nos tempos atuais.
2. Custo anual de operação e manutenção acima da economia incremental (hoje R$ 18.132 contra R$ 918).
3. A alternativa sem sistema ainda não foi implantada e medida. Sem ela, o ganho atribuído ao sistema mistura efeitos de fluxo.
4. Não há API do SEI-RS e a integração depende de RPA, que quebra a cada mudança de tela e aumenta a manutenção.
5. As capacidades de IA são construídas só para este processo, sem reuso em processos de maior volume.

**Riscos do sistema.**

| Risco | Efeito | Direção no resultado |
| --- | --- | --- |
| Erro da IA na conferência ou na minuta | Retrabalho e risco jurídico. A revisão humana continua obrigatória. | Reduz a economia |
| Adesão parcial das unidades | Com 75% de adesão, o VPL cai para −R$ 142.266 | Reduz a economia |
| Mudança no SEI-RS ou na norma | Reconfiguração fora da manutenção prevista | Aumenta o custo |
| LGPD e segurança | Exige relatório de impacto e controle de acesso | Aumenta o custo |
| Dependência de fornecedor | Custo de troca e de continuidade | Aumenta o custo |

**Riscos da alternativa sem sistema.**

- Os tempos futuros são estimativas. No teste de estresse, a economia some.
- A minuta padrão e o parecer referencial dependem de aprovação da DAJ e da PSE.
- Sem um dono do processo efetivo, as etapas voltam ao padrão atual.

**Quando reavaliar o sistema.** Quando a alternativa sem sistema tiver 12 meses de medição. Ou quando capacidades de IA já construídas para outros processos puderem ser usadas aqui só com custo de configuração, e com custo de operação marginal próximo de zero.

## 10. Premissas, o que ficou fora e como medir

Só o volume e o custo-hora são dados informados. Todo o resto é HIPÓTESE a medir.

| Premissa | Valor usado | Situação | Como medir |
| --- | --- | --- | --- |
| Volume | 20 casos/ano | Dado do gestor (inclui aditivos) | Cadastro de municípios conveniados e fila de pedidos. Separar aditivos de celebrações novas. |
| Custo-hora do servidor | R$ 57,69 | Dado do gestor | Tabela de vencimentos e encargos por cargo |
| Ocorrências por caso (AS-IS) | média de 18 processos | Medido nos autos do SEI | Relatório de andamentos do SEI-RS |
| Horas por ocorrência (AS-IS) | regra de esforço por peça | HIPÓTESE | Cronometrar 5 peças de cada tipo (parecer, minuta, ofício) com quem executa |
| Tempos futuros por tarefa | seção 3 | HIPÓTESE | Piloto da alternativa sem sistema com 5 casos |
| Casos com desvio (PSE e Conselho) | 20% | HIPÓTESE | Contar após a minuta padrão |
| Casos com diligência | 50% | HIPÓTESE | Contar após o checklist |
| Trabalho novo do sistema | 12–36 h/ano | HIPÓTESE | Registro de chamados em sistemas similares |
| Horas de construção | 916 h + 60 h de validação | HIPÓTESE (metodologia do diagnóstico) | Estimativa da DTI ou da PROCERGS |
| R$/h de desenvolvimento | R$ 150 | HIPÓTESE | Contrato vigente ou cotação |
| Produtividade no desenvolvimento | 50% | HIPÓTESE | Histórico de projetos recentes da DTI |
| Operação anual | R$ 3.700 | HIPÓTESE | Cotação de hospedagem e de uso de IA |
| Manutenção | 20% de I por ano | Premissa do roteiro | Contratos de sustentação similares |
| Implantação da alternativa sem sistema | 100 h | HIPÓTESE | Registro das horas gastas na implantação |

**Fora da conta e direção do efeito.**

| Item fora da conta | Puxaria o resultado para |
| --- | --- |
| Redução do prazo (lead time) e da espera dos municípios | A favor das duas alternativas, quase toda a favor da alternativa sem sistema |
| Início antecipado da cobrança da taxa de regulação | A favor das duas alternativas, quase toda a favor da alternativa sem sistema |
| Reuso das capacidades de IA em outros processos | A favor do sistema. Mesmo assim, a operação e a manutenção superam a economia incremental. |
| Aditivos mais leves que celebrações completas | Contra as duas alternativas |
| Treinamento e gestão da mudança do sistema | Contra o sistema |
| Retrabalho por erro da IA | Contra o sistema |
| Melhoria de conformidade (extrato no prazo, decisão em 30 dias) | A favor das duas alternativas, sem valor monetário |
| Esforço dos municípios e do prestador | Fora do escopo (custo de terceiros) |

**Fontes.**

- Diagnóstico do processo de celebração: 18 processos do SEI-RS, de 2013 a 2026 (`saida/fase2/casos_CONV.json`).
- Simulação TO-BE (`docs/TOBE_SIMULACAO.md`).
- Matriz de priorização da automação (`docs/PRIORIZACAO_AUTOMACAO.md`).
- Premissas de construção (`metodologia-repo/scripts/comum.py`).
