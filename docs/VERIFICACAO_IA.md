# Verificação da IA — o que foi julgado por IA e como foi conferido

Material de método (fala de IA, como no repositório do curso). Regra seguida: **a IA escreve nomes, fluxos, decisões e propostas; o código escreve os números.** Cada etapa de julgamento teve especificação escrita antes, saída em formato fixo e verificação por código ou por auditor às cegas.

## 1. Etapas feitas por IA

| Etapa | Quem fez | Especificação | Saída | Verificação | Resultado |
|---|---|---|---|---|---|
| Ficha por peça e narrativa por processo: 1ª rodada (12 processos; Passo Fundo em 2 partes) | 13 agentes Haiku, em paralelo | `ESPECIFICACAO_FICHAS.md` (adaptação do prompt ficha-v2 de `fichas_trabalho.py`) | `dados/fichas/*.jsonl`, `dados/narrativas/*.json` | Ancoragem literal de cada evidência por código (`pipeline_agergs.py`, mesma regra de `ancorar`) | ver linha seguinte |
| Ficha por peça e narrativa: 2ª rodada (Alecrim, Campinas das Missões, Chiapetta, Liberato Salzano, Salvador do Sul, Unistalda) | 6 agentes Haiku, em paralelo | a mesma especificação | idem | idem | 381/381 peças com ficha nas duas rodadas; 732 evidências, **100% ancoradas** (`saida/auditoria_ancoragem.json`) |
| Leitura do processo orientativo e da minuta padrão | 2 agentes Haiku | mesma especificação + esquema próprio | `dados/referencia/processo_orientativo.json`, `minuta_padrao.json` | Evidência literal conferida pelo agente; fichas ancoradas pelo código | Incluídas nos totais acima |
| Rótulo de atividade de cada peça (campo `atividade` da ficha) | os mesmos agentes | lista fechada `ATIVIDADES` | fichas | **Reclassificação às cegas** por outro agente Haiku em cada rodada, sem acesso aos rótulos (`saida/auditoria/amostra_cega.jsonl` e `amostra_cega_2.jsonl`, amostras estratificadas por atividade) | 1ª rodada: 60 peças, 83,3% nas 54 substantivas; 2ª rodada: 37 peças, 78,8% nas 33 substantivas. **Conjunto: 97 peças, 78,4% na tarefa e 81,6% nas 87 substantivas, abaixo do critério de 85%** |
| Base normativa (download do texto integral) | 1 agente Haiku | lista de normas e fontes oficiais | `normas/*.txt`, `normas/indice.json` | Origem registrada por norma; trechos dos requisitos conferidos literalmente (`fase3_agergs.py normas`) | **10/10 trechos literais**; Leis RS 16.266, 15.612 e 10.931 vêm de fonte **secundária** |
| Benchmarking | 1 agente Sonnet | `metodologia-repo/saida/fase3/ESPECIFICACAO_BENCHMARK.md` | `dados/referencia/benchmark.json` (13 práticas) | URL aberta e trecho registrado pelo agente | 13 com `verificado: true`; sem verificação independente por segundo agente; nenhum reporta ganho numérico |
| Modelo canônico AS-IS e TO-BE | agente principal | `metodologia-repo/saida/bpmn/ESPECIFICACAO_MODELO.md` | `saida/bpmn/modelo_CONV*.json` | Gerador do repositório (`gerar_bpmn.py`, validação de estrutura) | 0 falha; 24 e 22 elementos |
| Vínculo atividade → tarefa | agente principal (tabela `ATIV_TAREFA` no código) | idem | `pipeline_agergs.py` | Determinístico; auditado pela reclassificação às cegas | ver acima |
| Avaliação AS-IS | agente principal | `ESPECIFICACAO_AVALIACAO.md` (v2/v3) | modelo `saida/bpmn/avaliacao_CONV.modelo.json` (texto com marcadores `{F:id}`) → `avaliacao_CONV.json` | `fase3_agergs.py avaliacao`: troca cada marcador pelo valor do fato e confere que todo número com unidade é valor de um fato citado | **0 problema** com os 18 casos |
| Requisitos legais | agente principal | `ESPECIFICACAO_CONFORMIDADE.md` | `saida/fase3/normas_CONV.json` | Trecho literal × texto integral | 10/10 |
| Melhorias TO-BE | agente principal | `ESPECIFICACAO_TOBE.md` | `melhorias_CONV.json` | `validar_tobe` (fatos, requisitos, benchmarks, monotonicidade, esperas protegidas, controle humano) | **0 problema** |
| Controles e metas | agente principal (definições) e código (valores) | `ESPECIFICACAO_TOBE.md` (controles) | `controles_CONV.json` via `scripts/controles_agergs.py` | `validar_controles` (linha de base = fato; meta = caminho da simulação ou norma) | **0 problema** |

## 2. Verificações determinísticas

- **Determinismo:** rodadas completas repetidas (`pipeline_agergs.py` e `fase3_agergs.py`) dão `fatos_CONV.json` e `resultado_tobe_CONV.json` idênticos (mesmo md5).
- **Estabilidade na ampliação:** ao incluir os 6 processos novos, os 321 documentos antigos mantiveram `seq` e `doc_id`, e as correções de regra (início do processo, tempo de terceiros) foram aplicadas a todos os casos pela mesma regra.
- **Carimbos:** a linha de base tem carimbo SHA-256 (`linha_base_CONV.json`), e a avaliação registra o `fatos_sha` contra o qual foi validada.
- **Portões:** `fase3_agergs.py` para no primeiro portão que falhar (normas, avaliação, TO-BE, controles). Com os números novos, o portão da avaliação barrou o texto antigo, como esperado, até a reescrita com marcadores.

## 3. PARADA — concordância às cegas abaixo de 85%

Pelo método (AGENTS.md, regra 10), concordância abaixo de 85% exige validação humana. Consequências aplicadas:
1. A situação do código ficou **indicativo**, não *procedimento* (`procedimento_CONV.json`, BPMN).
2. Das 21 divergências das duas rodadas, só 3 foram corrigidas, nas peças que decidem objetivamente (`dados/correcoes_rotulos.json`, com motivo); nenhuma correção foi feita na 2ª rodada, para não ajustar rótulos até passar no critério. As demais ficam para o aluno ou os servidores decidirem (`saida/auditoria/auditoria_classificador_CONV.json`).
3. O percentual informado é o das rodadas cegas, comparado ao rótulo original da ficha, **antes** das correções.

## 4. O que NÃO foi verificado

- As horas por peça e a composição do texto (autoral × padrão) são estimativa: **hipótese até a calibração com servidores**.
- As 33 peças digitalizadas com pouco texto (`baixo_texto`) foram fichadas só pelo título e pelo cabeçalho, sem OCR.
- Datas: a falta de andamentos do SEI impede medir a fila dentro de cada unidade. A espera é inferida pelas datas das peças. Datas escritas no texto com erro (ex.: minuta de Campinas das Missões) foram tratadas por regra, não conferidas uma a uma.
- Nenhum trecho de benchmark foi reconferido por segundo agente. Os trechos de leis obtidos via WebFetch (BM-04 e BM-08 a BM-11) podem ter sido normalizados pela ferramenta.
- As leis RS 16.266/2024 e 15.612/2021 não foram conferidas no DOE-RS.
- Narrativas (situação final, desvios): conferidas só pela ancoragem das evidências, sem auditoria às cegas.
- Volume anual, custo-hora e frações automatizáveis são premissas, não medições.
