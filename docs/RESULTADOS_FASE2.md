# Fase 2 — do caso ao procedimento: coorte de 18 celebrações

04/11/2026 · procedimento em `saida/fase2/procedimento_CONV.json` · linha do tempo por caso em
`saida/fase2/casos_CONV.json` · fatos citáveis em `saida/bpmn/fatos_CONV.json` · modelo canônico em
`saida/bpmn/modelo_CONV.json` (diagrama em `saida/bpmn/CONV.bpmn` e `docs/bpmn/index.html`).

## 1. Coorte e situação

- **Coorte**: os 18 processos de celebração — 12 convênios de delegação (2013–2020 e 2026), 5 contratos de prestação
  de serviços de regulação (2025–2026) e 1 termo aditivo (Chiapetta, 2021). Os 2 processos de gestão de 2026 ficam
  fora da coorte e servem de referência para o TO-BE.
- **Rótulo de atividade**: cada peça recebeu, na ficha, uma das 26 atividades da especificação. Uma tabela fixa
  (`ATIV_TAREFA` em `scripts/pipeline_agergs.py`) liga a atividade a uma das 16 tarefas do modelo canônico.
  Encaminhamento puro não vira tarefa; conta só como passagem. Comunicação ao prestador antes da assinatura vira
  t16 ("Ouvir o prestador sobre a minuta"); depois da assinatura, t13.
- **Situação: indicativo.** O método exige pelo menos 5 casos **e** concordância às cegas de pelo menos 85% nas peças
  substantivas para chamar o fluxo de procedimento. Há 18 casos, mas a auditoria deu 81,6% nas duas rodadas somadas
  (seção 5). Os números valem como ordem de grandeza. Com 18 casos, ainda perto do limite de uns 15, as medianas
  continuam instáveis.

## 2. Distribuição por atividade

Fonte: fatos `coorte.<tN>.*`. Espera em du, por ocorrência. Horas = mediana por ocorrência no teto (hipótese).

| Tarefa | Nome | Casos (%) | Ocorrências | Casos com laço | Espera antes: mediana | q3 | máx | Horas teto | % da espera total |
|---|---|---|---|---|---|---|---|---|---|
| t1 | Solicitar delegação da regulação | 12 (66,7%) | 13 | 1 | 0 | 0 | 181 | 0 | 16,3 |
| t2 | Autuar pedido e distribuir às unidades | 8 (44,4%) | 9 | 1 | 1 | 3 | 9 | 0,4 | 1,2 |
| t3 | Complementar documentação e lei autorizativa | 15 (83,3%) | 25 | 7 | 0 | 0 | 32 | 0 | 5,0 |
| t4 | Analisar aspectos técnicos da delegação | 2 (11,1%) | 2 | 0 | 1 | 1 | 1 | 2,5 | 0,1 |
| t5 | Elaborar ou ajustar minuta do instrumento | 12 (66,7%) | 19 | 5 | 0 | 9 | 153 | 1,9 | 13,8 |
| t6 | Analisar juridicamente o pedido | 11 (61,1%) | 20 | 8 | 3,5 | 14,5 | 48 | 2,3 | 10,5 |
| t16 | Ouvir o prestador sobre a minuta | 3 (16,7%) | 17 | 2 | 1 | 4 | 26 | 0,6 | 4,0 |
| t7 | Emitir manifestação da Procuradoria Setorial | 2 (11,1%) | 2 | 0 | 0 | 0 | 0 | 1,3 | 0,0 |
| t8 | Deliberar sobre a celebração no Conselho | 3 (16,7%) | 6 | 2 | 0,5 | 1,8 | 17 | 4,2 | 1,2 |
| t9 | Autorizar celebração e inexigibilidade | 1 (5,6%) | 1 | 0 | 0 | 0 | 0 | 1,7 | 0,0 |
| t10 | Enviar minuta e tratar com município | 10 (55,6%) | 29 | 4 | 0 | 1 | 13 | 0,6 | 2,3 |
| t11 | Assinar o instrumento pelas partes | 12 (66,7%) | 13 | 1 | 0 | 14 | 32 | 0,9 | 5,5 |
| t12 | Publicar extrato no Diário Oficial | 12 (66,7%) | 15 | 2 | 2 | 34,5 | 76 | 0,5 | 16,1 |
| t13 | Comunicar prestador e unidades internas | 9 (50,0%) | 23 | 4 | 3 | 10 | 150 | 0,6 | 21,3 |
| t14 | Instruir aditivo ao instrumento | 2 (11,1%) | 2 | 0 | 0,5 | 0,8 | 1 | 0,8 | 0,1 |
| t15 | Arquivar o processo | 2 (11,1%) | 2 | 0 | 21,5 | 31,8 | 42 | 1,0 | 2,6 |

