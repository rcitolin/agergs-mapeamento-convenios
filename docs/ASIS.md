# AS-IS da celebração de convênios e contratos de delegação da regulação (reconstruído das peças do SEI)

04/11/2026 · fontes: narrativas por processo (`dados/narrativas/*.json`, uma por agente leitor, com evidência literal e
número da peça), indicadores (`saida/processos_indicadores.csv`) e caminho de tarefas (`saida/fase2/casos_CONV.json`).
du = dias úteis. "seq" = número da peça no PDF exportado. Pessoas aparecem só pelo cargo ou pela função. O modelo
canônico que consolida os casos está em `saida/bpmn/modelo_CONV.json` (diagrama em `docs/bpmn/index.html`).

Fluxo de referência usado na comparação: pedido do município → análise jurídica → minuta → aprovação (PSE, Conselho ou
Presidência) → assinatura → publicação → comunicação ao prestador e às unidades → arquivamento.

---

## Convênios de delegação (2013–2020)

### Alecrim — SEI 13.3900.00759-4 · assinado, sem publicação nos autos

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 56 | 24 | 8 | 7 | 2 | 3,1–5,1 |

- **Marcos**: lei municipal autorizativa (seq 5, 01/11/2013), pedido do município (seq 1, 05/11/2013), confirmação da
  CORSAN (seq 2, 20/11/2013) e assinatura do convênio em sessão do Conselho Superior com o prefeito presente (seq 3 e
  seq 6, 11/12/2013).
- **Desvios**: o convênio liga a vigência ao contrato de programa com a CORSAN (seq 7), cujo texto está ilegível e é
  datado depois da assinatura. A lei municipal é anterior ao pedido.
- **Diferença do padrão**: não há parecer jurídico, manifestação da PGE nem minuta no processo; a aprovação e a
  assinatura se confundem na sessão do Conselho. Não há publicação registrada. É o caso mais antigo da coorte, anterior
  às assinaturas eletrônicas lidas pela base.

### Campinas das Missões — SEI 000067-39.00/16-9 · assinado, sem publicação nos autos

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 97 | 97 | 9 | 6 | 1 | 4,7–7,2 |

- **Marcos**: lei municipal autorizativa (seq 2, 29/12/2015), pedido do município (seq 1, 07/01/2016), minuta de
  modelo da DJ (seq 3), minuta ajustada para água e esgoto (seq 6), encaminhamento de 30/05/2016 que registra a
  assinatura (seq 5) e versão assinada escaneada (seq 9).
- **Desvios**: o ofício cita a lei municipal com ano de 2014, mas a lei é de 2015 (seq 1 e 2). A minuta e a versão
  assinada dizem "Porto Alegre, 18 de maio de 2015", data anterior ao próprio pedido (seq 6 e 9). A mesma minuta foi
  reemitida com texto idêntico (seq 6 e 8).
- **Gargalo**: cerca de 118 dias entre o pedido do município e o encaminhamento à DJ (seq 1 a 4, segundo a narrativa).
  Não há parecer jurídico, manifestação da PGE, deliberação do Conselho nem publicação nos autos.
- **Regra nova**: a data de 2015 escrita só no texto, anterior ao início do processo, deixou de ser usada; o lead é
  contado do pedido de 07/01/2016.

### Panambi — SEI 000771-39.00/18-8 · assinado, sem publicação nos autos

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 22 | 2 | 13 | 9 | 1 | 3,4–6,2 |

- **Marcos**: pedido do município (seq 1, 09/07/2018), lei autorizativa de 2010 anexada (seq 2), abertura (seq 3),
  minuta da DJ (seq 7) encaminhada à DG e ao GP no mesmo dia (seq 8 e 9, 11/07/2018), via assinada remetida ao
  prefeito em 23/07/2018 (seq 11) e aviso interno da assinatura em 08/08/2018 (seq 12).
- **Desvios**: minuta e convênio sem data de assinatura no texto (seq 7 e 10). O e-mail interno de aviso da
  assinatura foi anexado ao AR do ofício (seq 12).
- **Diferença do padrão**: não há parecer jurídico formal, deliberação do Conselho Superior nem publicação nos autos.
  Três peças digitalizadas (aditivo e contrato de programa com a CORSAN, seq 5, 6 e 13) não têm texto extraível.

### Salvador do Sul — SEI 001086-39.00/18-3 · assinado e publicado

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 72 | 45 | 13 | 8 | 2 | 4,8–9,7 |

- **Marcos**: lei municipal autorizativa (seq 1, 22/08/2018), pedido do município (seq 1, 04/09/2018), abertura (seq 2,
  06/09/2018), informação jurídica e minuta (seq 6 e 7, 18/10/2018), pedido da Presidência ao município (seq 9),
  convênio assinado (seq 10, 12/11/2018), publicação no DOE (seq 11) e juntada do contrato de programa (seq 12,
  21/12/2018).
- **Desvios**: a informação jurídica cita a Lei Municipal 2.374/2018; o ofício, a minuta e o convênio citam a Lei
  3.383/2018 (seq 1, 6, 7 e 10). O foro mudou sem registro: a minuta prevê o foro do município, o convênio assinado a
  Comarca de Montenegro (seq 7 e 10).
- **Diferença do padrão**: o termo de cooperação com o Estado e o contrato de programa são pedidos só depois da minuta
  (seq 9), e o contrato chega depois da assinatura (seq 12). Não há manifestação da PGE nem deliberação do Conselho; o
  padrão é citado como já aprovado (seq 6). A publicação (seq 11) só tem o título legível.

### Unistalda — SEI 001283-39.00/18-1 · aguardando a AGERGS

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 199 | — | 12 | 6 | 3 | 4,9–7,6 |

- **Marcos**: lei municipal autorizativa (seq 1, 16/10/2018), pedido do município (seq 1, 22/10/2018), abertura (seq 2,
  24/10/2018), informação jurídica (seq 4, 05/11/2018), minuta enviada à Presidência (seq 7, 13/11/2018) e novo pedido
  do município (seq 10, 09/08/2019).
- **Desvios**: o pedido de 2018 não tem resposta registrada; o município reitera em 2019 e reanexa ofício e lei
  (seq 1 e 10). O convênio foi visado pela DJ, mas não tem assinatura no processo (seq 8). A cláusula de foro cita outro
  município (Santiago) nas duas versões da minuta (seq 5 e 8). O termo de cooperação com o Estado, pedido duas vezes
  (seq 4 e 7), não aparece nos autos.
- **Gargalo**: o silêncio da agência entre a minuta e a reiteração do município. É a maior espera antes de um pedido
  na coorte (máximo de 181 du em `coorte.t1.espera_antes.max`) e motivou a regra nova de terceiros: reiteração do
  município é espera da AGERGS, não do município.

### Mampituba — SEI 000212-39.00/19-7 · aguardando o município

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 376 | — | 38 | 15 | 6 | 11,3–21,5 |

- **Marcos**: pedido do município (seq 28, 13/12/2018), abertura (seq 12, 18/02/2019), informação jurídica (seq 17,
  19/03/2019), aprovação do Conselho Superior (Ata 24/2019, seq 21, 10/04/2019) e minutas de convênio e de projeto
  de lei remetidas quatro vezes: mai/2019, ago/2019, dez/2019 e ago/2020 (seq 25, 27, 30 e 33).
- **Desvios**: análise em cascata (DT, DQ, DJ), com estudo de receita e de taxa. A DT recomendou declinar ou cobrar
  2% (seq 14), e a DJ relata manifestação favorável da DQ que não aparece expressa no memorando (seq 13 e 17). A DJ
  cita uma peça com número de documento errado (seq 17). A ata do Conselho está ilegível na cópia digitalizada
  (seq 20). A DG pediu a publicação da documentação em 13/01/2020 (seq 29), sem registro de publicação.
- **Gargalo**: a assinatura depende de uma lei municipal que nunca aparece no processo. Há cerca de sete meses sem
  movimentação (jan a ago/2020).
- **Diferença do padrão**: a prestação é direta, pelo departamento municipal (DEMAEM), sem contrato com prestador. A
  deliberação do Conselho vem antes da minuta. Não há assinatura, publicação nem encerramento. As comunicações com o
  município foram para endereços de e-mail de provedores comerciais.

### Mata — SEI 000734-39.00/19-7 · assinado e publicado

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 105 | — | 21 | 10 | 2 | 6,1–11,4 |