**Leitura.** As esperas medianas por ocorrência são curtas; o tempo se acumula nas caudas. Cinco tarefas concentram
78,0% da espera total da coorte: comunicação pós-assinatura (21,3%), novo pedido do município (16,3%), publicação
(16,1%), minuta (13,8%) e análise jurídica (10,5%). Essa soma foi calculada em python a partir de
`coorte.<tN>.pct_espera_total`. A espera antes de t1 é nova nesta rodada: o máximo de 181 du é o pedido de Unistalda,
reiterado pelo município sem resposta registrada. Etapas que a lei e o processo orientativo pedem são raras nos
autos: análise técnica em 2 casos, manifestação da PSE em 2, deliberação do Conselho em 3 e autorização formal em 1.

## 3. Por caso

Fatos `coorte.caso.*` (n = 18, exceto o lead até a assinatura, com n = 12):

| Medida | Mediana | q3 | Máximo |
|---|---|---|---|
| Lead time (du) | 74,5 | 135,8 | 376 |
| Lead até a assinatura (du) | 37 | 107 | 299 |
| Espera entre atividades (du) | 74,5 | 99,2 | 287 |
| Execução das atividades (du) | 0,5 | 10,2 | 100 |
| Tempo de terceiros (du) | 1 | 9 | 91 |
| Horas piso / teto | 4,8 / 8,6 | 6,1 / 12,1 | 35,8 / 88,4 |
| Peças | 13 | 17 | 99 |
| Encaminhamentos sem conteúdo | 3 | 4 | 16 |
| Passagens entre unidades | 7,5 | 10,8 | 64 |
| Retornos a atividade já feita | 2 | 3 | 33 |

Eficiência do ciclo (PCE) no teto: 1,7% (`coorte.pce_teto`). Execução no lead somado: 14,3%. Espera de terceiros:
14,6% da espera total (com a regra nova, a reiteração do município conta como espera da agência).

Por instrumento (`coorte.instrumento.*`): lead mediano de 79,5 du nos 12 convênios, 15 du nos 5 contratos e 3 du no
aditivo.

## 4. Caminhos e transições

- **18 caminhos distintos em 18 casos** (`coorte.n_caminhos`): não há um caminho típico. Os três contratos que chegam
  assinados têm o caminho mínimo (assinatura → publicação → comunicação), e o aditivo de Chiapetta só registra súmula,
  publicação e comunicação. Passo Fundo e Minas do Leão têm caminhos com dezenas de ocorrências, em laço entre minuta,
  envio ao município, oitiva da CORSAN e deliberação.
- **Transições mais frequentes** (`procedimento_CONV.json`): envio ao município → complementação (9; 31,0% das saídas
  de t10); análise jurídica → minuta (9; 45,0% das saídas de t6); minuta → análise jurídica (7; 36,8% das saídas de
  t5); assinatura → comunicação (5; 45,5%); envio ao município → oitiva do prestador (5; 17,2%); comunicação → oitiva
  do prestador (5; 25,0%); oitiva do prestador → envio ao município (5; 29,4%); minuta → envio ao município (5; 26,3%).
- **Laços**: a análise jurídica se repete em 8 casos, a complementação em 7, a minuta em 5, o envio ao município em 4,
  a comunicação em 4, a deliberação do Conselho em 2 e a oitiva do prestador em 2. O vaivém minuta ↔ análise jurídica
  é o laço mais comum.

## 5. Auditoria às cegas do rótulo de atividade

`saida/auditoria/auditoria_classificador_CONV.json`. Duas rodadas, cada uma com amostra estratificada de peças com
texto (até 3 por atividade, semente fixa) e um auditor independente que não via as fichas nem o gabarito: a 1ª
sobre os 12 casos iniciais, a 2ª sobre os 6 processos novos.