- **Marcos**: pedido do município e lei autorizativa (seq 1, 06/2019), abertura (seq 2, 13/06/2019), ofício pedindo
  4 documentos (seq 8, 17/06/2019), resposta do município 24 dias depois, para um prazo de 10 dias (seq 10,
  11/07/2019), informação jurídica com a minuta (seq 15, 17/07/2019) e súmula publicada no DOE (seq 19, 06/11/2019).
- **Desvios**: dois dos quatro documentos pedidos (convênio com o Estado e contrato com a CORSAN) não aparecem entre
  os anexos da resposta, e o contrato da CORSAN (seq 21) é imagem sem texto. A minuta circulou em duas versões
  (seq 15 e 18). O mesmo ofício foi distribuído a três unidades no mesmo dia por encaminhamentos separados
  (seq 3 a 5).
- **Diferença do padrão**: não há manifestação da PGE nem deliberação do Conselho. O padrão aprovado pelo Conselho
  aparece só como precedente. Entre o parecer e a publicação não há data de assinatura do convênio nos autos.

### Liberato Salzano — SEI 000765-39.00/19-5 · assinado e publicado

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 68 | 68 | 12 | 7 | 1 | 4,8–8,6 |

- **Marcos**: lei municipal autorizativa (seq 1, 21/12/2018), pedido do município (seq 1, 19/06/2019), abertura (seq 2,
  21/06/2019), informação jurídica (seq 5, 15/07/2019), minuta (seq 6), súmula no DOE (seq 10, 25/09/2019) e convênio
  assinado pelas partes (seq 11).
- **Desvios**: a DQ pediu que a fiscalização compartilhada constasse do texto, e a minuta passou a prevê-la (seq 4 e
  6). Um encaminhamento datado de 18/07/2019 só foi assinado em 07/08/2019 (seq 8). A remessa ao município voltou pelos
  Correios sem entrega (seq 12).
- **Diferença do padrão**: fluxo curto, sem manifestação da PGE nem deliberação do Conselho (a minuta-padrão aprovada
  é citada, seq 5). O contrato de programa com a CORSAN, exigido pela informação jurídica, não consta dos autos.

### Jaguari — SEI 000972-39.00/19-5 · assinado e publicado

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 77 | — | 13 | 6 | 2 | 5,5–8,7 |

- **Marcos**: lei autorizativa municipal (seq 1, 16/07/2019), pedido e abertura (seq 1, 01/08/2019), informação
  jurídica (seq 6, 08/08/2019), minuta enviada (seq 9, 19/08/2019), súmula no DOE (seq 11, 06/11/2019) e juntada do
  contrato de programa da CORSAN (seq 13, 20/11/2019).
- **Desvios**: a DJ exigiu o contrato de programa e o termo de cooperação (seq 6), e a DG teve de reiterar a exigência
  (seq 9). O contrato só foi juntado **depois** da publicação.
- **Diferença do padrão**: não há deliberação do Conselho nem registro de assinatura eletrônica nos autos. O AR da
  correspondência ao prefeito é ilegível, e o ofício inicial e o contrato da CORSAN são imagens.

### Vila Nova do Sul — SEI 001132-39.00/19-0 · assinado e publicado

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 82 | 29 | 17 | 8 | 3 | 6,1–12,0 |

- **Marcos**: lei autorizativa (seq 3, 03/09/2019), abertura (seq 5, 17/09/2019), informação jurídica e minuta
  (seq 8 e 10, 23/09/2019) e súmula no DOE (seq 17, 16/01/2020).
- **Desvios**: o CNPJ do município diverge em dígitos entre o e-mail de resposta e a minuta e o convênio, sem
  correção (seq 7, 9 e 16). A localização do convênio é informada de forma divergente: FAMURS ou Gabinete
  (seq 13 a 15).
- **Gargalo**: cerca de três meses sem movimentação entre o memorando de 03/10/2019 (seq 12) e o pedido do município
  de 07/01/2020 (seq 13). A assinatura ficou centralizada no Gabinete (seq 15). Um questionamento do Ministério
  Público ao município pressionou o andamento.
- **Diferença do padrão**: segue a sequência padrão até a aprovação jurídica, sem PGE nem Conselho, com a CORSAN e a
  FAMURS como intervenientes.

### Arambaré — SEI 001470-39.00/19-6 · assinado, sem publicação nos autos

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 237 | 200 | 17 | 11 | 3 | 6,6–12,1 |