| Medida | Rodada 1 | Rodada 2 | Total |
|---|---|---|---|
| Peças | 60 | 37 | 97 (todas rotuladas pelo auditor) |
| Concordância na atividade (26 rótulos) | 71,7% | 73,0% | 72,2% |
| Concordância na tarefa do modelo | 78,3% | 78,4% | 78,4% |
| Peças substantivas (que viram tarefa) | 54 | 33 | 87 |
| Concordância na tarefa, peças substantivas | 83,3% | 78,8% | **81,6%**, abaixo do critério de 85% |

Os valores por rodada foram calculados em python a partir de `gabarito_oculto*.json`, `rotulos_auditor*.json` e
`ATIV_TAREFA`; o total é o do arquivo da auditoria.

As 21 divergências (ficha → auditor):

| Peça | Ficha | Auditor | Rodada |
|---|---|---|---|
| Alecrim #3 | assinatura_instrumento | deliberacao_conselho_superior | 2 |
| Arambaré #13 | arquivamento_encerramento | encaminhamento_interno | 1 |
| Campinas das Missões #5 | comunicacao_interna_pos_assinatura | encaminhamento_interno | 2 |
| Campinas das Missões #8 | envio_minuta_ao_municipio | elaboracao_minuta | 2 |
| Capão Bonito do Sul #2 | autuacao_abertura | encaminhamento_interno | 1 |
| Capão Bonito do Sul #5 | analise_juridica | manifestacao_pge | 1 |
| Capão Bonito do Sul #10 | autuacao_abertura | decisao_presidencia_diretoria | 1 |
| Chiapetta #6 | comunicacao_interna_pos_assinatura | encaminhamento_interno | 2 |
| Liberato Salzano #9 | juntada_documentos_municipio | solicitacao_municipio | 2 |
| Liberato Salzano #12 | outro | tratativa_com_municipio | 2 |
| Mampituba #13 | analise_tecnica | encaminhamento_interno | 1 |
| Mata #9 | documento_externo_anexo | tratativa_com_municipio | 1 |
| Panambi #11 | outro | tratativa_com_municipio | 1 |
| Panambi #12 | comunicacao_interna_pos_assinatura | tratativa_com_municipio | 1 |
| Passa Sete #1 | outro | assinatura_instrumento | 1 |
| Passo Fundo #14 | decisao_presidencia_diretoria | comunicacao_prestador | 1 |
| Passo Fundo #21 | encaminhamento_interno | tratativa_com_municipio | 1 |
| Passo Fundo #57 | outro | tratativa_com_municipio | 1 |
| Passo Fundo #93 | cadastro_controle | outro | 1 |
| Unistalda #8 | revisao_ajuste_minuta | assinatura_instrumento | 2 |
| Unistalda #11 | documento_externo_anexo | tratativa_com_municipio | 2 |

**Correções aplicadas** (`dados/correcoes_rotulos.json`, só da rodada 1). Foram corrigidas as 3 divergências em que a
peça decide objetivamente:

- **Passa Sete #1 → assinatura_instrumento.** A peça é o próprio contrato, como nos casos análogos de Lagoa Bonita do
  Sul e Nova Bréscia.
- **Panambi #11 → tratativa_com_municipio.** É o ofício que remete a via assinada ao prefeito.
- **Passo Fundo #57 → tratativa_com_municipio.** É uma comunicação ao município que a ficha tinha deixado como "outro".

As 8 divergências da rodada 2 não foram corrigidas: nenhuma é decidida só pela peça (Alecrim #3 é a ata da sessão do
Conselho em que o convênio foi assinado; Unistalda #8 é a minuta visada pela DJ, sem assinatura). Elas e as outras 10
da rodada 1 ficam como **perguntas de validação** para os servidores. A concordância informada é a das rodadas às
cegas, antes das correções. **PARADA do método**: abaixo de 85%, a divergência vai ao aluno. Por isso o fluxo continua
indicativo.

## 6. O que isso significa

O procedimento existe no papel (pedido → análise jurídica → minuta → aprovação → assinatura → publicação), mas cada
caso o percorre de um jeito. As variações têm quatro causas observadas: a forma do instrumento (convênio de 2013 a
2020; contrato com inexigibilidade desde 2025; aditivo), quem conduz (GP, DG, DAJ, DAI ou DQS, conforme o caso), a
resposta ao pedido do município (Unistalda reiterou o pedido sem resposta) e a negociação com a CORSAN nos dois maiores
casos recentes. A padronização proposta no processo orientativo e na minuta padrão ataca exatamente essa dispersão. A
avaliação está em `saida/bpmn/avaliacao_CONV.json`.