- **Marcos**: lei autorizativa (seq 2, 27/11/2019), pedido (seq 1, 28/11/2019), abertura (seq 3, 04/12/2019),
  informação jurídica (seq 5, 09/12/2019), minuta enviada (seq 8, 10/12/2019), assinatura afirmada em 17/12/2019
  (seq 14) e encerramento (seq 17, 10/11/2020).
- **Desvios**: um aditivo para incluir a competência sancionatória (Ofício 49/2020, seq 9) nunca foi firmado. A DQ
  não localizou o convênio, o Gabinete localizou, e a DG cita a assinatura (seq 11 a 14). O convênio foi juntado em
  duas versões escaneadas sem assinatura legível (seq 15 e 16). Um encaminhamento repete quase integralmente outro
  (seq 10 e 12).
- **Gargalo**: sete meses sem movimentação (10/12/2019 a 13/07/2020). O encerramento veio quase 11 meses depois da
  última análise jurídica.

## Termo aditivo (2021)

### Chiapetta — SEI 000802-39.00/21-6 · assinado e publicado

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 3 | — | 6 | 3 | 0 | 1,1–2,6 |

- **Objeto**: termo aditivo a convênio vigente (processo 001466-39.00/19-0) para incluir a competência sancionatória
  (inciso XIV da subcláusula única da cláusula terceira), autorizado pela lei municipal de 15/07/2020 (seq 1).
- **Marcos**: termo assinado em 2020 (seq 1, dia e mês ilegíveis), abertura do processo de publicação (seq 2,
  17/05/2021), súmula (seq 3, 18/05/2021), publicação no DOE (seq 5, 20/05/2021) e envio do termo e da publicação ao
  município.
- **Desvios**: o termo assinado em 2020 só foi levado à súmula em 2021, depois do desmembramento do processo anterior
  (seq 1 e 2). A súmula saiu em lote com 15 súmulas de outros municípios (seq 5).
- **Diferença do padrão**: não há pedido, análise jurídica nem minuta neste processo; ele só cuida de súmula,
  publicação e comunicação. O lead de 3 du mede só essa etapa final.

## Convênio de delegação recente (2026)

### Capão Bonito do Sul — SEI 002718-39.00/26-1 · aguardando a AGERGS

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 26 | — | 17 | 12 | 1 | 4,7–15,7 |

- **Marcos**: pedido do município (seq 1, 11/09/2026), abertura (seq 2, 14/09/2026), manifestação jurídica (seq 5,
  21/09/2026), checklist de documentos da DAI (seq 9, 28/09/2026) e documentação do município por e-mail (seq 16,
  20/10/2026).
- **Desvios**: DSI e PSE declinaram a condução (seq 4 e 5). O expediente passou por DG, GP e DAI antes de a DAI
  assumir. Houve pedido de abertura de processo já autuado (seq 10). O município reiterou um pedido de acesso sem
  resposta (seq 6 e 15).
- **Divergências de escopo e prestador**: a DAI delimita água e esgoto e aponta a CORSAN (seq 9); o município informa
  só abastecimento de água, prestado por departamento municipal criado em 2025 (seq 16 e 17).
- **Gargalo**: segundo a DSI (seq 4), não há unidade formalmente responsável por convênios. É o primeiro caso que já
  segue o checklist da DAI.

## Contratos de prestação de serviços de regulação (2025–2026)

### Passa Sete — SEI 000495-39.00/25-0 · assinado, sem publicação nos autos

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 14 | 0 | 5 | 4 | 0 | 1,9–3,0 |

- O contrato (seq 1) chega já firmado e tem o texto ilegível na extração (páginas rotacionadas, codificação
  corrompida). O GP-CS comunica o contrato e pede providências a DG, DSI e DAF (seq 2, 20/02/2025). A publicação foi
  pedida em 14/03 (seq 5) sem registro de conclusão. O TAAC está em processo-mãe (seq 4).
- **Diferença do padrão**: não há pedido, análise jurídica, PSE, minuta nem aprovação neste processo.

### Lagoa Bonita do Sul — SEI 000684-39.00/25-2 · assinado e publicado

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 15 | 0 | 5 | 4 | 0 | 0,9–2,5 |

- O contrato foi assinado pelo prefeito em 19/02/2025 (seq 1), juntado em 11/03/2025 e publicado no DOE em
  12/03/2025 (seq 5). Ele cita a inexigibilidade nº 08/2025, que está fora deste processo, e é praticamente igual à
  minuta padrão.
- **Desvios**: os comunicados internos chamam o instrumento de "convênio". Há números de encaminhamento citados errado
  (seq 2, 3 e 5).

### Nova Bréscia — SEI 000681-39.00/25-4 · assinado e publicado

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 13 | 0 | 10 | 6 | 1 | 4,0–6,8 |

- Assinatura do município em 05/03/2025 (seq 1), encaminhamento da AGERGS em 11/03 (seq 2), publicação em 12/03
  (seq 5), pedido de cópia pela CORSAN em 18/03 com resposta em 20/03 (seq 6 a 9) e arquivamento em 21/03/2025
  (seq 10).
- **Desvios**: o contrato cita "Lei n. 11.445/2027" (seq 1). A inexigibilidade (nº 017/2025) aparece como processo do
  município, fora dos autos.

### Passo Fundo — SEI 001165-39.00/25-8 · assinado e publicado (com errata)

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 334 | 299 | 99 | 64 | 33 | 35,8–88,4 |

- **Marcos**: pedido e abertura (seq 1, 23/05/2025), informação da PSE (seq 3, 23/06/2025), ofício e minuta à CORSAN
  (seq 6, 30/07/2025), nova informação da PSE (seq 32, 09/12/2025), minuta reenviada (seq 41, 07/01/2026), retirada de
  pauta no Conselho (seq 49), nova análise da PSE (seq 52, 17/04/2026), resolução do Conselho (seq 74, 18/05/2026),
  assinatura (seq 88, 30/07/2026), súmula no DOE (seq 94 e 96, 14/09) e errata de rerratificação (seq 99).
- **Desvios**:
  - A CORSAN contestou a minuta com base em lei e no contrato de concessão (seq 6 a 18). A DG propôs indeferir a
    dilação de prazo, mas o GP a concedeu (seq 14 e 15).
  - Um e-mail foi enviado a endereço desativado da CORSAN (seq 16).
  - A DG pediu nova minuta (seq 19), e o processo foi e voltou entre DG e PSE de set/2025 a jan/2026 (seq 19 a 40).
  - A PSE apontou fundamento legal inadequado na minuta: Lei 14.133 no lugar da Lei 11.445 (seq 32).
  - A cláusula de vigência mudou para 60 meses (seq 52 a 63).
  - A CORSAN pediu suspensão na véspera da sessão, e a ata não registra votação sobre o pedido (seq 76 e 86).
  - Houve cerca de dois meses entre a resolução e a assinatura (seq 81 a 88).
  - A súmula foi publicada antes da assinatura e precisou de errata (seq 94 a 99).
- **Erros materiais**: a minuta final trazia "2025" num contrato de 2026, número de processo em branco, "Lei
  11.445/2027" e foro divergente (seq 41). Há cabeçalhos com data diferente da assinatura (seq 55 e 72) e
  numerações de peças inconsistentes.
- **Diferença do padrão**: é o único caso com oitiva longa do prestador (t16 em laço), duas rodadas de PSE e
  deliberação colegiada contestada. A CORSAN pediu acesso aos autos a cada etapa (seq 84, 90 e 98).

### Minas do Leão — SEI 002063-39.00/25-1 · assinado e publicado

| Lead (du) | Até assinatura (du) | Peças | Passagens | Retornos | Horas piso–teto |
|---|---|---|---|---|---|
| 146 | 137 | 43 | 33 | 21 | 16,9–33,1 |

- **Marcos**: abertura (seq 1, 28/09/2025), lei municipal autorizativa (seq 2), informação jurídica e manifestação da
  PSE (seq 6 e 7, 06/11/2025), minuta enviada (seq 20, 20/02/2026), resolução do Conselho (seq 29, 31/03/2026),
  publicação e comunicação ao prestador (seq 35 e 36, 01/04/2026), encerramento (seq 41, 16/04/2026), contrato assinado
  (seq 42; data ilegível no OCR) e publicação no site da AGERGS (seq 43, 14/09/2026).
- **Desvios**:
  - A minuta inicial regulava água e esgoto, mas a lei municipal autorizava só água (seq 4 e 6). O contrato ficou só
    com água.
  - O voto diz que o município não respondeu a um ofício, mas há resposta por e-mail de 20/02/2026 (seq 19, 20 e 28).
  - O relator questionou a circulação antecipada de voto e minuta (seq 26). A CORSAN pediu retirada de pauta na
    véspera da sessão (seq 30 e 31).
  - O anexo aprovado tem foro em Porto Alegre, e o contrato assinado tem foro no município (seq 33).
  - Dois ofícios foram para um e-mail do município com domínio inválido (seq 32 e 37). Um e-mail cita outro número
    de processo (seq 19).
- **Gargalo**: município sem resposta formal entre 23/12/2025 e 20/02/2026. A CORSAN só teve acesso à minuta na
  véspera da sessão. Houve cerca de cinco meses entre a resolução e a publicação no site.

---

## Processos de gestão de 2026 (referência para o TO-BE)

### Processo orientativo — SEI 002594-39.00/26-9 (Celebração de Instrumentos)

Fonte: `dados/referencia/processo_orientativo.json`. **Objetivo**: estabelecer um procedimento institucional
padronizado para proposição, análise, aprovação, formalização, publicação, implantação, acompanhamento, alteração e
encerramento dos instrumentos de cooperação, delegação e parceria da AGERGS. O processo abrange 13 tipos de
instrumento, entre eles o contrato de delegação da regulação, o convênio de regulação e as alterações relevantes.

**Problemas diagnosticados pela própria AGERGS**: não existe fluxo institucional único; os critérios de transição
entre etapas não estão definidos; os procedimentos seguem práticas administrativas, sem fluxo formal; a falta de
competências definidas gera retrabalho e conflito de atribuições; o processo depende do conhecimento individual; e há
risco de mobilizar a PSE cedo demais em propostas sem aderência institucional.

**Etapas propostas (anexo v1)**:

| # | Etapa | Responsável |
|---|---|---|
| 1 | Identificação da necessidade, abertura do processo e instrução inicial | Unidade proponente / DAI (a DAI coordena desde a origem quando é delegação da regulação) |
| 2 | Articulação institucional, definição do objeto e coleta documental | DAI |
| 3 | Análise técnica e de viabilidade (avança só com conclusão favorável) | Unidade técnica competente (DSI, DEGIP, DTM, DAF, DTI…) |
| 4 | Validação institucional e autorização de prosseguimento | DG, com DAI e unidades impactadas |
| 5 | Estruturação jurídica e controle de legalidade | PSE |
| 6 | Definição do rito decisório e encaminhamento | GP / Presidência |
| 7 | Análise e deliberação (aprovar, condicionar, rejeitar) | Presidência ou Conselho Superior |
| 8 | Formalização e assinatura | DAI |
| 9 | Publicação e comunicação institucional | DG, com ACS, DAF, DAI, GP e unidade técnica |
| 10 | Implantação e início da execução | DG (coordenação executiva) |
| 11 | Monitoramento, alteração, renovação e encerramento | DAI e unidade gestora |

**Lacunas em aberto**:
- Não há prazos por etapa. O único prazo é de 15 dias úteis para as unidades se manifestarem.
- A forma normativa (instrução normativa ou equivalente) não foi decidida.
- Não há critério objetivo para escolher entre Presidência e Conselho nas parcerias estratégicas.
- A lista de documentos é indicativa, sem checklist mínimo por modalidade, e a classificação processual SEI não foi
  definida.
- A DG aparece como executora nas etapas 4, 9 e 10, embora o texto diga que ela não deve executar.
- A regra de deliberação cita a "Etapa 8", mas a deliberação é a etapa 7.
- O escopo da DSI diverge entre a justificativa e o anexo.
- A DTM pediu prazo adicional, sem deferimento nos autos, e as demais manifestações estão pendentes.

### Minuta padrão do contrato de delegação — SEI 002840-39.00/26-3

Fonte: `dados/referencia/minuta_padrao.json`. **Objetivo**: padronizar, em 2026, a minuta de contrato de delegação
da regulação (água e esgoto), comparar os contratos já celebrados, propor documentação mínima e reunir as
manifestações de DAU, PSE, DSI e DAI.

**Divergências entre contratos já assinados**:
- **Fundamento legal**: art. 74 da Lei 14.133 na maioria dos contratos; art. 8º, § 5º, da Lei 11.445 em Passo Fundo.
  A PSE 320 recomenda não citar a Lei 14.133.
- **Vigência**: 60 meses em Passo Fundo; concomitante à concessão nos demais.
- **Hipóteses de rescisão**: art. 23, § 1º-B, ou com acréscimo do "não exercício de competências", que a PSE manda
  suprimir.
- **Cláusulas que só aparecem em parte dos contratos**: competência de homologar o instrumento da concessão (só em
  dois contratos); custeio de 0,6% com periodicidade internamente contraditória em três contratos; foro de Porto
  Alegre ou do município; canal de atendimento ao usuário (Ouvidoria ou DAU).
- **Erros materiais**: "Lei n. 11.445/2027" em quatro contratos e "Município de Xxx" em dois.

**Manifestações**:

| Unidade | Posição |
|---|---|
| DAU | Adequada a previsão de atendimento pela AGERGS e de divulgação de canais pelo município |
| PSE | Aprova juridicamente a minuta e o checklist, com dois ajustes: excluir a vigência de 60 meses e restringir a rescisão ao art. 23, § 1º-B |
| DSI | Concorda e acolhe os ajustes; propõe anexo único para quatro componentes (água, esgoto, resíduos, drenagem), com ativação e custeio por resolução (ainda sem análise da PSE) |
| DAI | Favorável; propõe materiais orientativos, fluxo de recepção de demandas e articulação federativa |

**Documentação mínima proposta** (classificada em obrigatório, importante e complementar):
- manifestação formal de interesse do município;
- serviços a delegar;
- prestador;
- contrato de concessão ou de programa vigente;
- lei municipal autorizativa, quando houver;
- PMSB, quando aplicável;
- regulação anterior por outra entidade.

**Pendências**:
- Os contratos de Itaara e Morro Redondo, citados como firmados, estão sem assinatura no conjunto.
- O texto do contrato de Passa Sete está ilegível.
- O anexo único da DSI não está no conjunto.
- Falta decidir o tratamento do contrato vigente de Passo Fundo (60 meses).
- O item de canal de atendimento ao usuário ainda não entrou no checklist.
- Falta definir o foro padrão.

---

## Síntese transversal

1. **Não há dono do processo nem prazo para responder ao município.** A condução passa por GP, DG, DAJ, DAI ou DQS, conforme o caso. Em 2026, a DSI afirma
   que não há unidade formalmente responsável (Capão Bonito do Sul). Em Unistalda, o pedido de 2018 ficou sem
   resposta até o município reiterá-lo em 2019.
2. **A instrução está fragmentada.** Nos contratos de 2025, inexigibilidade, TAAC e assinatura do município ficam fora
   do processo de celebração, que só registra a juntada, a publicação e a comunicação.
3. **Documentação em rodadas.** Lei autorizativa, contrato com o prestador e PMSB são pedidos e reiterados, às vezes
   depois da publicação ou da assinatura (Jaguari, Salvador do Sul), e o escopo diverge da lei municipal (Minas do Leão; Capão Bonito do Sul).
4. **Cada caso tem sua minuta.** Cláusulas e erros materiais diferentes entre contratos motivaram o processo da minuta
   padrão. Os convênios antigos repetem os mesmos erros: foro de outro município (Unistalda), foro trocado entre
   minuta e convênio (Salvador do Sul), número e ano de lei municipal divergentes (Salvador do Sul, Campinas das
   Missões).
5. **Publicação e encerramento sem marco.** Há súmula antes da assinatura (Passo Fundo), cinco casos assinados sem
   publicação nos autos, aditivo assinado em 2020 e publicado só em 2021 (Chiapetta) e encerramento meses depois da
   última providência (Arambaré).
6. **Oitiva do prestador sem prazo fixo.** Nos dois maiores casos recentes, a CORSAN contesta a minuta e pede retirada
   de pauta na véspera da sessão.
7. **Instâncias formais ausentes nos convênios antigos.** Em Alecrim, Campinas das Missões, Salvador do Sul, Liberato
   Salzano e Unistalda não há manifestação da PGE nem deliberação do Conselho nos autos; a minuta-padrão aprovada é
   citada como já existente, e em Alecrim a assinatura acontece na própria sessão do Conselho.
